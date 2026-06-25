"""
claim_pipeline.py — Constitutional Claim Verification Pipeline v0.1

Input -> extraction -> evidence -> verification -> policy -> authorization -> receipt.
Verified support is not truth. Receipts never grant authority.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from policy_loader import compute_policy_hash, load_policy
from receipt import (
    compute_core_hash,
    compute_final_hash,
    compute_section_hashes,
    create_receipt_skeleton,
    verify_receipt,
)

POLICY_ID = "POLICY_CLAIM_VERIFICATION_V0_1"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def simple_extract_claims(text: str) -> List[Dict[str, Any]]:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return [
        {"claim_id": f"clm_{i:03d}", "text": f"{sentence}.", "confidence": 0.85}
        for i, sentence in enumerate(sentences)
    ]


def create_evidence_packet(claims: List[Dict[str, Any]], source_text: str) -> Dict[str, Any]:
    evidence_items = []
    for claim in claims:
        digest = hashlib.sha256(claim["text"].encode("utf-8")).hexdigest()
        evidence_items.append({
            "evidence_id": f"ev_{claim['claim_id']}",
            "type": "source_text",
            "content_hash": f"sha256:{digest}",
            "supports_claim": claim["claim_id"],
            "retrieved_at": _utc_now(),
        })
    packet_digest = hashlib.sha256(
        json.dumps(evidence_items, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "packet_hash": f"sha256:{packet_digest}",
        "items": evidence_items,
        "source_text_hash": f"sha256:{hashlib.sha256(source_text.encode('utf-8')).hexdigest()}",
    }


def verify_support(evidence: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "verifier_version": "verify-v0.1",
        "replay_class": "Level2",
        "result": "partial" if evidence.get("items") else "fail",
        "confidence": 0.75 if evidence.get("items") else 0.0,
        "mismatches": [],
    }


def policy_check(claims: List[Dict[str, Any]], evidence: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
    policy_doc = load_policy(POLICY_ID)
    rules = {
        "at_least_one_evidence": len(evidence.get("items", [])) >= 1,
        "every_claim_mapped": all(
            any(item.get("supports_claim") == claim["claim_id"] for item in evidence.get("items", []))
            for claim in claims
        ),
        "verification_passed": verification.get("result") in ("pass", "partial"),
    }
    return {
        "policy_version": POLICY_ID,
        "policy_hash": compute_policy_hash(policy_doc),
        "rules_evaluated": list(rules.keys()),
        "result": "compliant" if all(rules.values()) else "non_compliant",
        "details": rules,
    }


def _add_attestations(receipt: Dict[str, Any], human_approved: bool) -> None:
    receipt["attestations"] = [
        {
            "role": "extractor",
            "identity": "did:key:z6MkClaimExtractor",
            "signature_alg": "ed25519",
            "signed_section": "extraction",
            "signed_section_hash": receipt["section_hashes"]["extraction_hash"],
            "signature": "base64:stubExtractor",
        },
        {
            "role": "verifier",
            "identity": "did:key:z6MkVerifier",
            "signature_alg": "ed25519",
            "signed_section": "verification",
            "signed_section_hash": receipt["section_hashes"]["verification_hash"],
            "signature": "base64:stubVerifier",
        },
    ]
    if human_approved:
        receipt["attestations"].append({
            "role": "authorizer",
            "identity": "did:key:z6MkHumanAuthorizer",
            "signature_alg": "ed25519",
            "signed_section": "core",
            "signed_section_hash": receipt["section_hashes"]["core_hash"],
            "signature": "base64:stubAuthorizer",
        })


def create_claim_verification_receipt(source: str | Dict[str, Any], human_approved: bool = False) -> Dict[str, Any]:
    if isinstance(source, str):
        text = source
        input_data = {"hash": f"sha256:{hashlib.sha256(source.encode('utf-8')).hexdigest()}", "source_type": "text"}
    else:
        text = source.get("text", "")
        input_data = source

    claims = simple_extract_claims(text)
    evidence = create_evidence_packet(claims, text)
    verification = verify_support(evidence)
    policy = policy_check(claims, evidence, verification)
    authorization = {
        "authorized_by": "human" if human_approved else "policy:pending",
        "scope": ["publish_to_map"],
        "result": "granted" if human_approved else "pending_human",
    }

    receipt = create_receipt_skeleton("final", input_data)
    receipt.update({
        "extraction": {"claims": claims},
        "evidence": evidence,
        "verification": verification,
        "policy": policy,
        "authorization": authorization,
        "execution": {
            "actions": [] if not human_approved else [{"type": "world_map_projection", "status": "authorized"}],
            "status": "receipt_only" if not human_approved else "executed",
        },
    })
    receipt["section_hashes"] = compute_section_hashes(receipt)
    receipt["section_hashes"]["core_hash"] = compute_core_hash(receipt)
    _add_attestations(receipt, human_approved)
    receipt["final_hash"] = compute_final_hash(receipt)
    return receipt


def save_receipt(receipt: Dict[str, Any], output_dir: str = "receipts") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = Path(output_dir) / f"{receipt['receipt_id']}.json"
    path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Receipt saved: {path}")
    return str(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, help="Claim text to verify")
    parser.add_argument("--approve", action="store_true", help="Simulate explicit human approval")
    args = parser.parse_args()
    if not args.text:
        raise SystemExit("Usage: python claim_pipeline.py --text 'claim text' [--approve]")
    r = create_claim_verification_receipt(args.text, human_approved=args.approve)
    saved = save_receipt(r)
    print(json.dumps(verify_receipt(saved), indent=2))
