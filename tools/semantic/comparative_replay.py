#!/usr/bin/env python3
import sys
import json
import uuid
from typing import Any, Dict, List
from receipt_hash import verify_receipt_identity


def flatten_surface(d: Any, prefix: str = "") -> Dict[str, Any]:
    """Flatten nested structures into dot-notation surfaces."""
    items: List[tuple] = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                items.extend(flatten_surface(v, new_key).items())
            else:
                items.append((new_key, v))
    return dict(items)


def compute_surface_drift(receipt_a: Dict[str, Any], receipt_b: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate a field-level drift trace between two receipt-like records."""
    surf_a = {k: v for k, v in receipt_a.items() if k != "receipt_hash"}
    surf_b = {k: v for k, v in receipt_b.items() if k != "receipt_hash"}

    flat_a = flatten_surface(surf_a)
    flat_b = flatten_surface(surf_b)

    drift = []
    all_keys = set(flat_a.keys()).union(set(flat_b.keys()))

    for key in sorted(all_keys):
        val_a = flat_a.get(key)
        val_b = flat_b.get(key)

        if val_a != val_b:
            drift.append({
                "path": key,
                "before": val_a,
                "after": val_b,
            })

    return drift


def execute_comparative_replay(file_path_a: str, file_path_b: str) -> Dict[str, Any]:
    """
    Execute a structural comparison between two receipt-like JSON records.

    This engine performs identity comparison and field drift analysis only.
    Semantic truth arbitration is intentionally excluded.
    """
    res_a = verify_receipt_identity(file_path_a)
    res_b = verify_receipt_identity(file_path_b)

    if res_a.get("status") == "ERROR" or res_b.get("status") == "ERROR":
        return {
            "status": "ENGINE_ERROR",
            "reason": f"A: {res_a.get('reason')}, B: {res_b.get('reason')}",
        }

    with open(file_path_a, "r", encoding="utf-8") as f:
        raw_a = json.load(f)

    with open(file_path_b, "r", encoding="utf-8") as f:
        raw_b = json.load(f)

    hash_a = raw_a.get("receipt_hash", {}).get("value", "MALFORMED")
    hash_b = raw_b.get("receipt_hash", {}).get("value", "MALFORMED")

    checkpoint_a = raw_a.get("substrate_checkpoint")
    checkpoint_b = raw_b.get("substrate_checkpoint")
    substrate_match = (checkpoint_a == checkpoint_b) and (checkpoint_a is not None)

    drift_report = compute_surface_drift(raw_a, raw_b)

    if (
        res_a["status"] == "HASH_MATCH"
        and res_b["status"] == "HASH_MATCH"
        and substrate_match
    ):
        lineage_result = "LINEAGE_CONTINUITY"
    else:
        lineage_result = "LINEAGE_BREAK"

    return {
        "comparison_id": str(uuid.uuid4()),
        "receipt_a": hash_a,
        "receipt_b": hash_b,
        "substrate_checkpoint_match": substrate_match,
        "identity_surface": {
            "a_status": res_a["status"],
            "b_status": res_b["status"],
        },
        "field_drift": drift_report,
        "lineage_result": lineage_result,
        "semantic_analysis": None,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"status": "ENGINE_ERROR", "reason": "Requires two receipt files as arguments."}))
        sys.exit(1)

    report = execute_comparative_replay(sys.argv[1], sys.argv[2])
    print(json.dumps(report, indent=2))
