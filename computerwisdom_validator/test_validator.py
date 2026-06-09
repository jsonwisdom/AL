"""Replay-parity tests for the ComputerWisdom validator stack.

These tests execute the canonical fixture corpus against the frozen decision
matrix. Passing tests prove implementation alignment only; they do not create
authority, attestation, liquidity, or verification receipts.
"""

from computerwisdom_validator.receipt_gen import generate_receipt
from computerwisdom_validator.validator import evaluate
from computerwisdom_validator.verify import run_verification_suite, suite_passed


FIXTURES = [
    {
        "name": "valid_pass",
        "expected_state": "PASS",
        "input": {
            "expected_hash": "0xaaa",
            "observed_hash": "0xaaa",
            "attestation_present": True,
            "schema_version": "1.0.0",
            "evidence_uri": "ipfs://bafyvalid",
            "continuity_boundary": "RESPECTED",
        },
    },
    {
        "name": "blocked_missing_hash",
        "expected_state": "BLOCKED",
        "input": {
            "expected_hash": "0xaaa",
            "observed_hash": "PENDING_INPUT",
            "attestation_present": True,
            "schema_version": "1.0.0",
            "evidence_uri": "ipfs://bafyvalid",
            "continuity_boundary": "RESPECTED",
        },
    },
    {
        "name": "fail_hash_mismatch",
        "expected_state": "FAIL",
        "input": {
            "expected_hash": "0xaaa",
            "observed_hash": "0xbbb",
            "attestation_present": True,
            "schema_version": "1.0.0",
            "evidence_uri": "ipfs://bafyvalid",
            "continuity_boundary": "RESPECTED",
        },
    },
    {
        "name": "pending_no_attestation",
        "expected_state": "PENDING",
        "input": {
            "expected_hash": "0xaaa",
            "observed_hash": "0xaaa",
            "attestation_present": False,
            "schema_version": "1.0.0",
            "evidence_uri": "ipfs://bafyvalid",
            "continuity_boundary": "RESPECTED",
        },
    },
    {
        "name": "fail_schema_mismatch",
        "expected_state": "FAIL",
        "input": {
            "expected_hash": "0xaaa",
            "observed_hash": "0xaaa",
            "attestation_present": True,
            "schema_version": "2.0.0",
            "evidence_uri": "ipfs://bafyvalid",
            "continuity_boundary": "RESPECTED",
        },
    },
    {
        "name": "blocked_invalid_uri",
        "expected_state": "BLOCKED",
        "input": {
            "expected_hash": "0xaaa",
            "observed_hash": "0xaaa",
            "attestation_present": True,
            "schema_version": "1.0.0",
            "evidence_uri": "not-a-verifiable-uri",
            "continuity_boundary": "RESPECTED",
        },
    },
    {
        "name": "fail_continuity_breach",
        "expected_state": "FAIL",
        "input": {
            "expected_hash": "0xaaa",
            "observed_hash": "0xaaa",
            "attestation_present": True,
            "schema_version": "1.0.0",
            "evidence_uri": "ipfs://bafyvalid",
            "continuity_boundary": "BREACHED",
        },
    },
]


def test_canonical_fixtures_match_decision_table():
    for fixture in FIXTURES:
        assert evaluate(fixture["input"]) == fixture["expected_state"]


def test_verification_suite_reports_all_matches():
    results = run_verification_suite(FIXTURES)
    assert suite_passed(results) is True
    assert all(result.verification_result == "MATCH" for result in results)
    assert all(result.failure_class is None for result in results)


def test_receipt_generation_preserves_authority_false():
    fixture = FIXTURES[0]
    evaluated = evaluate(fixture["input"])
    receipt = generate_receipt(
        fixture_name=fixture["name"],
        input_data=fixture["input"],
        expected_state=fixture["expected_state"],
        evaluated_state=evaluated,
    )

    assert receipt["receipt_type"] == "VALIDATOR_VERIFICATION_RECEIPT"
    assert receipt["verification_result"] == "MATCH"
    assert receipt["authority"] is False
    assert receipt["membrane"] == "INTACT"
    assert receipt["no_fake_green"] is True
    assert receipt["input_hash"].startswith("sha256:")
