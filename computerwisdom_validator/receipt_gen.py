"""Receipt generation for validator verification results.

This module turns verification outputs into deterministic JSON-compatible
receipt dictionaries. It does not execute the validator, decide authority,
perform network calls, or mutate repository state unless save_receipt is called
explicitly by a separate harness.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Mapping


RECEIPT_TYPE = "VALIDATOR_VERIFICATION_RECEIPT"
RECEIPT_VERSION = "0.1"
DECISION_TABLE_VERSION = "DECISION_TABLE_V0_1"


def canonical_json(data: Mapping[str, Any]) -> str:
    """Return stable JSON for hashing and replay comparison."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def input_hash(input_data: Mapping[str, Any]) -> str:
    """Return sha256 digest over canonical fixture input JSON."""
    digest = hashlib.sha256(canonical_json(input_data).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def generate_receipt(
    fixture_name: str,
    input_data: Mapping[str, Any],
    expected_state: str,
    evaluated_state: str,
    failure_class: str | None = None,
) -> dict[str, Any]:
    """Generate one validator verification receipt.

    Authority is always false. A MATCH proves only that the implementation
    matched the expected fixture state for this input.
    """
    verification_result = "MATCH" if expected_state == evaluated_state else "MISMATCH"

    return {
        "receipt_type": RECEIPT_TYPE,
        "version": RECEIPT_VERSION,
        "fixture_name": fixture_name,
        "input_hash": input_hash(input_data),
        "decision_table_version": DECISION_TABLE_VERSION,
        "expected_state": expected_state,
        "evaluated_state": evaluated_state,
        "verification_result": verification_result,
        "failure_class": failure_class,
        "authority": False,
        "membrane": "INTACT",
        "no_fake_green": True,
    }


def receipt_json(receipt: Mapping[str, Any]) -> str:
    """Serialize receipt as stable, human-readable JSON."""
    return json.dumps(receipt, sort_keys=True, indent=2) + "\n"


def save_receipt(receipt: Mapping[str, Any], filepath: str | Path) -> None:
    """Persist a receipt artifact to an explicit path."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(receipt_json(receipt), encoding="utf-8")
