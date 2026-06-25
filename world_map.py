"""
world_map.py — Constitutional World Map Ingestor v0.1

World map consumes receipts. It does not create authority or decide truth.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from receipt import verify_receipt


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_receipt(path: str | Path) -> Dict[str, Any]:
    with open(Path(path), "r", encoding="utf-8") as f:
        return json.load(f)


def eligible_for_ingest(path: str | Path) -> bool:
    try:
        receipt = load_receipt(path)
    except Exception:
        return False
    checks = {
        "valid_receipt": verify_receipt(path)["valid"],
        "authority_false": receipt.get("authority") is False,
        "authorization_granted": receipt.get("authorization", {}).get("result") == "granted",
        "execution_executed": receipt.get("execution", {}).get("status") == "executed",
        "policy_compliant": receipt.get("policy", {}).get("result") == "compliant",
        "has_final_hash": bool(receipt.get("final_hash")),
        "has_policy_hash": bool(receipt.get("policy", {}).get("policy_hash")),
    }
    return all(checks.values())


def project_claims(receipt: Dict[str, Any]) -> list[Dict[str, Any]]:
    return [
        {
            "claim_id": claim.get("claim_id"),
            "text": claim.get("text"),
            "original_confidence": claim.get("confidence"),
        }
        for claim in receipt.get("extraction", {}).get("claims", [])
    ]


def append_world_map_entry(path: str | Path, world_map_path: str | Path = "world_map.jsonl") -> Optional[str]:
    try:
        receipt = load_receipt(path)
    except Exception:
        return None
    if not eligible_for_ingest(path):
        return None

    entry = {
        "map_entry_id": f"wm_{receipt['receipt_id']}",
        "receipt_id": receipt["receipt_id"],
        "final_hash": receipt["final_hash"],
        "policy_hash": receipt.get("policy", {}).get("policy_hash"),
        "claims": project_claims(receipt),
        "verification_result": receipt.get("verification", {}).get("result"),
        "policy_result": receipt.get("policy", {}).get("result"),
        "authorization_result": receipt.get("authorization", {}).get("result"),
        "authority": receipt["authority"],
        "created_at": _utc_now(),
    }
    out = Path(world_map_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry["map_entry_id"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=str, help="Path to receipt JSON")
    parser.add_argument("--map", default="world_map.jsonl")
    args = parser.parse_args()
    result = append_world_map_entry(args.receipt, args.map)
    print(result if result else "Rejected by WORLD_MAP_INGEST_POLICY_V0_1")
