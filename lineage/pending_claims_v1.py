#!/usr/bin/env python3
"""
Pending Claims Handler v1

Evidence aggregation layer for CBRE/Lineage.

Constitutional boundary:
  - This module NEVER writes to asset_lineage_events.jsonl
  - This module NEVER performs adoption
  - This module NEVER resolves competing hashes
  - This module aggregates evidence only
  - This module NEVER trusts caller-provided trace status
  - This module REQUIRES VerifierReceiptV1 before state change
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PENDING_LOG_PATH = Path("lineage/pending_asset_claims.jsonl")

NEW_CLAIM = "NEW_CLAIM"
COALESCED = "COALESCED"
DUPLICATE_CLAIM = "DUPLICATE_CLAIM"
REJECTED = "REJECTED"
REJECTED_TRACE = "REJECTED_TRACE"
SOVEREIGN_REVIEW_REQUIRED = "SOVEREIGN_REVIEW_REQUIRED"

RECEIPT_TYPE = "VERIFIER_RECEIPT_V1"
VERIFIER_VERSION = "CBREv1.2+"
OPCODE_TABLE_ID = "0x0001"
VERIFIED_TRACE = "VERIFIED_TRACE"

REQUIRED_CLAIM_FIELDS = {
    "asset_id",
    "asset_hash",
    "trace_hash",
    "output_commitment",
    "manifest_hash",
    "origin",
    "signature",
    "timestamp_utc",
}


def load_pending_claims(path: Path = PENDING_LOG_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    claims: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip() == "":
            continue
        claims.append(json.loads(raw))
    return claims



def save_pending_claims(
    claims: list[dict[str, Any]],
    path: Path = PENDING_LOG_PATH,
) -> None:
    lines = [json.dumps(c, sort_keys=True, separators=(",", ":")) for c in claims]
    payload = "\n".join(lines)
    if payload:
        payload += "\n"
    path.write_text(payload, encoding="utf-8")



def validate_claim(claim: dict[str, Any]) -> tuple[bool, str | None]:
    missing = REQUIRED_CLAIM_FIELDS.difference(claim)
    if missing:
        return False, f"missing fields: {sorted(missing)}"

    for field in REQUIRED_CLAIM_FIELDS:
        value = claim.get(field)
        if not isinstance(value, str) or value.strip() == "":
            return False, f"invalid field: {field}"

    return True, None



def validate_receipt(
    claim: dict[str, Any],
    verifier_receipt: dict[str, Any] | None,
) -> tuple[str | None, str | None]:
    if verifier_receipt is None:
        return REJECTED_TRACE, "NO_VERIFIER_RECEIPT"

    if verifier_receipt.get("receipt_type") != RECEIPT_TYPE:
        return REJECTED_TRACE, "BAD_RECEIPT_TYPE"

    if verifier_receipt.get("verifier_version") != VERIFIER_VERSION:
        return REJECTED_TRACE, "BAD_VERIFIER_VERSION"

    if verifier_receipt.get("opcode_table_id") != OPCODE_TABLE_ID:
        return REJECTED_TRACE, "BAD_OPCODE_TABLE"

    if verifier_receipt.get("trace_status") != VERIFIED_TRACE:
        return REJECTED_TRACE, "TRACE_STATUS_NOT_VERIFIED"

    if verifier_receipt.get("trace_hash") != claim.get("trace_hash"):
        return REJECTED_TRACE, "TRACE_HASH_MISMATCH"

    if verifier_receipt.get("output_commitment") != claim.get("output_commitment"):
        return REJECTED_TRACE, "OUTPUT_COMMITMENT_MISMATCH"

    return None, None



def process_claim(
    claim: dict[str, Any],
    verifier_receipt: dict[str, Any] | None,
    pending_claims: list[dict[str, Any]],
) -> tuple[str, list[dict[str, Any]]]:
    valid, reason = validate_claim(claim)
    if not valid:
        raise ValueError(f"REJECTED: {reason}")

    receipt_status, receipt_reason = validate_receipt(claim, verifier_receipt)
    if receipt_status is not None:
        raise ValueError(f"{receipt_status}: {receipt_reason}")

    asset_hash = claim["asset_hash"]
    origin = claim["origin"]

    for existing in pending_claims:
        if existing["asset_hash"] != asset_hash:
            continue

        existing_origins = {
            attestor["branch_id"]
            for attestor in existing.get("attestors", [])
        }

        if origin in existing_origins:
            return DUPLICATE_CLAIM, pending_claims

        existing.setdefault("attestors", []).append(
            {
                "branch_id": origin,
                "manifest_hash": claim["manifest_hash"],
                "signature": claim["signature"],
                "timestamp_utc": claim["timestamp_utc"],
            }
        )
        existing["latest_attestation_utc"] = claim["timestamp_utc"]

        return COALESCED, pending_claims

    pending_claims.append(
        {
            "asset_id": claim["asset_id"],
            "asset_hash": claim["asset_hash"],
            "trace_hash": claim["trace_hash"],
            "output_commitment": claim["output_commitment"],
            "trace_status": VERIFIED_TRACE,
            "trace_verified_at": verifier_receipt["verified_at_utc"],
            "latest_attestation_utc": claim["timestamp_utc"],
            "attestors": [
                {
                    "branch_id": origin,
                    "manifest_hash": claim["manifest_hash"],
                    "signature": claim["signature"],
                    "timestamp_utc": claim["timestamp_utc"],
                }
            ],
            "adoption_status": "ELIGIBLE",
        }
    )

    return NEW_CLAIM, pending_claims



def detect_competing_hashes(
    pending_claims: list[dict[str, Any]],
) -> list[list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}

    for claim in pending_claims:
        grouped.setdefault(claim["asset_id"], []).append(claim)

    competing: list[list[dict[str, Any]]] = []

    for asset_id, claims in grouped.items():
        unique_hashes = {claim["asset_hash"] for claim in claims}

        if len(unique_hashes) > 1:
            for claim in claims:
                claim["adoption_status"] = "COMPETING"
            competing.append(claims)

    return competing



def main() -> int:
    claims = load_pending_claims()
    competing = detect_competing_hashes(claims)

    print(f"pending_claims={len(claims)}")
    print(f"competing_groups={len(competing)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
