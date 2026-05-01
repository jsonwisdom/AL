#!/usr/bin/env python3
import json, hashlib, glob
from pathlib import Path

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def read_leaf(path):
    data = Path(path).read_bytes()
    return {
        "path": path,
        "hash": sha256_hex(data)
    }

def parent_hash(left, right):
    return sha256_hex((left + right).encode())

paths = sorted(glob.glob("_truth/courts/leaf*/verdict_*.canonical.json"))
if not paths:
    raise SystemExit("NO_VERDICT_FILES")

leaves = [read_leaf(p) for p in paths]
level = [x["hash"] for x in leaves]
proofs = {x["hash"]: [] for x in leaves}

while len(level) > 1:
    next_level = []
    # If odd number of nodes, duplicate the last node
    current_level_hashes = list(level)
    if len(current_level_hashes) % 2 == 1:
        current_level_hashes.append(current_level_hashes[-1])

    for i in range(0, len(current_level_hashes), 2):
        left, right = current_level_hashes[i], current_level_hashes[i+1]
        parent = parent_hash(left, right)
        next_level.append(parent)

        # In a real Merkle tree with proofs, we track the original leaf index.
        # This simplification works for unique hashes.
        for leaf_hash, path_list in proofs.items():
            # If the leaf was in the subtree under level[i]
            # This is complex to track correctly in a loop like this without indices.
            pass

    # Simplified tracking for current small set:
    level = next_level

# Re-implementing with index tracking for correct proofs
def build_proofs(leaves):
    level = [leaf["hash"] for leaf in leaves]
    n = len(level)
    proofs = [[] for _ in range(n)]
    
    while len(level) > 1:
        next_level = []
        if len(level) % 2 == 1:
            level.append(level[-1])
        
        for i in range(0, len(level), 2):
            left, right = level[i], level[i+1]
            parent = parent_hash(left, right)
            next_level.append(parent)
            
            # For each leaf index in the left subtree, add right as sibling
            for j in range(i * (n // len(level)), min((i + 1) * (n // len(level)), n)):
                 proofs[j].append({"direction": "right", "sibling": right})
            # For each leaf index in the right subtree, add left as sibling
            for j in range((i + 1) * (n // len(level)), min((i + 2) * (n // len(level)), n)):
                 proofs[j].append({"direction": "left", "sibling": left})
        level = next_level
    return level[0], proofs

root, leaf_proofs = build_proofs(leaves)

out = {
    "type": "court_merkle_inclusion_proofs",
    "hash_function": "sha256",
    "parent_rule": "sha256(left_hex + right_hex)",
    "leaf_count": len(leaves),
    "root": root,
    "leaves": [
        {
            "path": leaves[i]["path"],
            "leaf_hash": leaves[i]["hash"],
            "proof": leaf_proofs[i]
        }
        for i in range(len(leaves))
    ]
}

Path("_truth/merkle").mkdir(parents=True, exist_ok=True)
Path("_truth/merkle/court_inclusion_proofs.json").write_text(json.dumps(out, indent=2) + "\n")
Path("_truth/merkle/court_inclusion_proofs.canonical.json").write_text(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")

print("MERKLE_ROOT", root)
print("LEAF_COUNT", len(leaves))
print("WROTE _truth/merkle/court_inclusion_proofs.canonical.json")
