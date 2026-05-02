#!/usr/bin/env python3
"""
Track 020 - Aggregated Batch Root
Deterministic, domain-separated Merkle root over all batch roots
Usage: ./scripts/aggregate_batch_roots.py
"""

import hashlib
import json
import sys
from pathlib import Path

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()

def normalize_root(root):
    """Handle 0x prefix safely + validate 64 hex chars"""
    root = root.lower().strip()
    root = root.replace("0x", "")
    if len(root) != 64 or not all(c in "0123456789abcdef" for c in root):
        raise ValueError(f"Invalid root (must be 64 hex chars): {root}")
    return root

def domain_separate(batch_root_hex):
    """Domain separation: 0x01 || batch_root_bytes"""
    normalized = normalize_root(batch_root_hex)
    batch_root_bytes = bytes.fromhex(normalized)
    separator = b'\x01'
    return hashlib.sha256(separator + batch_root_bytes).hexdigest()

def merkle_root(hashes):
    """Deterministic Merkle root construction (sorted pairs, duplicate last)"""
    if not hashes:
        return hashlib.sha256(b"").hexdigest()
    
    level = sorted(hashes)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        nxt = []
        for i in range(0, len(level), 2):
            a, b = sorted([level[i], level[i+1]])
            nxt.append(hashlib.sha256(bytes.fromhex(a) + bytes.fromhex(b)).hexdigest())
        level = sorted(nxt)
    return level[0]

def is_batch_manifest(filepath):
    """Check if file is a batch manifest (not payload)"""
    try:
        data = json.loads(filepath.read_text())
        # Batch manifests have batch_type field
        return data.get("batch_type") == "knowledge_broker_batch"
    except:
        return False

def load_batch_roots(batch_dir="_truth/batches"):
    """Load only batch manifests, skip payload files"""
    all_files = list(Path(batch_dir).glob("kb_batch_*.json"))
    batch_files = [f for f in all_files if is_batch_manifest(f)]
    batch_roots = []
    
    for bf in batch_files:
        data = json.loads(bf.read_text())
        
        # Skip aggregate batches (self-inclusion guard)
        if data.get("aggregation_type") == "MERKLE_BATCH_ROOT":
            continue
        
        # Hard fail on missing merkle_root
        if "merkle_root" not in data:
            raise ValueError(f"{bf} missing merkle_root")
        
        batch_roots.append(data["merkle_root"])
    
    return batch_roots

def main():
    print("🔍 Building aggregated batch root...")
    
    # Load raw batch roots
    raw_roots = load_batch_roots()
    
    # Guard against empty aggregation
    if len(raw_roots) == 0:
        raise ValueError("No valid batch roots to aggregate")
    
    print(f"📦 Found {len(raw_roots)} batch roots")
    
    # Single source of truth: normalize, then sort
    normalized_roots = [normalize_root(r) for r in raw_roots]
    normalized_roots.sort()
    
    # Check for duplicates
    if len(set(normalized_roots)) != len(normalized_roots):
        raise ValueError("Duplicate batch roots detected")
    
    # Domain-separate each leaf
    domain_leaves = [domain_separate(r) for r in normalized_roots]
    
    # Build Merkle tree
    global_root = merkle_root(domain_leaves)
    
    # Output both layers for auditability
    result = {
        "leaf_count": len(raw_roots),
        "leaf_roots_raw": [f"0x{r}" for r in raw_roots],
        "domain_separated_leaves": domain_leaves,
        "global_merkle_root": f"0x{global_root}"
    }
    
    print("\n✅ Aggregation complete:")
    print(json.dumps(result, indent=2))
    
    # Machine-readable output
    print(f"\nGLOBAL_ROOT={global_root}")

if __name__ == "__main__":
    main()
