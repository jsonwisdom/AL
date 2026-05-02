#!/usr/bin/env python3
import json
import hashlib
import sys
from pathlib import Path

BATCH_NUM = sys.argv[1] if len(sys.argv) > 1 else "001"

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def merkle_root(hashes):
    if not hashes:
        return hashlib.sha256(b"").hexdigest()
    level = sorted(hashes)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        nxt = []
        for i in range(0, len(level), 2):
            a, b = sorted([level[i], level[i+1]])
            nxt.append(hashlib.sha256(bytes.fromhex(a)+bytes.fromhex(b)).hexdigest())
        level = sorted(nxt)
    return level[0]

# Load all leaves (all KB_* directories)
leaves = sorted(Path("_truth/leaves").glob("KB_*/receipt.canonical.json"))
items = []
for p in leaves:
    data = json.loads(p.read_text())
    h = sha256_bytes(canonical(data).encode())
    items.append({
        "leaf_id": data["leaf_id"],
        "path": str(p),
        "status": data.get("status",""),
        "anchor_allowed": str(bool(data.get("anchor_allowed", False))).lower(),
        "receipt_hash": h
    })
items.sort(key=lambda x: (x["leaf_id"], x["path"]))
root = merkle_root([i["receipt_hash"] for i in items])
core = {
    "batch_type": "knowledge_broker_batch",
    "policy": "knowledge_broker_policy_v1",
    "ready_count": len(items),
    "blocked_count": 0,
    "items": items,
    "blocked_items": [],
    "merkle_root": root
}
batch_hash = sha256_bytes(canonical(core).encode())
manifest = {
    "batch_id": f"kb_batch_{batch_hash[:16]}",
    "batch_hash": batch_hash,
    **core
}
out = Path(f"_truth/batches/kb_batch_{BATCH_NUM}.json")
out.write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
print(f"MERKLE_ROOT = {root}")
print(f"READY = {len(items)}")
print(f"OUTPUT = {out}")
