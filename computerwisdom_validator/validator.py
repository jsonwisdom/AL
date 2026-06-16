"""Pure validator implementation for DECISION_TABLE_V0_1.

The validator resolves fixture inputs to a state only. It does not create
receipts, attestations, authority, network calls, or repository mutations.
"""

from enum import Enum
from typing import Any, Mapping


class State(str, Enum):
    BLOCKED = "BLOCKED"
    FAIL = "FAIL"
    PENDING = "PENDING"
    PASS = "PASS"


REQUIRED_FIELDS = {
    "expected_hash",
    "observed_hash",
    "attestation_present",
    "schema_version",
    "evidence_uri",
    "continuity_boundary",
}

CANONICAL_SCHEMA_VERSION = "1.0.0"
COMPATIBLE_SCHEMA_VERSIONS = {CANONICAL_SCHEMA_VERSION}
RESPECTED = "RESPECTED"
BREACHED = "BREACHED"
PENDING_INPUT = "PENDING_INPUT"


def missing(value: Any) -> bool:
    """Return True when a required value is absent or explicitly pending."""
    return value is None or value == "" or value == PENDING_INPUT


def valid_evidence_uri(uri: Any) -> bool:
    """Accept only evidence URIs that are independently retrievable later."""
    if not isinstance(uri, str) or missing(uri):
        return False
    return uri.startswith("ipfs://") or uri.startswith("https://")


def schema_compatible(schema_version: Any) -> bool:
    """Return True only for schema versions authorized by the frozen table."""
    return schema_version in COMPATIBLE_SCHEMA_VERSIONS


def evaluate(fixture: Mapping[str, Any]) -> str:
    """Resolve one fixture input to one canonical validator state.

    Decision order follows DECISION_TABLE_V0_1:
    1. BLOCKED for missing required evidence or invalid evidence URI.
    2. FAIL for hash mismatch, breached continuity, or schema incompatibility.
    3. PENDING for matching hash with respected boundary and no attestation.
    4. PASS for matching hash with respected boundary, attestation, and schema.
    """
    for field in REQUIRED_FIELDS:
        if field not in fixture or missing(fixture.get(field)):
            return State.BLOCKED.value

    expected_hash = fixture["expected_hash"]
    observed_hash = fixture["observed_hash"]
    attestation_present = fixture["attestation_present"]
    schema_version = fixture["schema_version"]
    evidence_uri = fixture["evidence_uri"]
    boundary = fixture["continuity_boundary"]

    if not valid_evidence_uri(evidence_uri):
        return State.BLOCKED.value

    if (
        observed_hash != expected_hash
        or boundary == BREACHED
        or not schema_compatible(schema_version)
    ):
        return State.FAIL.value

    if (
        observed_hash == expected_hash
        and boundary == RESPECTED
        and attestation_present is False
    ):
        return State.PENDING.value

    if (
        observed_hash == expected_hash
        and boundary == RESPECTED
        and attestation_present is True
        and schema_compatible(schema_version)
    ):
        return State.PASS.value

    return State.FAIL.value
