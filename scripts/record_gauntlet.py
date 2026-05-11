#!/usr/bin/env python3
"""Record a gauntlet run into the canonical spine.

This script establishes the execution surface required by #177.
It does NOT self-activate #176. Independent verification is still required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

from alms.ci_receipt import CIReceipt, CIReceiptManager


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def git_sha() -> str:
    return subprocess.check_output([
        "git", "rev-parse", "HEAD"
    ]).decode().strip()


def workflow_sha(workflow_file: Path) -> str:
    return sha256_file(workflow_file)


def run_pytest() -> dict:
    result = subprocess.run(
        ["python", "-m", "pytest", "tests", "-q"],
        capture_output=True,
        text=True,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--storage-path", required=True)
    parser.add_argument("--workflow-file", required=True)
    args = parser.parse_args()

    storage_path = Path(args.storage_path)
    workflow_file = Path(args.workflow_file)

    manager = CIReceiptManager(storage_path)

    parent_root = manager.ensure_genesis()

    pre_run_tip = manager.current_tip()

    pytest_result = run_pytest()

    post_run_tip = manager.current_tip()

    if pre_run_tip != post_run_tip:
        print("ABORT_SPINE_TIP_CHANGED_DURING_GAUNTLET")
        return 2

    receipt = CIReceipt(
        run_id=f"local-{time.time_ns()}",
        commit_sha=git_sha(),
        workflow_sha=workflow_sha(workflow_file),
        suite="full_gauntlet",
        replay_result={
            "pytest_returncode": pytest_result["returncode"]
        },
        fuzz_stats={},
        artifact_hashes={
            "workflow": workflow_sha(workflow_file)
        },
        timestamp_ns=time.time_ns(),
        parent_cumulative_root=parent_root,
    )

    receipt_hash = manager.record(receipt)

    output = {
        "receipt_hash": receipt_hash,
        "parent_cumulative_root": parent_root,
        "commit_sha": receipt.commit_sha,
        "workflow_sha": receipt.workflow_sha,
        "pytest_returncode": pytest_result["returncode"],
        "status": "RECORDED_NOT_YET_VERIFIED",
    }

    print(json.dumps(output, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
