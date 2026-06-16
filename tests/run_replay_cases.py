#!/usr/bin/env python3
"""
Minimal constitutional replay harness for PR #85.

Enforces:
- exactly one TRACE_CLOSED event
- terminal closure position
- deterministic trace hash presence
- PASS/FAIL expected verdict alignment
- immutable sealed transcript semantics
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERIFY = ROOT / "scripts" / "alms_verify.py"

CASES = [
    {
        "name": "PASS_001",
        "fixture": ROOT / "tests" / "fixtures" / "pass_valid_fixture" / "fixture.json",
        "expected": "PASS",
    },
    {
        "name": "FAIL_001",
        "fixture": ROOT / "tests" / "fixtures" / "fail_digest_mismatch" / "fixture.json",
        "expected": "FAIL",
    },
]


def run_case(case: dict) -> dict:
    result = subprocess.run(
        [sys.executable, str(VERIFY), str(case["fixture"])],
        check=False,
        capture_output=True,
        text=True,
    )

    if not result.stdout.strip():
        raise RuntimeError(f"{case['name']}: verifier produced no report")

    report = json.loads(result.stdout)

    verdict = report["verdict"]["state"]
    if verdict != case["expected"]:
        raise RuntimeError(
            f"{case['name']}: expected verdict {case['expected']} but got {verdict}"
        )

    trace = report["replay_trace"]
    closure_events = [t for t in trace if t["name"] == "TRACE_CLOSED"]

    if len(closure_events) != 1:
        raise RuntimeError(
            f"{case['name']}: expected exactly one TRACE_CLOSED event"
        )

    if trace[-1]["name"] != "TRACE_CLOSED":
        raise RuntimeError(
            f"{case['name']}: TRACE_CLOSED is not terminal"
        )

    closure = closure_events[0]

    if not closure.get("trace_hash"):
        raise RuntimeError(
            f"{case['name']}: TRACE_CLOSED missing deterministic trace hash"
        )

    if closure.get("verdict") != verdict:
        raise RuntimeError(
            f"{case['name']}: closure verdict mismatch"
        )

    return {
        "case": case["name"],
        "verdict": verdict,
        "trace_hash": closure["trace_hash"],
        "report_hash": report["hash"]["digest"],
    }


if __name__ == "__main__":
    outputs = [run_case(case) for case in CASES]
    print(json.dumps(outputs, sort_keys=True, indent=2))
