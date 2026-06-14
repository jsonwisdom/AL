#!/usr/bin/env python3
"""
Deterministic verifier for FEDERAL_AI_TESTING_ROOT_LANE_V1.

No timestamps. No network calls. No wallet actions.
This verifier checks the docket hash and emits a stable JSON receipt.
"""

import hashlib
import json
import sys
from pathlib import Path

DOCKET_PATH = Path("docs/FEDERAL_AI_TESTING_ROOT_LANE_V1.md")
EXPECTED_DOCKET_SHA256 = "d15496d9f06073d76f449639038b51c93bb57a56ce0469bbf3738bb29b60d449"
VERIFIER_VERSION = "verify_federal_ai_root_lane.py:v1"
DOCKET_ID = "FEDERAL_AI_TESTING_ROOT_LANE_V1"

LANES = {
    "FED-AI-001": "White House AI action/framework lane",
    "FED-AI-002": "CAISI / federal AI testing unit lane",
    "FED-AI-003": "DOJ AI litigation / enforcement lane",
    "FED-AI-004": "Pam Bondi / named official authority graph lane",
    "FED-AI-005": "Federal preemption of state AI laws lane",
    "FED-AI-006": "National-security AI / autonomous systems lane",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not DOCKET_PATH.exists():
        receipt = {
            "docket_id": DOCKET_ID,
            "verifier_version": VERIFIER_VERSION,
            "overall": "RED",
            "no_fake_green": True,
            "error": f"MISSING_DOCKET: {DOCKET_PATH}",
        }
        print(json.dumps(receipt, sort_keys=True, indent=2))
        return 1

    actual = sha256_file(DOCKET_PATH)
    state_match = actual == EXPECTED_DOCKET_SHA256
    overall = "GREEN" if state_match else "RED"

    receipt = {
        "docket_id": DOCKET_ID,
        "verifier_version": VERIFIER_VERSION,
        "docket_path": str(DOCKET_PATH),
        "expected_docket_sha256": EXPECTED_DOCKET_SHA256,
        "actual_docket_sha256": actual,
        "state_match": state_match,
        "lanes": {lane: {"description": desc, "status": overall} for lane, desc in LANES.items()},
        "overall": overall,
        "no_fake_green": True,
    }
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0 if state_match else 1


if __name__ == "__main__":
    sys.exit(main())
