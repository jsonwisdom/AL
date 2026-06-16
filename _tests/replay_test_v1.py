#!/usr/bin/env python3
"""
ALMS replay membrane regression test v1.

This test suite is intentionally local and non-authoritative.
It verifies expected validator behavior before keyset, validator policy,
and public canon notices are indexed.
"""

from dataclasses import dataclass
from typing import Optional

ALLOWED_BOOTSTRAP_SCOPE = {
    "boundary_receipts",
    "keyset_publication",
    "validator_policy_receipts",
    "repo_hygiene_receipts",
}

FORBIDDEN_SCOPE = {
    "Epoch 4 experimental claim promotion",
    "OpenAI legitimacy claims",
    "RED_TO_GREEN narrative elevation",
    "visual art as truth",
    "universal canonical supremacy",
}


@dataclass(frozen=True)
class Candidate:
    name: str
    indexed: bool
    signature_valid: bool
    scope: str
    schema_type: str
    key_type: str
    threshold_mode: str


def validate(candidate: Candidate) -> tuple[bool, str]:
    if not candidate.indexed:
        return False, "R1/R6 reject: non-indexed receipts have zero canonical authority"

    if not candidate.signature_valid:
        return False, "R2 reject: invalid signature"

    if candidate.schema_type == "ClaimDraft":
        return False, "R5 reject: ClaimDraft is syntactically invalid for index.json"

    if candidate.key_type == "WK":
        return False, "R5 reject: WK keys cannot promote canonical receipts"

    if candidate.scope in FORBIDDEN_SCOPE:
        return False, "R4 reject: forbidden bootstrap scope"

    if candidate.threshold_mode == "1_of_1_bootstrap":
        if candidate.scope not in ALLOWED_BOOTSTRAP_SCOPE:
            return False, "R3/R7 reject: bootstrap key cannot promote experimental claims"

    return True, "accept: indexed receipt with valid signature and allowed scope"


def run() -> None:
    cases = [
        Candidate("boundary receipt allowed", True, True, "boundary_receipts", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("keyset publication allowed", True, True, "keyset_publication", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("validator policy allowed", True, True, "validator_policy_receipts", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("repo hygiene allowed", True, True, "repo_hygiene_receipts", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("epoch 4 experimental promotion blocked", True, True, "Epoch 4 experimental claim promotion", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("OpenAI legitimacy blocked", True, True, "OpenAI legitimacy claims", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("RED to GREEN narrative blocked", True, True, "RED_TO_GREEN narrative elevation", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("visual art blocked", True, True, "visual art as truth", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("universal supremacy blocked", True, True, "universal canonical supremacy", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("ClaimDraft blocked", True, True, "boundary_receipts", "ClaimDraft", "CA", "1_of_1_bootstrap"),
        Candidate("WK key blocked", True, True, "boundary_receipts", "Receipt", "WK", "1_of_1_bootstrap"),
        Candidate("non-indexed blocked", False, True, "boundary_receipts", "Receipt", "CA", "1_of_1_bootstrap"),
        Candidate("invalid signature blocked", True, False, "boundary_receipts", "Receipt", "CA", "1_of_1_bootstrap"),
    ]

    expected_accepts = {
        "boundary receipt allowed",
        "keyset publication allowed",
        "validator policy allowed",
        "repo hygiene allowed",
    }

    failures: list[str] = []
    for case in cases:
        accepted, reason = validate(case)
        should_accept = case.name in expected_accepts
        if accepted != should_accept:
            failures.append(f"{case.name}: expected {should_accept}, got {accepted} ({reason})")
        print(f"{'PASS' if accepted == should_accept else 'FAIL'} | {case.name} | {reason}")

    if failures:
        raise SystemExit("\n".join(failures))

    print("\nALMS replay membrane regression: PASS")


if __name__ == "__main__":
    run()
