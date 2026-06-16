#!/usr/bin/env python3
import json, hashlib, glob
from pathlib import Path

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_pair(left_hex, right_hex):
    return sha256_hex(bytes.fromhex(left_hex) + bytes.fromhex(right_hex))

def read_leaf(path):
    data = Path(path).read_bytes()
    return {
        "path": path,
        "hash": sha256_hex(data)
    }

def build_proofs(leaves):
    level = [leaf["hash"] for leaf in leaves]
    n = len(level)
    # proofs[i] stores siblings for leaf at index i
    proofs = [[] for _ in range(n)]
    
    # map leaf indices to their current index in the 'level' array
    indices = list(range(n))
    
    while len(level) > 1:
        next_level = []
        next_indices = []
        
        # If odd, duplicate last element
        work_level = list(level)
        work_indices = list(indices)
        if len(work_level) % 2 == 1:
            work_level.append(work_level[-1])
            work_indices.append(None) # Shadow index
            
        for i in range(0, len(work_level), 2):
            left_h = work_level[i]
            right_h = work_level[i+1]
            parent = sha256_pair(left_h, right_h)
            next_level.append(parent)
            
            # Update proofs for leaves in left subtree
            # work_indices[i] might be a list of original leaf indices
            # Let's use a more robust tracking
            pass
        
        # Simplified robust tracking:
        # Each 'node' in current level represents a range of original leaves.
        # But duplication makes it tricky.
        break

    # Standard Merkle Tree implementation (fixed size powers of 2 or duplication)
    # Let's use the simplest reliable approach for proofs
    return level[0], proofs

# Re-implementing correctly:
def build_tree_and_proofs(leaves):
    current_hashes = [l["hash"] for l in leaves]
    num_leaves = len(current_hashes)
    proofs = [[] for _ in range(num_leaves)]
    
    # Tree nodes at each level: nodes[level_idx] = [hash0, hash1, ...]
    nodes = [current_hashes]
    
    while len(nodes[-1]) > 1:
        last_level = nodes[-1]
        next_level = []
        for i in range(0, len(last_level), 2):
            left = last_level[i]
            right = last_level[i+1] if i+1 < len(last_level) else left
            next_level.append(sha256_pair(left, right))
        nodes.append(next_level)
    
    root = nodes[-1][0]
    
    # Generate proofs for each leaf
    for i in range(num_leaves):
        idx = i
        for level_idx in range(len(nodes) - 1):
            level = nodes[level_idx]
            if idx % 2 == 0:
                # Leaf is a left child
                if idx + 1 < len(level):
                    sibling = level[idx + 1]
                else:
                    sibling = level[idx] # Duplicated self
                proofs[i].append({"direction": "right", "sibling": sibling})
            else:
                # Leaf is a right child
                sibling = level[idx - 1]
                proofs[i].append({"direction": "left", "sibling": sibling})
            idx //= 2
            
    return root, proofs

paths = sorted(glob.glob("_truth/courts/leaf*/verdict_*.canonical.json"))
leaves = [read_leaf(p) for p in paths]
root, leaf_proofs = build_tree_and_proofs(leaves)

out = {
    "type": "court_merkle_inclusion_proofs",
    "hash_function": "sha256",
    "parent_rule": "sha256(left_bytes + right_bytes)",
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
