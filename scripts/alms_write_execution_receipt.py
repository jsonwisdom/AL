#!/usr/bin/env python3
"""ALMS Execution Receipt Writer — fail-closed history surface.

Emits a terminal execution receipt for one GitHub Actions replay attempt.

Boundaries:
- never sets authority=true;
- never claims PASS when runner_exit_code != 0;
- distinguishes FAIL, INDETERMINATE, and ERROR;
- hashes the exact corpus report bytes when present;
- uses deterministic compact sorted-key JSON for receipt hashing;
- does not claim RFC 8785 JCS compatibility;
- terminal receipt generation is best-effort after the runner step. A whole-job
  timeout, cancellation, or runner-host loss can prevent this post-step from
  executing; a future two-phase STARTED -> TERMINAL receipt can close that gap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_prefixed(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_object(obj: Any) -> str:
    return sha256_prefixed(canonical_json_bytes(obj))


def parse_report(path: Path) -> Tuple[str, Optional[Dict[str, Any]], Optional[str], Optional[str]]:
    """Return (state, parsed_report, sha256, parse_error)."""
    if not path.exists():
        return "MISSING", None, None, None

    raw = path.read_bytes()
    digest = sha256_prefixed(raw)

    try:
        parsed = json.loads(raw)
    except Exception as exc:
        return "INVALID", None, digest, str(exc)

    if not isinstance(parsed, dict):
        return "INVALID", None, digest, "top-level report must be a JSON object"

    return "PARSED", parsed, digest, None


def nonnegative_int(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return max(parsed, 0)


def classify_verdict(exit_code: int, report_state: str, report: Optional[Dict[str, Any]]) -> str:
    if report_state != "PARSED" or report is None:
        return "ERROR"

    report_verdict = report.get("verdict")
    failed = nonnegative_int(report.get("fail"))
    indeterminate = nonnegative_int(report.get("indeterminate"))

    if exit_code == 0 and report_verdict == "PASS":
        return "PASS"

    if failed > 0:
        return "FAIL"

    if indeterminate > 0:
        return "INDETERMINATE"

    if report_verdict == "FAIL":
        return "FAIL"

    return "ERROR"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--runner-exit-code", required=True, type=int)
    p.add_argument("--workflow-run-id", required=True)
    p.add_argument("--workflow-run-attempt", default="1")
    p.add_argument("--repo", required=True)
    p.add_argument("--ref", required=True)
    p.add_argument("--sha", required=True)
    p.add_argument("--actor", default="")
    p.add_argument("--event-name", default="")
    p.add_argument("--workflow-name", default="")
    p.add_argument("--started-at", default="")
    p.add_argument("--completed-at", default="")
    p.add_argument("--report-path", default="ci/corpus_report.json")
    p.add_argument("--out-dir", default="alms/execution_receipts")
    p.add_argument("--alms-version", default="UNBOUND")
    p.add_argument("--receiptos-frame")
    p.add_argument("--ens-pointer")
    p.add_argument("--requested-replay-parameter", type=int)
    p.add_argument("--requested-replay-unit", default="UNBOUND")
    return p


def main() -> int:
    args = build_parser().parse_args()

    report_path = Path(args.report_path)
    report_state, report, report_hash, parse_error = parse_report(report_path)
    report = report or {}

    verdict = classify_verdict(args.runner_exit_code, report_state, report)

    now = datetime.now(timezone.utc)
    timestamp = now.isoformat().replace("+00:00", "Z")
    receipt_id = f"exec_{args.workflow_run_id}_{args.workflow_run_attempt}"

    requested_replay = None
    if args.requested_replay_parameter is not None:
        requested_replay = {
            "value": args.requested_replay_parameter,
            "unit": args.requested_replay_unit,
        }

    execution = {
        "workflow_name": args.workflow_name,
        "workflow_run_id": str(args.workflow_run_id),
        "workflow_run_attempt": str(args.workflow_run_attempt),
        "repo": args.repo,
        "ref": args.ref,
        "commit": args.sha,
        "actor": args.actor,
        "event_name": args.event_name,
        "runner_started_at": args.started_at or None,
        "runner_completed_at": args.completed_at or None,
        "runner_exit_code": args.runner_exit_code,
        "verdict": verdict,
        "items_requested": report.get("total_cases"),
        "items_passed": report.get("pass"),
        "items_failed": report.get("fail"),
        "items_indeterminate": report.get("indeterminate"),
        "failed_cases": report.get("failed_cases", []),
        "corpus_report_state": report_state,
        "corpus_report_present": report_path.exists(),
        "corpus_report_parse_error": parse_error,
    }

    receipt: Dict[str, Any] = {
        "receipt_id": receipt_id,
        "receipt_type": "EXECUTION_RECEIPT",
        "version": "0.2",
        "phase": "TERMINAL",
        "timestamp": timestamp,
        "authority": False,
        "proof_inferred": False,
        "no_fake_green": True,
        "canonicalization": {
            "method": "JSON_SORTED_KEYS_COMPACT_UTF8_V0_1",
            "hash_alg": "sha256",
            "rfc8785_jcs_claimed": False,
        },
        "execution": execution,
        "requested_replay_parameter": requested_replay,
        "bindings": {
            "alms_version": args.alms_version,
            "receiptos_frame": args.receiptos_frame,
            "ens_pointer": args.ens_pointer,
        },
        "source_hashes": {
            "corpus_report": report_hash,
        },
        "limitations": {
            "post_step_terminal_receipt": True,
            "whole_job_timeout_or_cancellation_can_prevent_terminal_receipt": True,
            "runner_host_loss_can_prevent_terminal_receipt": True,
            "future_two_phase_started_terminal_receipt_recommended": True,
        },
    }

    core_view = {
        k: v
        for k, v in receipt.items()
        if k not in ("section_hashes", "final_hash", "attestations")
    }

    receipt["section_hashes"] = {
        "execution_hash": sha256_object(receipt["execution"]),
        "core_hash": sha256_object(core_view),
    }

    final_view = {k: v for k, v in receipt.items() if k != "final_hash"}
    receipt["final_hash"] = sha256_object(final_view)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{receipt_id}.json"
    out_path.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"WROTE {out_path} "
        f"verdict={verdict} "
        f"exit={args.runner_exit_code} "
        f"report={report_state} "
        f"final_hash={receipt['final_hash']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
