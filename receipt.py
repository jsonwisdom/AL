"""
receipt.py — Constitutional Receipt v0.1

Receipts prove process only. Receipts never prove truth or grant authority.
"""

import json
import hashlib
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

VALID_SIGNED_SECTIONS = {
    "input", "extraction", "evidence", "verification",
    "policy", "authorization", "execution", "core"
}


def jcs(obj: Any) -> str:
    """Deterministic JSON canonicalization approximation for v0.1."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_jcs(obj: Any) -> str:
    digest = hashlib.sha256(jcs(obj).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def compute_section_hashes(receipt: Dict[str, Any]) -> Dict[str, str]:
    sections = [
        "input", "extraction", "evidence", "verification",
        "policy", "authorization", "execution"
    ]
    out: Dict[str, str] = {}
    for section in sections:
        if section in receipt:
            out[f"{section}_hash"] = sha256_jcs(receipt[section])
    return out


def _core_view(receipt: Dict[str, Any]) -> Dict[str, Any]:
    core = {k: v for k, v in receipt.items() if k not in ("attestations", "final_hash")}
    if "section_hashes" in core and isinstance(core["section_hashes"], dict):
        core["section_hashes"] = {
            k: v for k, v in core["section_hashes"].items() if k != "core_hash"
        }
    return core


def compute_core_hash(receipt: Dict[str, Any]) -> str:
    """core_hash = JCS(receipt minus attestations/final_hash, excluding core_hash self-reference)."""
    return sha256_jcs(_core_view(receipt))


def compute_final_hash(receipt: Dict[str, Any]) -> str:
    """final_hash = JCS(receipt excluding only final_hash)."""
    final = {k: v for k, v in receipt.items() if k != "final_hash"}
    return sha256_jcs(final)


def verify_hashes(receipt: Dict[str, Any]) -> bool:
    section_hashes = receipt.get("section_hashes")
    if not isinstance(section_hashes, dict):
        return False

    expected_sections = compute_section_hashes(receipt)
    for key, expected in expected_sections.items():
        if section_hashes.get(key) != expected:
            return False

    if section_hashes.get("core_hash") != compute_core_hash(receipt):
        return False

    if receipt.get("final_hash") != compute_final_hash(receipt):
        return False

    return True


def verify_signature(identity: str, message_hash: str, signature: str) -> bool:
    """Pluggable v0.1 signature stub. Replace with DID/Ed25519 in v0.2."""
    return bool(identity and message_hash and signature)


def verify_attestations(receipt: Dict[str, Any]) -> bool:
    attestations = receipt.get("attestations")
    if not isinstance(attestations, list) or not attestations:
        return False

    section_hashes = receipt.get("section_hashes", {})
    for att in attestations:
        section = att.get("signed_section")
        if section not in VALID_SIGNED_SECTIONS:
            return False
        if att.get("signature_alg") != "ed25519":
            return False

        if section == "core":
            target_hash = section_hashes.get("core_hash")
        else:
            target_hash = section_hashes.get(f"{section}_hash")
        if not target_hash:
            return False
        if att.get("signed_section_hash") != target_hash:
            return False
        if not verify_signature(att.get("identity", ""), target_hash, att.get("signature", "")):
            return False

    return True


def verify_invariants(receipt: Dict[str, Any]) -> bool:
    if receipt.get("authority") is not False:
        return False
    if receipt.get("version") != "0.1":
        return False
    if receipt.get("canonicalization", {}).get("method") != "JCS":
        return False
    if receipt.get("canonicalization", {}).get("hash_alg") != "sha256":
        return False
    return True


def verify_receipt(path: str | Path) -> Dict[str, Any]:
    try:
        with open(Path(path), "r", encoding="utf-8") as f:
            receipt = json.load(f)
    except Exception as exc:
        return {"valid": False, "error": f"Failed to load: {exc}"}

    checks = {
        "invariants": verify_invariants(receipt),
        "hashes": verify_hashes(receipt),
        "attestations": verify_attestations(receipt),
    }
    valid = all(checks.values())
    return {
        "valid": valid,
        "receipt_id": receipt.get("receipt_id"),
        "receipt_type": receipt.get("receipt_type"),
        "checks": checks,
        "details": "All checks passed" if valid else "One or more checks failed",
    }


def seal_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    receipt = dict(receipt)
    receipt["section_hashes"] = compute_section_hashes(receipt)
    receipt["section_hashes"]["core_hash"] = compute_core_hash(receipt)
    receipt["final_hash"] = compute_final_hash(receipt)
    return receipt


def create_receipt_skeleton(receipt_type: str, input_data: Dict[str, Any] | None = None) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    suffix = secrets.token_hex(6)
    receipt = {
        "receipt_id": f"rec_{now.strftime('%Y%m%d')}_{suffix}",
        "receipt_type": receipt_type,
        "version": "0.1",
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "authority": False,
        "canonicalization": {"method": "JCS", "hash_alg": "sha256"},
    }
    if input_data is not None:
        receipt["input"] = input_data
    return receipt
