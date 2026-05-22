#!/usr/bin/env python3
import sys
import json
import hashlib
from typing import Dict, Any


def canonicalize_json(data: Dict[str, Any]) -> bytes:
    """Deterministic local canonicalization for fixture identity checks."""
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def verify_receipt_identity(file_path: str) -> Dict[str, Any]:
    """
    Ingests a raw receipt-like JSON object, removes receipt_hash, and compares
    the declared identity value to the SHA-256 of the canonicalized surface.

    This proves hash identity only. It does not prove replay, truth, legality,
    correctness, or semantic authority.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception as e:
        return {"status": "ERROR", "reason": f"File access or parsing failed: {str(e)}"}

    if not isinstance(payload, dict) or "receipt_hash" not in payload:
        return {"status": "ERROR", "reason": "Missing envelope structure or receipt_hash root block."}

    declared_hash_block = payload.get("receipt_hash", {})
    if not isinstance(declared_hash_block, dict):
        return {"status": "ERROR", "reason": "receipt_hash must be an object."}

    declared_value = declared_hash_block.get("value", "")
    observation_surface = {k: v for k, v in payload.items() if k != "receipt_hash"}
    canonical_bytes = canonicalize_json(observation_surface)
    computed_value = hashlib.sha256(canonical_bytes).hexdigest()

    if computed_value == declared_value:
        return {"status": "HASH_MATCH", "computed": computed_value}
    return {"status": "MISMATCH", "computed": computed_value, "declared": declared_value}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "ERROR", "reason": "Requires a target receipt file argument."}))
        sys.exit(1)

    result = verify_receipt_identity(sys.argv[1])
    print(json.dumps(result, indent=2))
    if result.get("status") != "HASH_MATCH":
        sys.exit(1)
