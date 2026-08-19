#!/usr/bin/env python3
"""Bind ACTIVE_LANES.json only to verified entries on the global execution ledger.

Rules:
- the ledger chain is verified before pointers are considered;
- a non-null receipt_ptr must resolve to a real ledger entry;
- exact known lane->repo bindings may advance to the latest matching ledger entry;
- lanes without a matching real receipt remain unbound / UNAVAILABLE;
- no receipt, PASS, or authority is inferred.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from alms_consume_execution_receipts import load_existing_ledger

LANES_PATH = Path("ACTIVE_LANES.json")

LANE_REPO_BINDINGS = {
    "AL": "jsonwisdom/AL",
    "COMPUTERWISDOM": "jsonwisdom/COMPUTERWISDOM",
    "JOY": "jsonwisdom/JOY",
}


def status_for_verdict(verdict: str) -> str:
    return {
        "PASS": "RECEIPTED",
        "FAIL": "RECEIPTED_FAIL",
        "INDETERMINATE": "RECEIPTED_INDETERMINATE",
        "ERROR": "RECEIPTED_ERROR",
    }.get(verdict, "REPORTED_UNVERIFIED")


def main() -> int:
    if not LANES_PATH.exists():
        print("ACTIVE_LANES.json missing", file=sys.stderr)
        return 1

    try:
        entries, _, _, _ = load_existing_ledger()
        lanes_doc = json.loads(LANES_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"LANE_BIND_REJECT {exc}", file=sys.stderr)
        return 1

    by_receipt_id: Dict[str, Dict[str, Any]] = {
        entry["receipt_id"]: entry for entry in entries
    }
    latest_by_repo: Dict[str, Dict[str, Any]] = {}
    for entry in entries:
        repo = entry.get("repo")
        if repo:
            latest_by_repo[repo] = entry

    changed = False

    for lane in lanes_doc.get("lanes", []):
        lane_id = lane.get("lane_id")
        ptr = lane.get("receipt_ptr")

        if ptr is not None and ptr not in by_receipt_id:
            lane["receipt_ptr"] = None
            lane["replay_verdict"] = "UNAVAILABLE"
            lane["status"] = "REPORTED_UNVERIFIED"
            lane["status_source"] = "EXECUTION_LEDGER_UNRESOLVED"
            changed = True

        expected_repo = LANE_REPO_BINDINGS.get(lane_id)
        latest = latest_by_repo.get(expected_repo) if expected_repo else None

        if latest is None:
            if (
                lane.get("receipt_ptr") is None
                and lane.get("replay_verdict") != "UNAVAILABLE"
            ):
                lane["replay_verdict"] = "UNAVAILABLE"
                changed = True
            continue

        if lane.get("receipt_ptr") != latest["receipt_id"]:
            lane["receipt_ptr"] = latest["receipt_id"]
            changed = True
        if lane.get("replay_verdict") != latest["verdict"]:
            lane["replay_verdict"] = latest["verdict"]
            changed = True

        status = status_for_verdict(latest["verdict"])
        if lane.get("status") != status:
            lane["status"] = status
            changed = True
        if lane.get("status_source") != "EXECUTION_LEDGER":
            lane["status_source"] = "EXECUTION_LEDGER"
            changed = True

    if changed:
        LANES_PATH.write_text(
            json.dumps(lanes_doc, indent=2) + "\n",
            encoding="utf-8",
        )
        print("ACTIVE_LANES.json updated from verified execution ledger")
    else:
        print("ACTIVE_LANES.json already consistent with verified execution ledger")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
