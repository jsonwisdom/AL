#!/usr/bin/env python3
"""Verify Root Continuity Checkpoint receipts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REQUIRED_OPERATION = "root_continuity_checkpoint"


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def load_receipt(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    print(f"RECEIPT_REJECTED: {message}")
    sys.exit(1)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: scripts/verify_root_continuity_receipt.py <receipt.json>")
        return 2

    receipt_path = Path(sys.argv[1])
    receipt = load_receipt(receipt_path)

    operation = receipt.get("operation", {})
    if operation.get("type") != REQUIRED_OPERATION:
        fail(f"unsupported operation type: {operation.get('type')}")

    outcome = receipt.get("outcome", {})
    result = outcome.get("result", {})

    current_head = run_git(["rev-parse", "HEAD"])
    recorded_head = result.get("head_commit")

    if recorded_head != current_head:
        fail(f"head_commit mismatch: recorded={recorded_head} current={current_head}")

    checks = receipt.get("checks", {})

    expected_status = "success" if all(
        checks.get(key) is True
        for key in [
            "local_bare_repo",
            "github_reachable",
            "mirror_reachable",
            "commits_aligned",
            "restore_path_documented",
        ]
    ) else "failure"

    if outcome.get("status") != expected_status:
        fail(
            f"status mismatch: recorded={outcome.get('status')} expected={expected_status}"
        )

    print("RECEIPT_CONFIRMED")
    print(f"receipt_id: {receipt.get('receipt_id')}")
    print(f"operation: {operation.get('type')}")
    print(f"head_commit: {current_head}")
    print(f"status: {outcome.get('status')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
