"""First-run receipt assembler for the ComputerWisdom validator stack.

This script is the evidence-producing lane for VALIDATOR_RUN_RECEIPT_001.
It executes the canonical fixture corpus, summarizes match counts, computes a
canonical receipt hash, and persists the run receipt only when invoked.

It never grants authority. Authority and attestation remain hard-coded false.
"""

import hashlib
from pathlib import Path
from typing import Any, Mapping

try:
    from .receipt_gen import canonical_json, receipt_json
    from .verify import run_verification_suite
except ImportError:  # pragma: no cover - supports direct script execution
    from receipt_gen import canonical_json, receipt_json
    from verify import run_verification_suite


RECEIPT_ID = "VALIDATOR_RUN_RECEIPT_001"
RECEIPT_TYPE = "VALIDATOR_VERIFICATION_RUN_RECEIPT"
VERSION = "0.1"
REPOSITORY = "jsonwisdom/AL"
DECISION_TABLE_VERSION = "DECISION_TABLE_V0_1"
OUTPUT_PATH = Path("receipts/validator_verification/VALIDATOR_RUN_RECEIPT_001.json")
HASH_PATH = Path("receipts/validator_verification/VALIDATOR_RUN_RECEIPT_001.sha256")

VALIDATOR_STACK_COMMITS = {
    "__init__.py": "f930e4345fc9823f9a025e5c830eba4047c2b943",
    "validator.py": "9c5ae8207c21e1d86eda14b11db673cdacb7aca5",
    "verify.py": "627ed0bf51b608aba6d54b647227bb565bfd5dfa",
    "receipt_gen.py": "f927ee86ea99db185f22396a61f6e9eea59caed9",
    "test_validator.py": "2c3d607bf1f180b1fe78e87f3e028757bb55aaf8",
    "README.md": "5fd34bc15eb1e5941b72184349cd0db3b8abd714",
}

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


def receipt_hash(receipt: Mapping[str, Any]) -> str:
    """Compute the canonical SHA-256 identity for a receipt."""
    digest = hashlib.sha256(canonical_json(receipt).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def classify_run(matched_count: int, mismatch_count: int, execution_error: bool = False) -> str:
    """Return the canonical first-run result class."""
    if execution_error:
        return "EXECUTION_ERROR"
    if mismatch_count == 0:
        return "MATCH_ALL"
    return "MISMATCH_PRESENT"


def build_run_receipt() -> dict[str, Any]:
    """Execute fixtures and build VALIDATOR_RUN_RECEIPT_001."""
    try:
        results = run_verification_suite(FIXTURES)
        matched_count = sum(result.verification_result == "MATCH" for result in results)
        mismatch_count = sum(result.verification_result != "MATCH" for result in results)
        failure_classes = sorted(
            {
                result.failure_class
                for result in results
                if result.failure_class is not None
            }
        )
        run_result = classify_run(matched_count, mismatch_count)
    except Exception as exc:  # pragma: no cover - preserves execution evidence
        matched_count = 0
        mismatch_count = len(FIXTURES)
        failure_classes = ["EXECUTION_ERROR", exc.__class__.__name__]
        run_result = classify_run(matched_count, mismatch_count, execution_error=True)

    receipt = {
        "receipt_id": RECEIPT_ID,
        "receipt_type": RECEIPT_TYPE,
        "version": VERSION,
        "repository": REPOSITORY,
        "validator_stack_commits": VALIDATOR_STACK_COMMITS,
        "decision_table_version": DECISION_TABLE_VERSION,
        "fixture_count": len(FIXTURES),
        "fixtures": [fixture["name"] for fixture in FIXTURES],
        "run_result": run_result,
        "matched_count": matched_count,
        "mismatch_count": mismatch_count,
        "failure_classes": failure_classes,
        "authority": False,
        "attestation": False,
        "membrane": "INTACT",
        "no_fake_green": True,
    }
    receipt["receipt_hash"] = receipt_hash(receipt)
    return receipt


def persist_run_receipt(receipt: Mapping[str, Any]) -> None:
    """Persist the run receipt and its evidence hash."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(receipt_json(receipt), encoding="utf-8")
    HASH_PATH.write_text(f"{receipt['receipt_hash']}  {OUTPUT_PATH.name}\n", encoding="utf-8")


def main() -> int:
    receipt = build_run_receipt()
    persist_run_receipt(receipt)
    print(f"{RECEIPT_ID} {receipt['run_result']} {receipt['receipt_hash']}")
    return 0 if receipt["run_result"] == "MATCH_ALL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
