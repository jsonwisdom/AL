#!/usr/bin/env python3
"""
Namespace Guard v1

Constitutional boundary:
  - Executes BEFORE CBRE VM
  - Executes BEFORE manifest verification
  - Executes BEFORE pending aggregation
  - Rejects protected namespace violations structurally
  - Fails closed on unknown namespaces
"""

from __future__ import annotations

import fnmatch
import json
from pathlib import Path
from typing import Any

POLICY_PATH = Path("namespace/namespace_policy_v1.json")

ALLOW = "ALLOW"
LOCAL_ONLY = "LOCAL_ONLY"
QUARANTINE = "QUARANTINE"

PASS = "PASS"
NAMESPACE_VIOLATION = "NAMESPACE_VIOLATION"
QUARANTINED = "QUARANTINED"



def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))



def match_namespace(asset_id: str, policy: dict[str, Any]) -> dict[str, Any] | None:
    for namespace in policy["protected_namespaces"]:
        if fnmatch.fnmatch(asset_id, namespace["pattern"]):
            return namespace
    return None



def evaluate_claim(
    asset_id: str,
    claim_origin: str,
    local_branch_id: str,
    policy: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    namespace = match_namespace(asset_id, policy)

    if namespace is None:
        return (
            QUARANTINED,
            {
                "reason": "UNRECOGNIZED_NAMESPACE",
                "default_rule": policy["default_rule"],
            },
        )

    mode = namespace["protection_mode"]

    if mode == ALLOW:
        return (
            PASS,
            {
                "namespace_id": namespace["namespace_id"],
                "pattern": namespace["pattern"],
                "protection_mode": mode,
            },
        )

    if mode == LOCAL_ONLY:
        if claim_origin != local_branch_id:
            return (
                NAMESPACE_VIOLATION,
                {
                    "namespace_id": namespace["namespace_id"],
                    "pattern": namespace["pattern"],
                    "reason": "LOCAL_ONLY_NAMESPACE",
                    "alert": namespace["alert_on_violation"],
                },
            )

        return (
            PASS,
            {
                "namespace_id": namespace["namespace_id"],
                "pattern": namespace["pattern"],
                "protection_mode": mode,
            },
        )

    return (
        QUARANTINED,
        {
            "reason": "UNKNOWN_PROTECTION_MODE",
            "mode": mode,
        },
    )



def main() -> int:
    policy = load_policy()
    print(json.dumps(policy, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
