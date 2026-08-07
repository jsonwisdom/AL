from __future__ import annotations

from typing import Any

from .canonicalize import sha256_value


class ContractError(ValueError):
    pass


def validate_phase0_semantics(receipt: dict[str, Any]) -> None:
    required = {
        "run_id",
        "call_index",
        "parent_call_index",
        "tool_name",
        "tool_version",
        "requested_arguments_hash",
        "executed_arguments_hash",
        "mutation_source",
        "authorization",
        "mode",
        "execution_status",
        "output_hash",
        "error",
        "authority",
    }
    unknown = set(receipt) - required
    missing = required - set(receipt)
    if unknown:
        raise ContractError(f"UNKNOWN_FIELDS:{','.join(sorted(unknown))}")
    if missing:
        raise ContractError(f"MISSING_FIELDS:{','.join(sorted(missing))}")
    if receipt["authority"] is not False:
        raise ContractError("AUTHORITY_MUST_BE_FALSE")
    if (
        receipt["requested_arguments_hash"] != receipt["executed_arguments_hash"]
        and not receipt["mutation_source"]
    ):
        raise ContractError("MUTATION_SOURCE_REQUIRED")

    status = receipt["execution_status"]
    if status == "COMPLETED":
        if not receipt["output_hash"] or receipt["error"] is not None:
            raise ContractError("COMPLETED_RECEIPT_INVALID")
    elif status == "FAILED":
        if not isinstance(receipt["error"], dict):
            raise ContractError("FAILED_ERROR_REQUIRED")
    elif status == "DENIED":
        if receipt["authorization"] != "DENIED" or receipt["output_hash"] is not None:
            raise ContractError("DENIED_RECEIPT_INVALID")
    else:
        raise ContractError("UNKNOWN_EXECUTION_STATUS")


def validate_signed_envelope(envelope: dict[str, Any]) -> None:
    if set(envelope) != {"receipt", "signature"}:
        raise ContractError("SIGNED_ENVELOPE_FIELDS_INVALID")
    validate_phase0_semantics(envelope["receipt"])
    signature = envelope["signature"]
    if set(signature) != {"algorithm", "key_id", "signed_payload_hash", "value"}:
        raise ContractError("SIGNATURE_FIELDS_INVALID")
    if signature["algorithm"] != "TEST-SHA256":
        raise ContractError("SIGNATURE_ALGORITHM_UNSUPPORTED")
    payload_hash = sha256_value(envelope["receipt"])
    if signature["signed_payload_hash"] != payload_hash:
        raise ContractError("SIGNED_PAYLOAD_HASH_MISMATCH")
    expected = sha256_value({"key_id": signature["key_id"], "payload_hash": payload_hash})
    if signature["value"] != expected:
        raise ContractError("SIGNATURE_VALUE_MISMATCH")
