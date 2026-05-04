#!/usr/bin/env python3
"""
Verify TRUE_MERKLE_V2 inclusion proof.

Rules:
- Leaf digest: sha256("LEAF:" + label + ":" + input_hash)
- Node digest: sha256("NODE:" + left + right)
- Proof path positions are sibling positions relative to current node.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RULE = "TRUE_MERKLE_V2"
LEAF_PREFIX = "LEAF:"
NODE_PREFIX = "NODE:"


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def leaf_digest(label: str, input_hash: str) -> str:
    return sha256_hex(f"{LEAF_PREFIX}{label}:{input_hash}")


def node_digest(left: str, right: str) -> str:
    return sha256_hex(f"{NODE_PREFIX}{left}{right}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", default="_truth/merkle/proofs/mn_0001_fixture.proof.json")
    args = parser.parse_args()

    proof = json.loads(Path(args.proof).read_text(encoding="utf-8"))
    if proof.get("rule") != RULE:
        raise SystemExit(f"wrong rule: {proof.get('rule')}")

    label = proof["leaf_label"]
    input_hash = proof["leaf_input_hash"]
    computed = leaf_digest(label, input_hash)
    if computed != proof["leaf_hash"]:
        raise SystemExit("leaf hash mismatch")

    for step in proof["path"]:
        sibling = step["hash"]
        position = step["position"]
        if position == "left":
            computed = node_digest(sibling, computed)
        elif position == "right":
            computed = node_digest(computed, sibling)
        else:
            raise SystemExit(f"invalid proof position: {position}")

    if computed != proof["root"]:
        raise SystemExit(f"proof failed: {computed} != {proof['root']}")

    print(json.dumps({"status": "VERIFIED", "root": computed, "leaf_label": label}, sort_keys=True))


if __name__ == "__main__":
    main()
