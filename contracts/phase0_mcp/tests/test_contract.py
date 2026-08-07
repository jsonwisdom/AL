from __future__ import annotations

import json
from pathlib import Path

import pytest

from contracts.phase0_mcp.src.canonicalize import sha256_value
from contracts.phase0_mcp.src.contract import ContractError, validate_signed_envelope
from contracts.phase0_mcp.src.receipt import build_contract_receipt

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
ADAPTER_SHA = "343a2c894ba74da6493e470fd864992680601be8"
COMMAND = "python -m pytest contracts/phase0-mcp/tests -q"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def sign(envelope: dict) -> dict:
    payload_hash = sha256_value(envelope["receipt"])
    envelope["signature"]["signed_payload_hash"] = payload_hash
    envelope["signature"]["value"] = sha256_value(
        {"key_id": envelope["signature"]["key_id"], "payload_hash": payload_hash}
    )
    return envelope


def test_valid_fixture_contract() -> None:
    fixture = sign(load("signed_mcp_receipt.valid.json"))
    validate_signed_envelope(fixture)
    receipt = build_contract_receipt(
        fixture=fixture,
        adapter_commit_sha=ADAPTER_SHA,
        test_command=COMMAND,
        exit_code=0,
        output={"accepted": True},
        result="PASS",
        failure_reason=None,
    )
    assert receipt["authority"] is False
    assert set(receipt) == {
        "input_fixture_sha256",
        "adapter_commit_sha",
        "test_command",
        "exit_code",
        "output_sha256",
        "compatibility_result",
        "failure_reason",
        "authority",
    }


def test_hash_mismatch_requires_mutation_source() -> None:
    fixture = sign(load("signed_mcp_receipt.hash_mismatch.json"))
    with pytest.raises(ContractError, match="MUTATION_SOURCE_REQUIRED"):
        validate_signed_envelope(fixture)


def test_unknown_field_is_rejected() -> None:
    fixture = sign(load("signed_mcp_receipt.unknown_field.json"))
    with pytest.raises(ContractError, match="UNKNOWN_FIELDS"):
        validate_signed_envelope(fixture)
