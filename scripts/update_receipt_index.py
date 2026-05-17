#!/usr/bin/env python3
"""Append a receipt entry to receipts/index.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

INDEX_PATH = Path("receipts/index.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: scripts/update_receipt_index.py <receipt.json>")
        return 2

    receipt_path = Path(sys.argv[1])
    receipt = load_json(receipt_path)

    index = load_json(INDEX_PATH)

    entry = {
        "receipt_id": receipt.get("receipt_id"),
        "path": str(receipt_path),
        "timestamp": receipt.get("timestamp"),
        "operation": receipt.get("operation", {}).get("type"),
        "status": receipt.get("outcome", {}).get("status"),
        "head_commit": receipt.get("outcome", {}).get("result", {}).get("head_commit"),
    }

    entries = index.setdefault("entries", [])

    if any(existing.get("receipt_id") == entry["receipt_id"] for existing in entries):
        print(f"index already contains receipt_id={entry['receipt_id']}")
        return 0

    entries.append(entry)
    index["tip"] = entry["receipt_id"]

    write_json(INDEX_PATH, index)

    print("INDEX_UPDATED")
    print(f"receipt_id: {entry['receipt_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
