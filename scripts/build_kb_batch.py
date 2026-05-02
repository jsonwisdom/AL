#!/usr/bin/env python3
"""
Track 010: Deterministic KB Batch Processor

Scans _truth/leaves/KB_*/receipt.canonical.json,
hashes each receipt, emits deterministic batch manifest,
and writes a SHA-256 receipt for the manifest.

No timestamps inside hashed manifest.
No auto-anchor.
No silent skipping.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_LEAVES_DIR = Path("_truth/leaves")
DEFAULT_OUT = Path("_truth/batches/kb_batch_001.json")
DEFAULT_POLICY = Path("_truth/policies/knowledge_broker_policy_v1.canonical.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def find_receipts(leaves_dir: Path) -> List[Path]:
    return sorted(leaves_dir.glob("KB_*/receipt.canonical.json"), key=lambda p: str(p))


def build_manifest(leaves_dir: Path, policy_path: Path) -> Dict[str, Any]:
    if not policy_path.exists():
        fail(f"missing policy: {policy_path}")

    policy_hash = sha256_bytes(policy_path.read_bytes())
    receipts = find_receipts(leaves_dir)

    items: List[Dict[str, str]] = []
    blocked: List[Dict[str, str]] = []

    for receipt_path in receipts:
        try:
            receipt = load_json(receipt_path)
            receipt_canon = canonical_json(receipt).encode("utf-8")
            receipt_hash = sha256_bytes(receipt_canon)

            leaf_id = str(receipt.get("leaf_id", ""))
            status = str(receipt.get("status", ""))
            anchor_allowed = bool(receipt.get("anchor_allowed", False))

            if not leaf_id:
                blocked.append({"path": str(receipt_path), "reason": "missing_leaf_id"})
                continue

            items.append({
                "leaf_id": leaf_id,
                "path": str(receipt_path),
                "status": status,
                "anchor_allowed": str(anchor_allowed).lower(),
                "receipt_hash": receipt_hash
            })

        except Exception as exc:
            blocked.append({"path": str(receipt_path), "reason": f"error:{exc}"})

    items.sort(key=lambda x: (x["leaf_id"], x["path"]))
    blocked.sort(key=lambda x: x["path"])

    manifest_core = {
        "batch_type": "knowledge_broker_batch",
        "policy": "knowledge_broker_policy_v1",
        "policy_hash": policy_hash,
        "ready_count": len(items),
        "blocked_count": len(blocked),
        "items": items,
        "blocked_items": blocked
    }

    batch_hash = sha256_bytes(canonical_json(manifest_core).encode("utf-8"))

    return {
        "batch_id": f"kb_batch_{batch_hash[:16]}",
        "batch_hash": batch_hash,
        **manifest_core
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--leaves-dir", default=str(DEFAULT_LEAVES_DIR))
    parser.add_argument("--policy", default=str(DEFAULT_POLICY))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = build_manifest(Path(args.leaves_dir), Path(args.policy))
    canon = canonical_json(manifest) + "\n"

    print(f"KB_BATCH_ID={manifest['batch_id']}")
    print(f"KB_BATCH_HASH={manifest['batch_hash']}")
    print(f"READY={manifest['ready_count']} BLOCKED={manifest['blocked_count']}")

    if not args.dry_run:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        out.with_suffix(out.suffix + ".sha256").write_text(
            f"{sha256_bytes(canon.encode('utf-8'))}  {out}\n",
            encoding="utf-8"
        )
        print(f"WROTE={out}")


if __name__ == "__main__":
    main()
