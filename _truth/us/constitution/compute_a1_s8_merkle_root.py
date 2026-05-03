#!/usr/bin/env python3
"""
Compute Article I, Section 8 Merkle root from constitution_span_audit.jsonl.

Rule: ALMS_GLOBAL_MERKLE_RULE_V1
- Require exactly USC-A1-S8-C1 through USC-A1-S8-C18
- Require every record status == OK
- Sort by numeric clause index
- Leaf hash = SHA256(id + ':' + sha256)
- Pairwise parent = SHA256(left_raw_digest || right_raw_digest)
- Odd final leaf at a level is promoted unchanged
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INFILE = ROOT / "constitution_span_audit.jsonl"
OUTFILE = ROOT / "a1_s8_merkle_manifest.json"
RULE_ID = "ALMS_GLOBAL_MERKLE_RULE_V1"

def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def clause_index(identifier: str) -> int:
    match = re.fullmatch(r"USC-A1-S8-C(\d+)", identifier)
    if not match:
        raise ValueError(f"bad id: {identifier}")
    return int(match.group(1))

def main() -> int:
    records = [json.loads(line) for line in INFILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(records) != 18:
        raise SystemExit(f"BLOCKED: expected 18 leaves, got {len(records)}")
    records.sort(key=lambda record: clause_index(record["id"]))
    expected = [f"USC-A1-S8-C{i}" for i in range(1, 19)]
    actual = [record["id"] for record in records]
    if actual != expected:
        raise SystemExit(f"BLOCKED: expected ids {expected}, got {actual}")
    bad = [record for record in records if record.get("status") != "OK"]
    if bad:
        raise SystemExit(f"BLOCKED: non-OK leaves present: {bad}")

    leaves = []
    for record in records:
        material = f"{record['id']}:{record['sha256']}".encode("utf-8")
        leaf = sha256_bytes(material)
        leaves.append({
            "id": record["id"],
            "span_sha256": record["sha256"],
            "leaf_hash": leaf.hex(),
        })

    levels = [[bytes.fromhex(leaf["leaf_hash"]) for leaf in leaves]]
    while len(levels[-1]) > 1:
        current = levels[-1]
        nxt = []
        for i in range(0, len(current), 2):
            if i + 1 < len(current):
                nxt.append(sha256_bytes(current[i] + current[i + 1]))
            else:
                nxt.append(current[i])
        levels.append(nxt)

    manifest = {
        "artifact": "USC_A1_S8_MERKLE_MANIFEST",
        "status": "ROOT_COMPUTED",
        "rule_id": RULE_ID,
        "input": "_truth/us/constitution/constitution_span_audit.jsonl",
        "leaf_count": 18,
        "root_sha256": levels[-1][0].hex(),
        "leaves": leaves,
        "levels": [[node.hex() for node in level] for level in levels],
    }
    OUTFILE.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest["root_sha256"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
