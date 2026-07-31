#!/usr/bin/env python3
"""Fail-closed verifier for Pony Express receipt-chain fixtures.

Valid fixture placeholders are materialized in memory using RFC 8785 JCS +
SHA-256. Committed fixture files are never rewritten by the default test run.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import rfc8785

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "receipt-chains"
REQUIRED_FIELDS = {
    "receipt_id",
    "protocol_version",
    "action",
    "result",
    "authority",
    "historical_truth_established",
    "gate_1_status",
    "previous_receipt_hash",
    "receipt_hash",
    "recorded_at",
    "payload",
}
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
UTC_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


class VerificationError(ValueError):
    """Raised when a fixture or receipt violates the protocol."""


def reject_floats(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise VerificationError(f"native float prohibited at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            reject_floats(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_floats(child, f"{path}[{index}]")


def validate_timestamp(value: Any) -> None:
    if not isinstance(value, str) or not UTC_TIMESTAMP.fullmatch(value):
        raise VerificationError("recorded_at must be an RFC 3339 UTC string")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise VerificationError("recorded_at is not a valid timestamp") from exc


def canonical_bytes(receipt: dict[str, Any]) -> bytes:
    payload = {k: v for k, v in receipt.items() if k != "receipt_hash" and not k.startswith("signature")}
    reject_floats(payload)
    encoded = rfc8785.dumps(payload)
    return encoded if isinstance(encoded, bytes) else encoded.encode("utf-8")


def receipt_digest(receipt: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(receipt)).hexdigest()


def validate_shape(receipt: Any) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        raise VerificationError("receipt must be an object")
    missing = REQUIRED_FIELDS - receipt.keys()
    if missing:
        raise VerificationError(f"missing required fields: {sorted(missing)}")
    reject_floats(receipt)
    validate_timestamp(receipt["recorded_at"])
    if receipt["authority"] is not False:
        raise VerificationError("authority must be false")
    if receipt["historical_truth_established"] is not False:
        raise VerificationError("historical_truth_established must be false")
    if receipt["gate_1_status"] != "BLOCKED":
        raise VerificationError("gate_1_status must be BLOCKED")
    return receipt


def materialize_valid_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    """Replace valid-fixture placeholders in memory, preserving source files."""
    output = copy.deepcopy(fixture)
    previous: str | None = None
    for receipt in output.get("receipts", []):
        receipt["previous_receipt_hash"] = previous
        receipt["receipt_hash"] = receipt_digest(receipt)
        previous = receipt["receipt_hash"]
    return output


def verify_chain(receipts: Any) -> tuple[bool, str]:
    try:
        if not isinstance(receipts, list) or not receipts:
            raise VerificationError("receipts must be a non-empty array")
        previous: str | None = None
        for index, raw in enumerate(receipts):
            receipt = validate_shape(raw)
            if receipt["previous_receipt_hash"] != previous:
                raise VerificationError(f"broken link at receipt index {index}")
            claimed = receipt["receipt_hash"]
            if not isinstance(claimed, str) or not HEX_64.fullmatch(claimed):
                raise VerificationError(f"receipt_hash is not lowercase SHA-256 hex at index {index}")
            expected = receipt_digest(receipt)
            if claimed != expected:
                raise VerificationError(f"hash mismatch at receipt index {index}")
            previous = claimed
        return True, "PASS"
    except (VerificationError, rfc8785.CanonicalizationError) as exc:
        return False, str(exc)


def load_fixture(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle, parse_float=lambda _: (_ for _ in ()).throw(VerificationError("native float prohibited")))
        return data, None
    except (OSError, json.JSONDecodeError, VerificationError) as exc:
        return None, str(exc)


def run() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=FIXTURE_ROOT)
    args = parser.parse_args()

    paths = sorted(args.fixtures.rglob("*.json"))
    if not paths:
        print("FAIL: no fixture files found", file=sys.stderr)
        return 1

    failures = 0
    for path in paths:
        fixture, load_error = load_fixture(path)
        if load_error is not None:
            actual = "FAIL"
            detail = load_error
            expected = "FAIL" if "invalid" in path.parts else "PASS"
        else:
            assert fixture is not None
            expected = fixture.get("expected_verdict")
            candidate = materialize_valid_fixture(fixture) if expected == "PASS" else fixture
            valid, detail = verify_chain(candidate.get("receipts"))
            actual = "PASS" if valid else "FAIL"

        matched = actual == expected
        status = "OK" if matched else "MISMATCH"
        print(f"{status}: {path.relative_to(args.fixtures)} expected={expected} actual={actual} detail={detail}")
        failures += 0 if matched else 1

    print(f"SUMMARY: fixtures={len(paths)} mismatches={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run())
