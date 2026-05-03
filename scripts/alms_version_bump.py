#!/usr/bin/env python3
"""
ALMS version bump automation.

Usage:
  python scripts/alms_version_bump.py \
    --id C0001 \
    --version 1.0.0 \
    --state REPLAY_PASSED \
    --artifact corpus/C0001/replay/expected_hashes.json

This updates alms/version_registry.json and emits a receipt under
alms/version_receipts/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

ALLOWED_STATES = {
    "DRAFT",
    "LOCKED",
    "REPLAY_REQUIRED",
    "REPLAY_PASSED",
    "BLOCKED",
    "DEPRECATED",
}

REGISTRY_PATH = Path("alms/version_registry.json")
RECEIPT_DIR = Path("alms/version_receipts")


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"registry_version": "1.0.0", "entries": []}
    return json.loads(REGISTRY_PATH.read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--state", required=True, choices=sorted(ALLOWED_STATES))
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--layer", default="corpus_version")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    artifact_path = Path(args.artifact)
    if not artifact_path.exists():
        raise SystemExit(f"ARTIFACT_MISSING {artifact_path}")

    artifact_hash = sha256_file(artifact_path)
    registry = load_registry()
    entries = registry.setdefault("entries", [])

    old_entry = None
    for entry in entries:
        if entry.get("id") == args.id:
            old_entry = dict(entry)
            entry.update(
                {
                    "layer": args.layer,
                    "version": args.version,
                    "state": args.state,
                    "artifact_path": artifact_path.as_posix(),
                    "hash": artifact_hash,
                    "notes": args.notes,
                }
            )
            break

    if old_entry is None:
        old_entry = {
            "id": args.id,
            "version": "0.0.0",
            "state": "DRAFT",
            "hash": None,
        }
        entries.append(
            {
                "id": args.id,
                "layer": args.layer,
                "version": args.version,
                "state": args.state,
                "artifact_path": artifact_path.as_posix(),
                "hash": artifact_hash,
                "depends_on": [],
                "notes": args.notes,
            }
        )

    REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n")

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "event_type": "alms_version_bump",
        "id": args.id,
        "old_version": old_entry.get("version"),
        "new_version": args.version,
        "old_state": old_entry.get("state"),
        "new_state": args.state,
        "old_hash": old_entry.get("hash"),
        "artifact_path": artifact_path.as_posix(),
        "artifact_hash": artifact_hash,
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "notes": args.notes,
    }
    receipt_path = RECEIPT_DIR / f"{args.id}-{args.version}.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")

    print(json.dumps({"registry": str(REGISTRY_PATH), "receipt": str(receipt_path), "artifact_hash": artifact_hash}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
