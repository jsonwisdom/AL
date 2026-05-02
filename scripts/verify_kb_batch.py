#!/usr/bin/env python3
"""
Track 013: Deterministic KB Batch Replay Verifier

Rebuilds the KB batch from _truth/leaves/KB_*/receipt.canonical.json
and verifies it exactly against _truth/batches/kb_batch_001.json.

No timestamps.
No policy-engine dependency.
No partial success on hash mismatch.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_LEAVES_DIR = Path("_truth/leaves")
DEFAULT_POLICY = Path("_truth/policies/knowledge_broker_policy_v1.canonical.json")
DEFAULT_MANIFEST = Path("_truth/batches/kb_batch_001.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def find_receipts(leaves_dir: Path) -> List[Path]:
    return sorted(leaves_dir.glob("KB_*/receipt.canonical.json"), key=lambda p: str(p))


def rebuild_manifest(leaves_dir: Path, policy_path: Path) -> Dict[str, Any]:
    if not policy_path.exists():
        raise FileNotFoundError(f"missing policy: {policy_path}")

    policy_hash = sha256_bytes(policy_path.read_bytes())
    items = []
    blocked = []

    for receipt_path in find_receipts(leaves_dir):
        try:
            receipt = load_json(receipt_path)
            receipt_hash = sha256_bytes(canonical_json(receipt).encode("utf-8"))

            leaf_id = str(receipt.get("leaf_id", ""))
            if not leaf_id:
                blocked.append({"path": str(receipt_path), "reason": "missing_leaf_id"})
                continue

            items.append({
                "leaf_id": leaf_id,
                "path": str(receipt_path),
                "status": str(receipt.get("status", "")),
                "anchor_allowed": str(bool(receipt.get("anchor_allowed", False))).lower(),
                "receipt_hash": receipt_hash
            })
        except Exception as exc:
            blocked.append({"path": str(receipt_path), "reason": f"error:{exc}"})

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

    batch_hash = sha256_bytes(canonical_json(core).encode("utf-8"))

    return {
        "batch_id": f"kb_batch_{batch_hash[:16]}",
        "batch_hash": batch_hash,
        **core
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--leaves-dir", default=str(DEFAULT_LEAVES_DIR))
    parser.add_argument("--policy", default=str(DEFAULT_POLICY))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"KB_BATCH_REPLAY_FAIL missing_manifest={manifest_path}", file=sys.stderr)
        sys.exit(1)

    stored = load_json(manifest_path)
    replayed = rebuild_manifest(Path(args.leaves_dir), Path(args.policy))

    stored_hash = stored.get("batch_hash")
    replayed_hash = replayed.get("batch_hash")

    print(f"STORED_BATCH_ID={stored.get('batch_id')}")
    print(f"REPLAYED_BATCH_ID={replayed.get('batch_id')}")
    print(f"STORED_BATCH_HASH={stored_hash}")
    print(f"REPLAYED_BATCH_HASH={replayed_hash}")
    print(f"STORED_READY={stored.get('ready_count')} REPLAYED_READY={replayed.get('ready_count')}")
    print(f"STORED_BLOCKED={stored.get('blocked_count')} REPLAYED_BLOCKED={replayed.get('blocked_count')}")

    if canonical_json(stored) != canonical_json(replayed):
        print("KB_BATCH_REPLAY_FAIL canonical_manifest_mismatch", file=sys.stderr)
        sys.exit(1)

    print("KB_BATCH_REPLAY_OK")


if __name__ == "__main__":
    main()
