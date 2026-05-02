#!/usr/bin/env python3

import argparse
import hashlib
import json
import sys
from pathlib import Path

DEFAULT_LEAVES_DIR = Path("_truth/leaves")
DEFAULT_POLICY = Path("_truth/policies/knowledge_broker_policy_v1.canonical.json")
DEFAULT_MANIFEST = Path("_truth/batches/kb_batch_001.json")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def find_receipts(leaves_dir: Path):
    return sorted(leaves_dir.glob("KB_*/receipt.canonical.json"))

def rebuild_manifest(leaves_dir: Path, policy_path: Path):
    policy_hash = sha256_bytes(policy_path.read_bytes())
    items = []
    blocked = []

    for receipt_path in find_receipts(leaves_dir):
        try:
            receipt = load_json(receipt_path)
            receipt_hash = sha256_bytes(canonical_json(receipt).encode())

            leaf_id = receipt.get("leaf_id")
            if not leaf_id:
                blocked.append({"path": str(receipt_path), "reason": "missing_leaf_id"})
                continue

            items.append({
                "leaf_id": leaf_id,
                "path": str(receipt_path),
                "status": receipt.get("status"),
                "anchor_allowed": str(bool(receipt.get("anchor_allowed", False))).lower(),
                "receipt_hash": receipt_hash
            })
        except Exception as e:
            blocked.append({"path": str(receipt_path), "reason": str(e)})

    items.sort(key=lambda x: (x["leaf_id"], x["path"]))
    blocked.sort(key=lambda x: x["path"])

    core = {
        "batch_type": "knowledge_broker_batch",
        "policy": "knowledge_broker_policy_v1",
        "policy_hash": policy_hash,
        "ready_count": len(items),
        "blocked_count": len(blocked),
        "items": items,
        "blocked_items": blocked
    }

    batch_hash = sha256_bytes(canonical_json(core).encode())

    return {
        "batch_id": f"kb_batch_{batch_hash[:16]}",
        "batch_hash": batch_hash,
        **core
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fail-on-blocked", action="store_true")
    args = parser.parse_args()

    stored = load_json(DEFAULT_MANIFEST)
    replayed = rebuild_manifest(DEFAULT_LEAVES_DIR, DEFAULT_POLICY)

    print(f"STORED_BLOCKED={stored['blocked_count']} REPLAYED_BLOCKED={replayed['blocked_count']}")

    if canonical_json(stored) != canonical_json(replayed):
        print("KB_BATCH_REPLAY_FAIL mismatch", file=sys.stderr)
        sys.exit(1)

    if args.fail_on_blocked and replayed["blocked_count"] > 0:
        print("KB_BATCH_REPLAY_FAIL blocked_items_present", file=sys.stderr)
        sys.exit(1)

    print("KB_BATCH_REPLAY_OK")

if __name__ == "__main__":
    main()

def merkle_root(hashes):
    import hashlib
    if not hashes:
        return hashlib.sha256(b"").hexdigest()

    level = sorted(hashes)

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])

        nxt = []
        for i in range(0, len(level), 2):
            a, b = sorted([level[i], level[i + 1]])
            combined = bytes.fromhex(a) + bytes.fromhex(b)
            nxt.append(hashlib.sha256(combined).hexdigest())

        level = sorted(nxt)

    return level[0]


expected_root = merkle_root([item["receipt_hash"] for item in items])

if manifest.get("merkle_root") != expected_root:
    import sys
    print("MERKLE_ROOT_MISMATCH", file=sys.stderr)
    sys.exit(1)
