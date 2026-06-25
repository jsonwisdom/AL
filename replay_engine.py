"""
replay_engine.py — Independent Receipt Replayer v0.1

Clone repo -> replay receipt -> verify hashes, attestations, and immutable policy hash.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from policy_loader import evaluate_policy, load_policy
from receipt import verify_receipt


def replay_receipt(path: str | Path, expected_policy_hash: str | None = None) -> Dict[str, Any]:
    with open(Path(path), "r", encoding="utf-8") as f:
        receipt = json.load(f)

    result: Dict[str, Any] = {
        "receipt_id": receipt.get("receipt_id"),
        "replay_success": False,
        "hash_verification": False,
        "policy_verification": False,
        "details": {},
    }

    hash_ok = verify_receipt(path)["valid"]
    result["hash_verification"] = hash_ok

    policy_version = receipt.get("policy", {}).get("policy_version")
    if policy_version:
        policy_doc = load_policy(policy_version)
        policy_hash = receipt.get("policy", {}).get("policy_hash")
        result["details"]["policy_hash"] = policy_hash
        if expected_policy_hash and policy_hash != expected_policy_hash:
            result["details"]["policy_hash_mismatch"] = True
        else:
            policy_eval = evaluate_policy(receipt, policy_doc)
            result["details"]["policy_eval"] = policy_eval
            result["policy_verification"] = policy_eval.get("result") == "compliant"

    result["replay_success"] = bool(hash_ok and result["policy_verification"])
    result["message"] = "Full replay successful" if result["replay_success"] else "Replay failed — see details"
    return result


def batch_replay(directory: str | Path = "receipts") -> Dict[str, Any]:
    receipts_dir = Path(directory)
    receipts = sorted(receipts_dir.glob("*.json")) if receipts_dir.exists() else []
    results = [replay_receipt(path) for path in receipts]
    successful = sum(1 for item in results if item["replay_success"])
    return {
        "total": len(results),
        "successful": successful,
        "success_rate": successful / len(results) if results else 1,
        "results": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", nargs="?", help="Receipt path")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--directory", default="receipts")
    args = parser.parse_args()
    if args.batch:
        print(json.dumps(batch_replay(args.directory), indent=2))
    elif args.receipt:
        print(json.dumps(replay_receipt(args.receipt), indent=2))
    else:
        print("Usage: python replay_engine.py <receipt> | --batch")
