#!/usr/bin/env python3
"""
ALMS Receipt Boundary Verifier v1

Dependency-free consumption-layer gate for threshold-aware receipts.

Rules enforced:
- Required boundary receipt fields are present.
- receipt_status is COMPLETE or PARTIAL.
- upstream_status, when present, is COMPLETE, PARTIAL, or NONE.
- remainder is explicit and fixed: guaranteed=true and correspondence_outside_scope=NOT_CLAIMED.
- FAIL if PARTIAL input produces COMPLETE output without conversion receipt.
- FAIL if inherited_latent is stripped when upstream is PARTIAL.

This verifier intentionally does not infer latent status from missing receipts.
It only checks declared receipt-boundary fields.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


PASS_MESSAGE = "PASS: receipt boundary checks clean"

REQUIRED_FIELDS = [
    "claim_id",
    "timestamp_utc",
    "actor",
    "nonce",
    "inputs",
    "outputs",
    "verdict",
    "receipt_status",
    "threshold",
    "remainder",
]

VALID_RECEIPT_STATUS = {"COMPLETE", "PARTIAL"}
VALID_UPSTREAM_STATUS = {"COMPLETE", "PARTIAL", "NONE"}


def load_receipt(path: Path) -> Dict[str, Any]:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_required_fields(receipt: Dict[str, Any]) -> Optional[str]:
    missing = [field for field in REQUIRED_FIELDS if field not in receipt]
    if missing:
        return f"FAIL: missing required fields: {missing}"
    return None


def check_receipt_status(receipt: Dict[str, Any]) -> Optional[str]:
    status = receipt.get("receipt_status")
    if status not in VALID_RECEIPT_STATUS:
        return f"FAIL: receipt_status must be COMPLETE or PARTIAL, got {status!r}"
    return None


def check_upstream_status(receipt: Dict[str, Any]) -> Optional[str]:
    upstream = receipt.get("upstream_status")
    if upstream is not None and upstream not in VALID_UPSTREAM_STATUS:
        return f"FAIL: upstream_status must be COMPLETE, PARTIAL, or NONE, got {upstream!r}"
    return None


def check_remainder(receipt: Dict[str, Any]) -> Optional[str]:
    remainder = receipt.get("remainder", {})
    if not isinstance(remainder, dict):
        return "FAIL: remainder must be an object"
    if remainder.get("guaranteed") is not True:
        return "FAIL: remainder.guaranteed must be true"
    if remainder.get("correspondence_outside_scope") != "NOT_CLAIMED":
        return "FAIL: remainder.correspondence_outside_scope must be NOT_CLAIMED"
    return None


def check_partial_not_laundered(receipt: Dict[str, Any]) -> Optional[str]:
    upstream = receipt.get("upstream_status")
    if upstream == "PARTIAL":
        status = receipt.get("receipt_status")
        if status == "COMPLETE" and not receipt.get("conversion_receipt"):
            return "FAIL: PARTIAL input produces COMPLETE output without conversion receipt"
    return None


def check_inherited_latent_preserved(receipt: Dict[str, Any]) -> Optional[str]:
    upstream = receipt.get("upstream_status")
    if upstream == "PARTIAL":
        inherited = receipt.get("inherited_latent")
        if inherited is None:
            return "FAIL: inherited_latent missing from PARTIAL chain descendant"
        if not isinstance(inherited, dict) or "present" not in inherited:
            return "FAIL: inherited_latent must be object with 'present' field"
    return None


CHECKS = [
    check_required_fields,
    check_receipt_status,
    check_upstream_status,
    check_remainder,
    check_partial_not_laundered,
    check_inherited_latent_preserved,
]


def verify(path: Path) -> List[str]:
    try:
        receipt = load_receipt(path)
    except json.JSONDecodeError as exc:
        return [f"FAIL: invalid JSON: {exc}"]
    except FileNotFoundError:
        return [f"FAIL: file not found: {path}"]

    failures: List[str] = []
    for check in CHECKS:
        result = check(receipt)
        if result:
            failures.append(result)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="ALMS receipt boundary verifier v1")
    parser.add_argument("input", help="local boundary receipt JSON file")
    args = parser.parse_args()

    failures = verify(Path(args.input))
    if failures:
        for failure in failures:
            print(failure)
        return 1

    print(PASS_MESSAGE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
