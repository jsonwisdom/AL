#!/usr/bin/env python3
"""ALMS Merkle root gate.

Computes a deterministic Merkle root over ALMS version registry entries.

Leaf rule:
  leaf = sha256(id + "\n" + version + "\n" + state + "\n" + artifact_path + "\n" + hash)

Tree rule:
  - sort leaves by id lexicographically
  - if one leaf, root = leaf
  - otherwise pairwise hash left + right as raw hex bytes
  - if odd leaf count, duplicate last leaf

Writes alms/merkle/version_root.json.
If an existing committed root exists and differs, updates it and exits 0.
This gate is an observation + publication gate, not a blocker for root changes.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

REGISTRY_PATH = Path("alms/version_registry.json")
ROOT_PATH = Path("alms/merkle/version_root.json")
RULE_ID = "ALMS_VERSION_MERKLE_RULE_V1"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_registry():
    return json.loads(REGISTRY_PATH.read_text())


def leaf_hash(entry) -> Tuple[str, str]:
    entry_id = entry["id"]
    material = "\n".join(
        [
            entry["id"],
            entry["version"],
            entry["state"],
            entry["artifact_path"],
            entry["hash"],
        ]
    ).encode("utf-8")
    return entry_id, sha256_hex(material)


def merkle_root(leaves: List[str]) -> str:
    if not leaves:
        return sha256_hex(b"")
    level = leaves[:]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(sha256_hex(bytes.fromhex(left) + bytes.fromhex(right)))
        level = nxt
    return level[0]


def main() -> int:
    if not REGISTRY_PATH.exists():
        print(f"MERKLE_ROOT_GATE_FAIL missing registry {REGISTRY_PATH}")
        return 1

    registry = load_registry()
    entries = registry.get("entries", [])
    leaves = [leaf_hash(entry) for entry in entries]
    leaves.sort(key=lambda item: item[0])
    root = merkle_root([leaf for _, leaf in leaves])

    report = {
        "rule_id": RULE_ID,
        "registry_path": str(REGISTRY_PATH),
        "leaf_count": len(leaves),
        "leaves": [{"id": entry_id, "leaf_hash": f"sha256:{leaf}"} for entry_id, leaf in leaves],
        "merkle_root": f"sha256:{root}",
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }

    ROOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    previous = None
    if ROOT_PATH.exists():
        try:
            previous = json.loads(ROOT_PATH.read_text()).get("merkle_root")
        except Exception:
            previous = None

    ROOT_PATH.write_text(json.dumps(report, indent=2) + "\n")

    if previous and previous != report["merkle_root"]:
        print(f"MERKLE_ROOT_UPDATED {previous} -> {report['merkle_root']}")
    else:
        print(f"MERKLE_ROOT_PASS {report['merkle_root']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
