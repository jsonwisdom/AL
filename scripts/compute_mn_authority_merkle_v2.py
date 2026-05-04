#!/usr/bin/env python3
"""
Compute TRUE_MERKLE_V2 for MN authority leaves.

Rules:
- Input: JSONL, one object per line, exact order preserved.
- Leaf digest: sha256("LEAF:" + label + ":" + hash)
- Node digest: sha256("NODE:" + left + right)
- Odd leaf/node rule: ODD_LEAF_CARRY_FORWARD
- No sorting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

RULE = "TRUE_MERKLE_V2"
ODD_RULE = "ODD_LEAF_CARRY_FORWARD"
LEAF_PREFIX = "LEAF:"
NODE_PREFIX = "NODE:"


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def read_leaves(path: Path) -> list[dict[str, str]]:
    leaves: list[dict[str, str]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        obj = json.loads(raw)
        if sorted(obj.keys()) != ["hash", "label"]:
            raise SystemExit(f"line {line_no}: expected only label/hash fields")
        label = obj["label"]
        value = obj["hash"]
        if not isinstance(label, str) or not isinstance(value, str):
            raise SystemExit(f"line {line_no}: label/hash must be strings")
        if len(value) != 64 or value.lower() != value or any(c not in "0123456789abcdef" for c in value):
            raise SystemExit(f"line {line_no}: hash must be lowercase 64-char hex")
        leaves.append({"label": label, "hash": value})
    if not leaves:
        raise SystemExit("no leaves found")
    return leaves


def leaf_digest(leaf: dict[str, str]) -> str:
    return sha256_hex(f"{LEAF_PREFIX}{leaf['label']}:{leaf['hash']}")


def node_digest(left: str, right: str) -> str:
    return sha256_hex(f"{NODE_PREFIX}{left}{right}")


def build_tree(leaf_rows: list[dict[str, str]]) -> dict[str, Any]:
    level0 = []
    for index, leaf in enumerate(leaf_rows):
        digest = leaf_digest(leaf)
        level0.append({"index": index, "label": leaf["label"], "input_hash": leaf["hash"], "hash": digest})

    levels: list[list[dict[str, Any]]] = [level0]
    current = level0
    while len(current) > 1:
        nxt: list[dict[str, Any]] = []
        i = 0
        while i < len(current):
            left = current[i]
            if i + 1 < len(current):
                right = current[i + 1]
                digest = node_digest(left["hash"], right["hash"])
                nxt.append({"index": len(nxt), "left": left["hash"], "right": right["hash"], "hash": digest})
                i += 2
            else:
                nxt.append({"index": len(nxt), "carry": left["hash"], "hash": left["hash"]})
                i += 1
        levels.append(nxt)
        current = nxt
    return {"root": levels[-1][0]["hash"], "levels": levels}


def proof_for_label(tree: dict[str, Any], label: str) -> dict[str, Any]:
    levels = tree["levels"]
    idx = None
    leaf = None
    for row in levels[0]:
        if row.get("label") == label:
            idx = row["index"]
            leaf = row
            break
    if idx is None or leaf is None:
        raise SystemExit(f"label not found: {label}")

    path = []
    current_index = idx
    for level_no, level in enumerate(levels[:-1]):
        if current_index % 2 == 0:
            sib_index = current_index + 1
            if sib_index < len(level):
                path.append({"level": level_no, "position": "right", "hash": level[sib_index]["hash"]})
        else:
            sib_index = current_index - 1
            path.append({"level": level_no, "position": "left", "hash": level[sib_index]["hash"]})
        current_index //= 2

    return {
        "rule": RULE,
        "odd_leaf_rule": ODD_RULE,
        "leaf_label": label,
        "leaf_input_hash": leaf["input_hash"],
        "leaf_hash": leaf["hash"],
        "path": path,
        "root": tree["root"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--leaves", default="_truth/merkle/mn_authority_leaves_v2.jsonl")
    parser.add_argument("--manifest", default="_truth/merkle/mn_authority_manifest_v2.json")
    parser.add_argument("--root", default="_truth/merkle/mn_authority_root_v2.txt")
    parser.add_argument("--proof", default="_truth/merkle/proofs/mn_0001_fixture.proof.json")
    parser.add_argument("--proof-label", default="mn_0001_fixture")
    args = parser.parse_args()

    leaves_path = Path(args.leaves)
    leaves = read_leaves(leaves_path)
    tree = build_tree(leaves)
    proof = proof_for_label(tree, args.proof_label)

    manifest = {
        "version": "2",
        "rule": RULE,
        "odd_leaf_rule": ODD_RULE,
        "leaf_prefix": LEAF_PREFIX,
        "node_prefix": NODE_PREFIX,
        "leaf_source": str(leaves_path),
        "leaf_count": len(leaves),
        "leaves": leaves,
        "levels": tree["levels"],
        "root": tree["root"],
    }

    Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    Path(args.proof).parent.mkdir(parents=True, exist_ok=True)
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.root).write_text(tree["root"] + "\n", encoding="utf-8")
    Path(args.proof).write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(tree["root"])


if __name__ == "__main__":
    main()
