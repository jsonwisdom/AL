#!/usr/bin/env python3
"""
GBRS Agent Capability Projection Stub

Pi_AGT_CAPS(TS_c) -> effective agent capabilities

This module derives effective agent capabilities from canonical grant/revoke
receipts. It is intentionally read-only and deterministic.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


AgentCapabilities = Dict[str, List[str]]


def project_agent_caps(ts_c: Dict[str, Any], receipts_dir: Path) -> AgentCapabilities:
    """
    Pi_AGT_CAPS(TS_c) -> effective agent capabilities.

    Deterministic Agent Capability projection stub.
    Resolves effective capabilities based on grant/revoke lineage.

    Input:
      - ts_c: canonical index.json as a dict
      - receipts_dir: Path to canonical/receipts/

    Output:
      - {
          "agent_A": ["tool.alms.receipt.verify", ...],
          "agent_B": []
        }
    """

    # Map: agent_id -> tool_id -> grant_receipt_id
    grants: Dict[str, Dict[str, str]] = {}

    # Set of grant receipt_ids that have been revoked/superseded
    revoked_grants = set()

    for receipt_name in ts_c.get("receipts", []):
        path = receipts_dir / receipt_name
        try:
            with open(path, "r", encoding="utf-8") as f:
                receipt = json.load(f)
        except Exception:
            # MVV behavior: unreadable receipt is ignored by this projection stub.
            # The outer verifier may later choose to fail closed on missing receipts.
            continue

        kind = receipt.get("kind")

        if kind == "agent_capability_grant":
            agent = receipt.get("agent_id")
            tool = receipt.get("capability_id")
            receipt_id = receipt.get("receipt_id")
            if not agent or not tool or not receipt_id:
                continue
            grants.setdefault(agent, {})[tool] = receipt_id

        elif kind in ("agent_capability_revoke", "capability_revocation"):
            # T005 uses agent_capability_revoke with successor_of, but this also
            # supports an explicit revoked_receipt_id form.
            target = receipt.get("successor_of") or receipt.get("revoked_receipt_id")
            if target:
                revoked_grants.add(target)

    # Compute effective capabilities: grants that are not revoked/superseded.
    effective_caps: AgentCapabilities = {}
    for agent, tools in sorted(grants.items()):
        active = []
        for tool_id, grant_receipt_id in sorted(tools.items()):
            if grant_receipt_id not in revoked_grants:
                active.append(tool_id)
        effective_caps[agent] = active

    return effective_caps


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Project GBRS effective agent capabilities")
    parser.add_argument("--index", required=True, help="Path to canonical/index.json")
    parser.add_argument("--receipts-dir", required=True, help="Path to canonical/receipts")
    args = parser.parse_args()

    with open(args.index, "r", encoding="utf-8") as f:
        ts_c = json.load(f)

    result = project_agent_caps(ts_c, Path(args.receipts_dir))
    print(json.dumps(result, indent=2, sort_keys=True))
