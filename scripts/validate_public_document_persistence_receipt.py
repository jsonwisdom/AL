#!/usr/bin/env python3
"""
Validate PUBLIC_DOCUMENT_PERSISTENCE_RECEIPT JSON files.

This validator is intentionally small and local-first.
It enforces the Sardine Marshal teaching loop:

DOCUMENT -> CUSTODY -> HASH -> REPLAY -> STATUS

It does not verify court facts or document contents.
It verifies receipt structure and epistemic posture.
"""

import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "type",
    "subject",
    "claim_mode",
    "allegation_mode",
    "existence",
    "custody",
    "mutation_history",
    "redaction_state",
    "release_timeline",
    "verification_path",
    "destruction_authorization",
    "verification_status",
    "claim_status",
]

ALLOWED_VERIFICATION_STATUS = {
    "unknown",
    "unverified",
    "unavailable",
    "sealed",
    "pending_public_evidence",
    "destroyed_with_receipt",
    "destroyed_without_receipt",
    "verified",
}

ALLOWED_CLAIM_STATUS = {"indeterminate", "verified", "blocked"}
ALLOWED_REDACTION_STATE = {"unknown", "none", "partial", "full", "sealed"}
ALLOWED_EXISTENCE_STATUS = {"unknown", "claimed", "verified"}
ALLOWED_DESTRUCTION_STATUS = {
    "not_destroyed",
    "unknown",
    "destroyed_with_receipt",
    "destroyed_without_receipt",
}


def fail(path: Path, message: str) -> int:
    print(f"FAIL {path}: {message}")
    return 1


def validate(path: Path) -> int:
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(path, f"invalid JSON: {exc}")

    if not isinstance(receipt, dict):
        return fail(path, "receipt must be a JSON object")

    missing = [key for key in REQUIRED_TOP_LEVEL if key not in receipt]
    if missing:
        return fail(path, f"missing required fields: {', '.join(missing)}")

    if receipt["type"] != "PUBLIC_DOCUMENT_PERSISTENCE_RECEIPT":
        return fail(path, "type must be PUBLIC_DOCUMENT_PERSISTENCE_RECEIPT")

    if receipt["claim_mode"] != "existence_and_custody_only":
        return fail(path, "claim_mode must be existence_and_custody_only")

    if receipt["allegation_mode"] != "blocked":
        return fail(path, "allegation_mode must remain blocked")

    existence = receipt["existence"]
    if not isinstance(existence, dict):
        return fail(path, "existence must be an object")
    for key in ["status", "source_uri", "document_hash"]:
        if key not in existence:
            return fail(path, f"existence missing {key}")
    if existence["status"] not in ALLOWED_EXISTENCE_STATUS:
        return fail(path, "invalid existence.status")

    if not isinstance(receipt["custody"], list):
        return fail(path, "custody must be an array")
    if not isinstance(receipt["mutation_history"], list):
        return fail(path, "mutation_history must be an array")
    if not isinstance(receipt["release_timeline"], list):
        return fail(path, "release_timeline must be an array")

    if receipt["redaction_state"] not in ALLOWED_REDACTION_STATE:
        return fail(path, "invalid redaction_state")

    destruction = receipt["destruction_authorization"]
    if destruction is not None:
        if not isinstance(destruction, dict):
            return fail(path, "destruction_authorization must be object or null")
        for key in ["status", "authorized_by", "authority", "date"]:
            if key not in destruction:
                return fail(path, f"destruction_authorization missing {key}")
        if destruction["status"] not in ALLOWED_DESTRUCTION_STATUS:
            return fail(path, "invalid destruction_authorization.status")

    if receipt["verification_status"] not in ALLOWED_VERIFICATION_STATUS:
        return fail(path, "invalid verification_status")

    if receipt["claim_status"] not in ALLOWED_CLAIM_STATUS:
        return fail(path, "invalid claim_status")

    if receipt["verification_status"] == "verified":
        if receipt["claim_status"] != "verified":
            return fail(path, "verified receipt must have claim_status verified")
        if existence["status"] != "verified":
            return fail(path, "verified receipt must have existence.status verified")
        if not existence["source_uri"]:
            return fail(path, "verified receipt requires source_uri")
        if not existence["document_hash"]:
            return fail(path, "verified receipt requires document_hash")
        if not receipt["verification_path"]:
            return fail(path, "verified receipt requires verification_path")

    if receipt["verification_status"] == "pending_public_evidence":
        if receipt["claim_status"] != "indeterminate":
            return fail(path, "pending_public_evidence must have claim_status indeterminate")

    print(f"PASS {path}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: validate_public_document_persistence_receipt.py <receipt.json> [...]")
        return 2

    status = 0
    for item in argv[1:]:
        status |= validate(Path(item))
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
