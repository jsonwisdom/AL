"""
policy_loader.py — Versioned, Immutable Policy Registry v0.1
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

POLICIES_DIR = Path("policies")


def compute_policy_hash(policy: Dict[str, Any]) -> str:
    core = {
        "policy_id": policy["policy_id"],
        "version": policy["version"],
        "rules": policy.get("rules", []),
        "effective_from": policy.get("effective_from"),
        "supersedes": policy.get("supersedes"),
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


def validate_policy(policy: Dict[str, Any]) -> bool:
    required = ["policy_id", "version", "effective_from", "rules"]
    missing = [key for key in required if key not in policy]
    if missing:
        raise ValueError(f"Policy missing required fields: {missing}")
    if not isinstance(policy["rules"], list):
        raise ValueError("rules must be a list")
    return True


def load_policy(policy_version: str) -> Dict[str, Any]:
    path = POLICIES_DIR / f"{policy_version}.json"
    if not path.exists():
        raise FileNotFoundError(f"Policy not found: {policy_version}")
    with open(path, "r", encoding="utf-8") as f:
        policy = json.load(f)
    validate_policy(policy)
    return policy


def evaluate_policy(receipt: Dict[str, Any], policy: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if policy is None:
        policy_version = receipt.get("policy", {}).get("policy_version")
        if not policy_version:
            return {"result": "unknown", "reason": "no policy_version in receipt"}
        policy = load_policy(policy_version)

    embedded_version = receipt.get("policy", {}).get("policy_version")
    if embedded_version != policy["policy_id"]:
        return {"result": "mismatch", "reason": "policy version mismatch"}

    policy_hash = compute_policy_hash(policy)
    embedded_hash = receipt.get("policy", {}).get("policy_hash")
    if embedded_hash != policy_hash:
        return {"result": "mismatch", "reason": "policy hash mismatch", "policy_hash": policy_hash}

    return {
        "policy_id": policy["policy_id"],
        "policy_hash": policy_hash,
        "result": receipt.get("policy", {}).get("result", "unknown"),
        "rules_evaluated": receipt.get("policy", {}).get("rules_evaluated", []),
    }


def list_available_policies() -> List[Dict[str, Any]]:
    if not POLICIES_DIR.exists():
        return []
    out: List[Dict[str, Any]] = []
    for path in sorted(POLICIES_DIR.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            policy = json.load(f)
        out.append({
            "policy_id": policy.get("policy_id"),
            "version": policy.get("version"),
            "effective_from": policy.get("effective_from"),
            "policy_hash": compute_policy_hash(policy),
        })
    return out
