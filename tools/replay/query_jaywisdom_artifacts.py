#!/usr/bin/env python3
"""
Query the Jay Wisdom Zora artifact seed index.

Local read-only search over JSONL records.
No Zora API call. No chain call. No wallet. No revenue claim.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_INDEX = "docs/zora/artifacts/jaywisdom_zora_artifact_index_seed_v0_1.jsonl"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at line {line_no}: {exc}") from exc
    return records


def record_text(record: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ["id", "title", "creator", "platform", "profile", "status", "category", "source", "notes"]:
        value = record.get(key)
        if value is not None:
            parts.append(str(value))
    tags = record.get("tags", [])
    if isinstance(tags, list):
        parts.extend(str(tag) for tag in tags)
    return " ".join(parts).lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="Query Jay Wisdom Zora artifact seed index")
    parser.add_argument("--index", default=DEFAULT_INDEX, help="JSONL artifact index path")
    parser.add_argument("--query", required=True, help="Case-insensitive search string")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true", help="Print raw JSON records")
    args = parser.parse_args()

    records = load_jsonl(Path(args.index))
    query = args.query.lower().strip()
    matches = [record for record in records if query in record_text(record)]

    output = {
        "query": args.query,
        "index": args.index,
        "records_scanned": len(records),
        "matches_returned": min(len(matches), args.limit),
        "full_catalog": False,
        "source_boundary": "seed index from operator screenshot; not full Zora export",
        "chain_write": False,
        "wallet_control": False,
        "revenue_confirmed": False,
        "authority": False,
        "no_fake_green": True,
        "matches": matches[: args.limit],
    }

    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(f"query={args.query}")
        print(f"records_scanned={len(records)}")
        print(f"matches_returned={output['matches_returned']}")
        print("full_catalog=false")
        print("source_boundary=seed index from operator screenshot; not full Zora export")
        for record in matches[: args.limit]:
            tags = ",".join(record.get("tags", [])) if isinstance(record.get("tags"), list) else ""
            print(f"- {record.get('id')} | {record.get('title')} | {record.get('category')} | {tags}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
