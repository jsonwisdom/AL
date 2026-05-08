#!/usr/bin/env python3
"""
ALMS Receipt Boundary Verifier v1

Minimal consumption-layer gate for threshold-aware receipts.

First enforceable rules:
- FAIL if PARTIAL input produces COMPLETE output without conversion receipt.
- FAIL if inherited_latent is stripped when upstream is PARTIAL.

This verifier intentionally does not infer latent status from missing receipts.
It only checks declared receipt-boundary fields.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


PASS_MESSAGE = "PASS: receipt boundary checks clean"


def load_receipt(path: Path) -> Dict[str, Any]:
    if not path.exists() or not path.is_file():
        raise ValueError(f"input file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_output_status(receipt: Dict[str, Any]) -> Optional[str]:
    nested = receipt.get("receipt")
    if isinstance(nested, dict):
        status = nested.get("status") or nested.get("receipt_status")
        if status is not None:
            return str(status)
    status = receipt.get("status") or receipt.get("receipt_status")
    return str(status) if status is not None else None


def get_upstream_status(receipt: Dict[str, Any]) -> Optional[str]:
    status = receipt.get("upstream_status")
    if status is not None:
        return str(status)
    upstream = receipt.get("upstream")
    if isinstance(upstream, dict):
        status = upstream.get("status") or upstream.get("receipt_status")
        return str(status) if status is not None else None
    return None


def has_conversion_receipt(receipt: Dict[str, Any]) -> bool:
    conversion = receipt.get("conversion_receipt")
    if conversion:
        return True
    conversion = receipt.get("conversion")
    if isinstance(conversion, dict):
        return bool(conversion.get("receipt") or conversion.get("receipt_id") or conversion.get("receipt_hash"))
    return False


def check_partial_not_laundered(receipt: Dict[str, Any]) -> Optional[str]:
    """FAIL if PARTIAL input produces COMPLETE output without conversion receipt."""
    upstream = get_upstream_status(receipt)
    output_status = get_output_status(receipt)

    if upstream == "PARTIAL" and output_status == "COMPLETE" and not has_conversion_receipt(receipt):
        return "FAIL: PARTIAL input produces COMPLETE output without conversion receipt"
    return None


def check_inherited_latent_preserved(receipt: Dict[str, Any]) -> Optional[str]:
    """FAIL if inherited_latent is stripped when upstream is PARTIAL."""
    upstream = get_upstream_status(receipt)

    if upstream == "PARTIAL" and "inherited_latent" not in receipt:
        return "FAIL: inherited_latent missing from PARTIAL chain descendant"
    return None


def verify(path: Path) -> List[str]:
    receipt = load_receipt(path)
    failures: List[str] = []

    for check in [check_partial_not_laundered, check_inherited_latent_preserved]:
        result = check(receipt)
        if result:
            failures.append(result)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="ALMS receipt boundary verifier v1")
    parser.add_argument("input", help="local receipt or replay JSON file")
    args = parser.parse_args()

    try:
        failures = verify(Path(args.input))
    except Exception as exc:
        print(f"INVALID_INPUT: {exc}", file=sys.stderr)
        return 64

    if failures:
        for failure in failures:
            print(failure)
        return 1

    print(PASS_MESSAGE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
