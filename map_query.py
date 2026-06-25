"""
map_query.py — Constitutional World Map Query Tools v0.1

Returns receipt-backed projections only. Never asserts truth. Never authorizes action.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_world_map(path: str | Path = "world_map.jsonl") -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    entries: List[Dict[str, Any]] = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def find_by_receipt_id(receipt_id: str, path: str | Path = "world_map.jsonl") -> Optional[Dict[str, Any]]:
    for entry in load_world_map(path):
        if entry.get("receipt_id") == receipt_id:
            return entry
    return None


def find_by_claim_text(query: str, path: str | Path = "world_map.jsonl") -> List[Dict[str, Any]]:
    q = query.lower()
    results: List[Dict[str, Any]] = []
    for entry in load_world_map(path):
        for claim in entry.get("claims", []):
            if q in claim.get("text", "").lower():
                results.append(entry)
                break
    return results


def summarize_map(path: str | Path = "world_map.jsonl") -> Dict[str, Any]:
    entries = load_world_map(path)
    if not entries:
        return {"total_entries": 0, "status": "empty_map", "message": "No verified receipts ingested yet."}
    counts: Dict[str, int] = {}
    for entry in entries:
        key = entry.get("verification_result", "unknown")
        counts[key] = counts.get(key, 0) + 1
    return {
        "total_entries": len(entries),
        "verification_breakdown": counts,
        "latest_entry": entries[-1].get("created_at"),
        "message": "Projection from verified receipts only. No truth asserted.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query constitutional world map")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--receipt", type=str)
    parser.add_argument("--search", type=str)
    parser.add_argument("--map", default="world_map.jsonl")
    args = parser.parse_args()
    if args.summary:
        print(json.dumps(summarize_map(args.map), indent=2))
    elif args.receipt:
        print(json.dumps(find_by_receipt_id(args.receipt, args.map), indent=2))
    elif args.search:
        print(json.dumps(find_by_claim_text(args.search, args.map), indent=2))
    else:
        print("Usage: python map_query.py --summary | --receipt ID | --search TEXT")
