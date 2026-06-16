#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

FIXTURE_DIR = Path("agents/track020/fixtures")
VERIFIER = Path("agents/track020/verifier/verify_track020_replay_state.py")


def run_fixture(path: Path):
    proc = subprocess.run(
        ["python3", str(VERIFIER), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.stdout.strip(), f"No output for fixture {path}"
    out = json.loads(proc.stdout)

    fixture = json.loads(path.read_text())

    assert out["classification"] == fixture["expected_classification"], (
        f"classification mismatch for {path.name}: "
        f"expected {fixture['expected_classification']} got {out['classification']}"
    )

    assert out["verdict_code"] == fixture["expected_verdict_code"], (
        f"verdict mismatch for {path.name}: "
        f"expected {fixture['expected_verdict_code']} got {out['verdict_code']}"
    )


if __name__ == "__main__":
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    assert fixtures, "No fixtures found"

    for fixture in fixtures:
        run_fixture(fixture)

    print(json.dumps({
        "artifact": "TRACK_020_REPLAY_TEST_RESULTS_V1",
        "fixtures": [f.name for f in fixtures],
        "verdict": "PASS"
    }, indent=2))
