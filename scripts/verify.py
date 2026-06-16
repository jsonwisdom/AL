#!/usr/bin/env python3
"""
Compatibility verifier wrapper for ALMS / legacy automation.

Why this exists:
- Older evidence and CI commands call: python3 scripts/verify.py
- The canonical ALMS replay verifier currently lives at: scripts/alms_verify.py
- alms_verify.py requires an input packet, while legacy health checks may call verify.py with no args.

Behavior:
- No args: emit a neutral health-check JSON and exit 0.
- --debug / --force-output with no input: accepted for legacy callers, still emits health JSON.
- With args: delegate to scripts/alms_verify.py unchanged.

Authority remains false. This wrapper does not interpret evidence.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def emit_health() -> int:
    payload = {
        "component": "scripts/verify.py",
        "role": "legacy_compatibility_wrapper",
        "canonical_verifier": "scripts/alms_verify.py",
        "checked_at_utc": utc_now(),
        "status": "HEALTH_CHECK_ONLY",
        "authority": False,
        "verification_state": "WRAPPER_PRESENT_NOT_INTERPRETED",
        "note": "No input packet supplied; wrapper presence confirmed. Use scripts/alms_verify.py with a fixture or replay JSON packet for replay verification.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    canonical = repo_root / "scripts" / "alms_verify.py"

    passthrough_args = [a for a in argv if a not in {"--debug", "--force-output"}]

    if not canonical.exists():
        print(json.dumps({
            "component": "scripts/verify.py",
            "status": "FAIL",
            "error": "canonical verifier missing",
            "expected_path": str(canonical),
            "authority": False,
            "verification_state": "WRAPPER_FAILED_NOT_INTERPRETED",
        }, indent=2, sort_keys=True), file=sys.stderr)
        return 1

    if len(passthrough_args) == 0:
        return emit_health()

    cmd = [sys.executable, str(canonical), *passthrough_args]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
