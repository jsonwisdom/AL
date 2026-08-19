#!/usr/bin/env python3
"""Append one source-bound workflow execution receipt to the JSONWisdom global ledger.

This writer is intentionally conservative:
- no synthetic workflow identity or timestamps;
- no PASS when the replay report is missing/invalid;
- duplicate workflow_run_id + workflow_attempt is rejected;
- each JSONL row is hash-linked to the previous row;
- authority is always false and no_fake_green is always true.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from jsonschema import Draft202012Validator, FormatChecker

DEFAULT_REPORT = Path("ci/corpus_report.json")
DEFAULT_LEDGER = Path("alms/global_execution_ledger/ledger.jsonl")
DEFAULT_SCHEMA = Path("schemas/JSONWISDOM_GLOBAL_EXECUTION_LEDGER_V0_1.schema.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_report(path: Path) -> tuple[str, Optional[str], Dict[str, Any]]:
    if not path.exists():
        return "MISSING", None, {}

    raw = path.read_bytes()
    digest = sha256_bytes(raw)
    try:
        report = json.loads(raw)
    except Exception:
        return "INVALID", digest, {}

    verdict = report.get("verdict")
    if verdict not in {"PASS", "FAIL"}:
        return "INVALID", digest, report
    return verdict, digest, report


def as_nonnegative_int(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return max(parsed, 0)


def hard_gate_result(exit_code: int, report_verdict: str) -> str:
    if exit_code == 0 and report_verdict == "PASS":
        return "PASS"
    if report_verdict == "FAIL":
        return "REJECT"
    if report_verdict in {"MISSING", "INVALID"}:
        return "HOLD"
    return "CONFLICT"


def load_existing(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []

    rows: List[Dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text().splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            rows.append(json.loads(raw_line))
        except Exception as exc:
            raise SystemExit(f"invalid ledger JSONL at line {line_number}: {exc}") from exc
    return rows


def required_text(value: Optional[str], label: str) -> str:
    if not value:
        raise SystemExit(f"missing required {label}")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY"))
    parser.add_argument("--ref", default=os.getenv("GITHUB_REF_NAME"))
    parser.add_argument("--commit-sha", default=os.getenv("GITHUB_SHA"))
    parser.add_argument("--workflow-name", default=os.getenv("GITHUB_WORKFLOW"))
    parser.add_argument("--workflow-run-id", default=os.getenv("GITHUB_RUN_ID"))
    parser.add_argument("--workflow-attempt", type=int, default=int(os.getenv("GITHUB_RUN_ATTEMPT", "1")))
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--completed-at", required=True)
    parser.add_argument("--runner-exit-code", type=int, required=True)
    parser.add_argument("--alms-version")
    parser.add_argument("--requested-replay-parameter", type=int)
    parser.add_argument("--requested-replay-unit", default="UNBOUND")
    parser.add_argument("--receipt-id", action="append", default=[])
    parser.add_argument("--source-hash", action="append", default=[])
    parser.add_argument("--replay-hash")
    parser.add_argument("--receiptos-frame")
    parser.add_argument("--ens-pointer")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    repo = required_text(args.repo, "repo")
    ref = required_text(args.ref, "ref")
    commit_sha = required_text(args.commit_sha, "commit_sha")
    workflow_name = required_text(args.workflow_name, "workflow_name")
    workflow_run_id = required_text(args.workflow_run_id, "workflow_run_id")

    report_verdict, report_sha256, report = read_report(args.report)
    total_cases = as_nonnegative_int(report.get("total_cases"))
    pass_count = as_nonnegative_int(report.get("pass"))
    fail_count = as_nonnegative_int(report.get("fail"))
    indeterminate_count = as_nonnegative_int(report.get("indeterminate"))
    validated = pass_count + fail_count + indeterminate_count

    existing = load_existing(args.ledger)
    for row in existing:
        if (
            str(row.get("workflow_run_id")) == str(workflow_run_id)
            and int(row.get("workflow_attempt", 0)) == args.workflow_attempt
        ):
            raise SystemExit(
                "workflow run already bound in ledger: "
                f"run_id={workflow_run_id} attempt={args.workflow_attempt}"
            )

    previous_entry_sha256 = existing[-1].get("entry_sha256") if existing else None
    requested_parameter = None
    if args.requested_replay_parameter is not None:
        requested_parameter = {
            "value": args.requested_replay_parameter,
            "unit": args.requested_replay_unit,
        }

    payload: Dict[str, Any] = {
        "schema_version": "0.1",
        "ledger_id": "JSONWISDOM_GLOBAL_EXECUTION_LEDGER",
        "record_type": "WORKFLOW_EXECUTION_RECEIPT",
        "sequence": len(existing) + 1,
        "repo": repo,
        "ref": ref,
        "commit_sha": commit_sha,
        "workflow_name": workflow_name,
        "workflow_run_id": str(workflow_run_id),
        "workflow_attempt": args.workflow_attempt,
        "started_at": args.started_at,
        "completed_at": args.completed_at,
        "alms_version": args.alms_version,
        "report": {
            "path": str(args.report),
            "sha256": report_sha256,
            "verdict": report_verdict,
        },
        "counters": {
            "items_requested": total_cases,
            "items_observed": total_cases,
            "items_validated": validated,
            "items_passed": pass_count,
            "items_held": 0,
            "items_conflicted": 0,
            "items_rejected": fail_count,
            "items_indeterminate": indeterminate_count,
        },
        "runner": {
            "name": "ci/replay_corpus_runner.py",
            "exit_code": args.runner_exit_code,
            "hard_gate_result": hard_gate_result(args.runner_exit_code, report_verdict),
        },
        "requested_replay_parameter": requested_parameter,
        "receipt_ids": sorted(set(args.receipt_id)),
        "source_hashes": sorted(set(args.source_hash)),
        "replay_hash": args.replay_hash,
        "receiptos_frame": args.receiptos_frame,
        "ens_pointer": args.ens_pointer,
        "previous_entry_sha256": previous_entry_sha256,
        "authority": False,
        "no_fake_green": True,
    }

    canonical_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    payload["entry_sha256"] = sha256_bytes(canonical_payload)

    schema = json.loads(args.schema.read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
    if errors:
        rendered = "\n".join(f"- {'.'.join(map(str, err.path))}: {err.message}" for err in errors)
        raise SystemExit(f"global execution ledger schema validation failed:\n{rendered}")

    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    with args.ledger.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
        handle.write("\n")

    print(
        "GLOBAL_EXECUTION_LEDGER_APPEND "
        f"sequence={payload['sequence']} "
        f"run_id={workflow_run_id} "
        f"hard_gate={payload['runner']['hard_gate_result']} "
        f"entry_sha256={payload['entry_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
