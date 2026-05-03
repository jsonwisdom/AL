#!/usr/bin/env python3
"""ALMS registry diff gate.

Validates version registry transitions against the previous git revision.
Blocks illegal jumps and illegal state transitions.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

REGISTRY_PATH = Path("alms/version_registry.json")
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

ALLOWED_STATE_TRANSITIONS = {
    "DRAFT": {"LOCKED", "BLOCKED", "DEPRECATED"},
    "LOCKED": {"REPLAY_REQUIRED", "BLOCKED", "DEPRECATED"},
    "REPLAY_REQUIRED": {"REPLAY_PASSED", "BLOCKED", "DEPRECATED"},
    "REPLAY_PASSED": {"REPLAY_REQUIRED", "DEPRECATED"},
    "BLOCKED": {"DRAFT", "LOCKED", "REPLAY_REQUIRED", "DEPRECATED"},
    "DEPRECATED": set(),
}


def load_json_text(text: str) -> Dict[str, Any]:
    return json.loads(text)


def load_current() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise SystemExit("REGISTRY_MISSING")
    return json.loads(REGISTRY_PATH.read_text())


def load_previous() -> Optional[Dict[str, Any]]:
    try:
        proc = subprocess.run(
            ["git", "show", f"HEAD~1:{REGISTRY_PATH.as_posix()}"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return None

    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return load_json_text(proc.stdout)


def entry_map(registry: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {entry["id"]: entry for entry in registry.get("entries", [])}


def parse_semver(version: str) -> Tuple[int, int, int]:
    match = SEMVER_RE.match(version or "")
    if not match:
        raise ValueError(f"BAD_SEMVER {version}")
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def semver_jump_ok(old: str, new: str) -> bool:
    old_v = parse_semver(old)
    new_v = parse_semver(new)
    if new_v == old_v:
        return True
    # Only one segment may increase by exactly 1; lower segments reset to 0.
    if new_v[0] == old_v[0] + 1 and new_v[1] == 0 and new_v[2] == 0:
        return True
    if new_v[0] == old_v[0] and new_v[1] == old_v[1] + 1 and new_v[2] == 0:
        return True
    if new_v[0] == old_v[0] and new_v[1] == old_v[1] and new_v[2] == old_v[2] + 1:
        return True
    return False


def main() -> int:
    current = load_current()
    previous = load_previous()

    if previous is None:
        print("REGISTRY_DIFF_GATE_BOOTSTRAP_PASS no previous registry")
        return 0

    old_entries = entry_map(previous)
    new_entries = entry_map(current)
    violations = []

    for entry_id, new_entry in new_entries.items():
        old_entry = old_entries.get(entry_id)
        if old_entry is None:
            # New entries are allowed only in DRAFT/LOCKED/REPLAY_REQUIRED.
            if new_entry.get("state") not in {"DRAFT", "LOCKED", "REPLAY_REQUIRED"}:
                violations.append(f"NEW_ENTRY_ILLEGAL_STATE {entry_id} {new_entry.get('state')}")
            continue

        old_state = old_entry.get("state")
        new_state = new_entry.get("state")
        old_version = old_entry.get("version")
        new_version = new_entry.get("version")

        if new_state != old_state:
            allowed = ALLOWED_STATE_TRANSITIONS.get(old_state, set())
            if new_state not in allowed:
                violations.append(f"ILLEGAL_STATE_TRANSITION {entry_id} {old_state}->{new_state}")

        try:
            if not semver_jump_ok(old_version, new_version):
                violations.append(f"ILLEGAL_VERSION_JUMP {entry_id} {old_version}->{new_version}")
        except ValueError as exc:
            violations.append(str(exc))

        if new_state == "REPLAY_PASSED" and not str(new_entry.get("hash", "")).startswith("sha256:"):
            violations.append(f"REPLAY_PASSED_WITHOUT_HASH {entry_id}")

    for entry_id in old_entries:
        if entry_id not in new_entries:
            violations.append(f"ENTRY_REMOVED {entry_id}")

    if violations:
        print("REGISTRY_DIFF_GATE_FAIL")
        for violation in violations:
            print(violation)
        return 1

    print("REGISTRY_DIFF_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
