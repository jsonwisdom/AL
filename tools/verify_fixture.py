#!/usr/bin/env python3
"""Minimal V0 replay verifier for AGENT_DELEGATION_RECEIPT_V0 fixtures.

This V0 verifier intentionally uses MOCK proof values. It is a deterministic
stranger-replay harness, not production cryptography.
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

SKEW_SECONDS = 300
VALID_PROOF = "mock-valid-signature"
VALID_BINDING_PROOF = "mock-valid-proof"


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def load_json(path: str):
    try:
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise ValueError(f"invalid json: {path}: {exc}") from exc


def parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def main(argv) -> int:
    if len(argv) != 4:
        print("usage: verify_fixture.py <receipt.json> <binding.json> <policy.json>")
        return 2

    try:
        receipt = load_json(argv[1])
        binding = load_json(argv[2])
        policy = load_json(argv[3])
    except ValueError as exc:
        return fail(str(exc))

    if receipt.get("receipt_type") != "AGENT_DELEGATION_RECEIPT_V0":
        return fail("invalid receipt type")

    if binding.get("binding_type") != "AGENT_RESULT_BINDING_V0":
        return fail("invalid binding type")

    try:
        expires_at = parse_time(receipt["scope"]["expires_at"])
    except Exception:
        return fail("invalid expiration")

    now = datetime.now(timezone.utc)
    if now > expires_at + timedelta(seconds=SKEW_SECONDS):
        return fail("receipt expired")

    proof = receipt.get("proof", {})
    if proof.get("signature") != VALID_PROOF:
        return fail("signature mismatch")

    receipt_digest = proof.get("digest")
    if binding.get("receipt_digest") != receipt_digest:
        return fail("receipt digest mismatch")

    binding_proof = binding.get("proof", {})
    if binding_proof.get("value") != VALID_BINDING_PROOF:
        return fail("binding proof mismatch")

    changed_files = binding.get("result", {}).get("changed_files", [])
    forbidden_paths = set(policy.get("forbidden_paths", []))
    allowed_paths = set(policy.get("allowed_paths", []))

    for path in changed_files:
        if path in forbidden_paths:
            return fail(f"forbidden file touched: {path}")
        if allowed_paths and path not in allowed_paths:
            return fail(f"file outside allowed paths: {path}")

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
