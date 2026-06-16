#!/usr/bin/env python3
"""
ALMS claim ledger validator.

Purpose:
- Block semantic overreach at commit/CI time.
- Enforce per-claim bounding plus basic cross-claim consistency.

Scope:
- Structure and epistemic status checks only.
- Does not fetch external content.
- Does not promote, attest, or open gates.
"""

import json
import re
import sys
from pathlib import Path

TEMPORAL_LEAKS = [
    "as of today",
    "currently",
    "still",
    "now",
    "at present",
]

ALLOWED_TYPES = {"EXISTENCE", "FACTUAL", "INTERPRETATION"}
ALLOWED_STATUS = {"VERIFIED", "UNVERIFIED", "REJECTED"}


def fail(message: str) -> None:
    print(f"CLAIM_LEDGER_INVALID: {message}")
    sys.exit(1)


def references_external_world(statement: str) -> bool:
    lower = statement.lower()
    return any(tok in lower for tok in TEMPORAL_LEAKS)


def validate_single_claim(claim: dict) -> None:
    cid = claim.get("claim_id", "<missing>")
    ctype = claim.get("type")
    status = claim.get("status")
    statement = claim.get("statement", "")

    if ctype not in ALLOWED_TYPES:
        fail(f"{cid}: invalid type {ctype}")
    if status not in ALLOWED_STATUS:
        fail(f"{cid}: invalid status {status}")

    grounding = claim.get("grounding")
    if not isinstance(grounding, list) or not grounding:
        fail(f"{cid}: grounding required")

    for g in grounding:
        if "node_ref" not in g and "evidence_path" not in g:
            fail(f"{cid}: grounding must contain node_ref or evidence_path")

    # Core bounding rules.
    if ctype == "INTERPRETATION" and status == "VERIFIED":
        fail(f"{cid}: INTERPRETATION claims cannot be VERIFIED")

    if ctype == "FACTUAL" and status == "VERIFIED":
        # Conservative rule: FACTUAL cannot be VERIFIED from artifact bytes alone.
        fail(f"{cid}: FACTUAL claims cannot be VERIFIED from artifact text alone")

    if references_external_world(statement) and status == "VERIFIED":
        fail(f"{cid}: temporal/external-world leak cannot be VERIFIED")


def grounding_fingerprint(claim: dict) -> tuple:
    normalized = []
    for g in claim.get("grounding", []):
        normalized.append((
            g.get("node_ref", ""),
            g.get("evidence_path", ""),
            g.get("evidence_sha256", ""),
        ))
    return tuple(sorted(normalized))


def claim_fingerprint(claim: dict) -> tuple:
    return (
        claim.get("type"),
        claim.get("statement"),
        grounding_fingerprint(claim),
    )


def extract_numeric_bound(statement: str):
    """Minimal numeric contradiction extraction.

    Supports phrases like:
    - over 3.5 million
    - more than 3 million
    - fewer than 1 million
    - less than 1000000
    - exactly 2000

    Returns (kind, value) or None.
    """
    s = statement.lower().replace(",", "")
    match = re.search(r"\b(over|more than|greater than|less than|fewer than|under|exactly)\s+([0-9]+(?:\.[0-9]+)?)\s*(million|billion|thousand)?", s)
    if not match:
        return None
    kind, num, scale = match.groups()
    value = float(num)
    if scale == "thousand":
        value *= 1_000
    elif scale == "million":
        value *= 1_000_000
    elif scale == "billion":
        value *= 1_000_000_000
    return kind, value


def numeric_bounds_conflict(a, b) -> bool:
    if not a or not b:
        return False
    ka, va = a
    kb, vb = b

    lower_kinds = {"over", "more than", "greater than"}
    upper_kinds = {"less than", "fewer than", "under"}

    # over X conflicts with less than/fewer than Y when X >= Y.
    if ka in lower_kinds and kb in upper_kinds and va >= vb:
        return True
    if kb in lower_kinds and ka in upper_kinds and vb >= va:
        return True

    # exactly X conflicts with exactly Y when X != Y.
    if ka == "exactly" and kb == "exactly" and va != vb:
        return True

    # exactly X conflicts with lower/upper constraints if outside bound.
    if ka == "exactly" and kb in lower_kinds and not (va > vb):
        return True
    if kb == "exactly" and ka in lower_kinds and not (vb > va):
        return True
    if ka == "exactly" and kb in upper_kinds and not (va < vb):
        return True
    if kb == "exactly" and ka in upper_kinds and not (vb < va):
        return True

    return False


def validate_cross_claims(claims: list) -> None:
    seen_ids = set()
    seen_fps = {}
    verified_existence_by_grounding = []

    for claim in claims:
        cid = claim.get("claim_id")
        if not cid:
            fail("claim missing claim_id")
        if cid in seen_ids:
            fail(f"duplicate claim_id: {cid}")
        seen_ids.add(cid)

        fp = claim_fingerprint(claim)
        prior_status = seen_fps.get(fp)
        if prior_status is not None and prior_status != claim.get("status"):
            fail(f"inconsistent status for duplicate claim fingerprint: {cid}")
        seen_fps[fp] = claim.get("status")

        if claim.get("type") == "EXISTENCE" and claim.get("status") == "VERIFIED":
            verified_existence_by_grounding.append(claim)

    # Minimal numeric contradiction scan among VERIFIED EXISTENCE claims
    for i, a in enumerate(verified_existence_by_grounding):
        for b in verified_existence_by_grounding[i + 1:]:
            if grounding_fingerprint(a) != grounding_fingerprint(b):
                continue
            if numeric_bounds_conflict(
                extract_numeric_bound(a.get("statement", "")),
                extract_numeric_bound(b.get("statement", "")),
            ):
                fail(f"numeric contradiction between {a['claim_id']} and {b['claim_id']}")


def validate_file(path: Path) -> None:
    with path.open("r", encoding="utf-8") as f:
        ledger = json.load(f)

    if "claims" not in ledger or not isinstance(ledger["claims"], list):
        fail(f"{path}: missing claims[]")

    for claim in ledger["claims"]:
        validate_single_claim(claim)

    validate_cross_claims(ledger["claims"])
    print(f"CLAIM_LEDGER_VALID: {path}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_claim_ledger.py <ledger.json> [more.json ...]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        validate_file(Path(arg))


if __name__ == "__main__":
    main()
