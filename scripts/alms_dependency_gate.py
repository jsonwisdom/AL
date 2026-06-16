#!/usr/bin/env python3
"""ALMS dependency gate.

Enforces depends_on chains in alms/version_registry.json.
If an entry is REPLAY_PASSED, every dependency must exist and also be REPLAY_PASSED.
If a dependency is missing or blocked, the dependent entry cannot promote.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

REGISTRY_PATH = Path("alms/version_registry.json")
TERMINAL_GOOD = "REPLAY_PASSED"


def main() -> int:
    if not REGISTRY_PATH.exists():
        print(f"DEPENDENCY_GATE_FAIL missing registry: {REGISTRY_PATH}")
        return 1

    registry: Dict[str, Any] = json.loads(REGISTRY_PATH.read_text())
    entries = registry.get("entries", [])
    by_id = {entry.get("id"): entry for entry in entries}
    violations = []

    for entry in entries:
        entry_id = entry.get("id")
        state = entry.get("state")
        deps = entry.get("depends_on", []) or []

        if not isinstance(deps, list):
            violations.append(f"DEPENDENCY_LIST_INVALID {entry_id}")
            continue

        for dep_id in deps:
            dep = by_id.get(dep_id)
            if dep is None:
                violations.append(f"DEPENDENCY_MISSING {entry_id} depends_on {dep_id}")
                continue

            dep_state = dep.get("state")

            if state == TERMINAL_GOOD and dep_state != TERMINAL_GOOD:
                violations.append(
                    f"DEPENDENCY_NOT_PASSED {entry_id}={state} requires {dep_id}={dep_state}"
                )

            if dep_state in {"BLOCKED", "DEPRECATED"} and state not in {"BLOCKED", "DEPRECATED"}:
                violations.append(
                    f"DEPENDENCY_BAD_STATE {entry_id}={state} depends_on {dep_id}={dep_state}"
                )

    if violations:
        print("DEPENDENCY_GATE_FAIL")
        for violation in violations:
            print(violation)
        return 1

    print("DEPENDENCY_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
