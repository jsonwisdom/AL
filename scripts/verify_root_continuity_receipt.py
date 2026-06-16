#!/usr/bin/env python3
"""Verify Root Continuity Checkpoint receipts.

Current-tip mode compares receipt HEAD to the current repository HEAD.
Historical mode verifies internal receipt consistency without requiring the
current repository state to equal the receipt's point-in-time state.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REQUIRED_OPERATION = "root_continuity_checkpoint"
REQUIRED_CHECKS = [
    "local_bare_repo",
    "github_reachable",
    "mirror_reachable",
    "commits_aligned",
    "restore_path_documented",
]


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def load_receipt(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    print(f"RECEIPT_REJECTED: {message}")
    sys.exit(1)


def expected_status_from_checks(checks: dict[str, Any]) -> str:
    return "success" if all(checks.get(key) is True for key in REQUIRED_CHECKS) else "failure"


def main() -> int:
    args = sys.argv[1:]
    historical = False
    if "--historical" in args:
        historical = True
        args.remove("--historical")

    if len(args) != 1:
        print("usage: scripts/verify_root_continuity_receipt.py [--historical] <receipt.json>")
        return 2

    receipt_path = Path(args[0])
    receipt = load_receipt(receipt_path)

    operation = receipt.get("operation", {})
    if operation.get("type") != REQUIRED_OPERATION:
        fail(f"unsupported operation type: {operation.get('type')}")

    checks = receipt.get("checks", {})
    for key in REQUIRED_CHECKS:
        if key not in checks or not isinstance(checks[key], bool):
            fail(f"missing or invalid check field: {key}")

    outcome = receipt.get("outcome", {})
    result = outcome.get("result", {})
    recorded_head = result.get("head_commit")
    if not recorded_head:
        fail("missing outcome.result.head_commit")

    expected_status = expected_status_from_checks(checks)
    if outcome.get("status") != expected_status:
        fail(f"status mismatch: recorded={outcome.get('status')} expected={expected_status}")

    current_head = None
    if not historical:
        current_head = run_git(["rev-parse", "HEAD"])
        if recorded_head != current_head:
            fail(f"head_commit mismatch: recorded={recorded_head} current={current_head}")

    print("RECEIPT_CONFIRMED")
    print(f"mode: {'historical' if historical else 'current-tip'}")
    print(f"receipt_id: {receipt.get('receipt_id')}")
    print(f"operation: {operation.get('type')}")
    print(f"recorded_head: {recorded_head}")
    if current_head:
        print(f"current_head: {current_head}")
    print(f"verifier_verdict: confirmed")
    print(f"recorded_outcome_status: {outcome.get('status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
