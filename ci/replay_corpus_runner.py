#!/usr/bin/env python3
"""
TRACK_00X_10 — Deterministic Replay Corpus Runner

Runs corpus/* entries through the ALMS CI gate chain and verifies replay output
against frozen expected hashes and identity bindings.

Rules enforced:
- Replay hash source of truth is pipeline/receipt/receipt_replay_manifest.json
- Expected identity is checked against the record identity in the replay manifest
- replay_gate_check must execute
- Non-zero gates fail the corpus item, except integration_matrix_t01_t08 may remain
  INDETERMINATE while TRACK_00X_6 fixtures are not fully implemented
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CORPUS_ROOT = Path("corpus")
REPORT_PATH = Path("ci/corpus_report.json")
REPLAY_MANIFEST_PATH = Path("pipeline/receipt/receipt_replay_manifest.json")
ALLOWED_INDETERMINATE_GATE = "integration_matrix_t01_t08"


def reset_runtime() -> None:
    for path_name in ["pipeline", "source", "policy", "replay"]:
        path = Path(path_name)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()


def load_json(path: Path | str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())


def copytree_if_exists(src: Path, dest: Path) -> None:
    if src.exists():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)


def run_pipeline() -> Tuple[int, Dict[str, Any]]:
    proc = subprocess.run(
        ["python", "ci/run_all_gates.py", "--mode", "audit_full"],
        capture_output=True,
        text=True,
        check=False,
    )

    report_path = Path("ci/report.json")
    if not report_path.exists():
        return 2, {
            "gates": [],
            "runner_stdout": proc.stdout,
            "runner_stderr": proc.stderr,
            "error": "missing_ci_report",
        }

    report = load_json(report_path)
    report["runner_stdout"] = proc.stdout
    report["runner_stderr"] = proc.stderr
    return proc.returncode, report


def gate_executed(report: Dict[str, Any], gate_name: str) -> bool:
    return any(gate.get("gate") == gate_name for gate in report.get("gates", []))


def first_blocking_gate(report: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for gate in report.get("gates", []):
        if gate.get("exit_code") != 0 and gate.get("gate") != ALLOWED_INDETERMINATE_GATE:
            return gate
    return None


def evaluate_case(case_dir: Path) -> Tuple[str, Optional[str], Dict[str, Any]]:
    reset_runtime()

    source_dir = case_dir / "source"
    if not source_dir.exists():
        return "INDETERMINATE", "missing_source", {}
    shutil.copytree(source_dir, Path("source"))

    manifests_dir = case_dir / "manifests"
    if not manifests_dir.exists():
        return "INDETERMINATE", "missing_manifests", {}
    shutil.copytree(manifests_dir, Path("pipeline"))

    copytree_if_exists(case_dir / "policy", Path("policy"))
    copytree_if_exists(case_dir / "replay", Path("replay"))

    expected_path = case_dir / "replay" / "expected_hashes.json"
    if not expected_path.exists():
        return "INDETERMINATE", "missing_expected_hashes", {}

    try:
        expected = load_json(expected_path)
    except Exception as exc:
        return "INDETERMINATE", f"invalid_expected_hashes:{exc}", {}

    expected_hash = expected.get("normalized_artifact_hash")
    if not expected_hash:
        return "INDETERMINATE", "missing_expected_normalized_hash", {}

    code, report = run_pipeline()

    if not gate_executed(report, "replay_gate_check"):
        return "INDETERMINATE", "replay_gate_not_executed", {"ci_exit_code": code, "ci_report": report}

    blocking_gate = first_blocking_gate(report)
    if blocking_gate is not None:
        return (
            "FAIL",
            f"gate_{blocking_gate.get('gate')}_{blocking_gate.get('verdict')}",
            {"ci_exit_code": code, "ci_report": report},
        )

    if not REPLAY_MANIFEST_PATH.exists():
        return "INDETERMINATE", "missing_replay_manifest", {"ci_exit_code": code, "ci_report": report}

    try:
        replay_data = load_json(REPLAY_MANIFEST_PATH)
    except Exception as exc:
        return "INDETERMINATE", f"invalid_replay_manifest:{exc}", {"ci_exit_code": code, "ci_report": report}

    actual_hash = replay_data.get("normalized_artifact_hash_replay")
    if actual_hash is None:
        return "INDETERMINATE", "missing_replay_hash", {"ci_exit_code": code, "ci_report": report}

    if actual_hash != expected_hash:
        return (
            "FAIL",
            "hash_mismatch",
            {
                "expected_hash": expected_hash,
                "actual_hash": actual_hash,
                "ci_exit_code": code,
                "ci_report": report,
            },
        )

    expected_identity = expected.get("identity", {})
    record_identity = {
        "source_url": replay_data.get("record_source_url"),
        "canonical_url": replay_data.get("record_canonical_url"),
        "FETCH_FINGERPRINT": replay_data.get("record_FETCH_FINGERPRINT"),
    }

    if expected_identity and record_identity != expected_identity:
        return (
            "FAIL",
            "identity_mismatch",
            {
                "expected_identity": expected_identity,
                "record_identity": record_identity,
                "ci_exit_code": code,
                "ci_report": report,
            },
        )

    return "PASS", None, {"ci_exit_code": code, "ci_report": report}


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CORPUS_ROOT.exists():
        report = {
            "total_cases": 0,
            "pass": 0,
            "fail": 0,
            "indeterminate": 1,
            "failed_cases": [{"case": None, "reason": "missing_corpus_root"}],
            "verdict": "FAIL",
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2))
        return 1

    cases = sorted(path for path in CORPUS_ROOT.iterdir() if path.is_dir())
    pass_count = 0
    fail_count = 0
    indeterminate_count = 0
    failed_cases: List[Dict[str, Any]] = []

    for case_dir in cases:
        case_id = case_dir.name
        verdict, reason, details = evaluate_case(case_dir)

        if verdict == "PASS":
            pass_count += 1
        elif verdict == "FAIL":
            fail_count += 1
            failed_cases.append({"case": case_id, "reason": reason, "details": details})
        else:
            indeterminate_count += 1
            failed_cases.append({"case": case_id, "reason": reason, "details": details})

    final_verdict = "PASS" if fail_count == 0 and indeterminate_count == 0 else "FAIL"
    report = {
        "total_cases": len(cases),
        "pass": pass_count,
        "fail": fail_count,
        "indeterminate": indeterminate_count,
        "failed_cases": failed_cases,
        "verdict": final_verdict,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    return 0 if final_verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
