from __future__ import annotations

import re
from typing import Any

from .canonicalize import sha256_value


_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class ContractError(ValueError):
    pass


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _require_nonempty_string(value: Any, code: str) -> None:
    if not isinstance(value, str) or not value:
        raise ContractError(code)


def _require_sha256(value: Any, code: str) -> None:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        raise ContractError(code)


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
    optional = {"normalized_result_sha256"}
    allowed = required | optional

    if not isinstance(receipt, dict):
        raise ContractError("RECEIPT_OBJECT_REQUIRED")

    unknown = set(receipt) - allowed
    missing = required - set(receipt)
    if unknown:
        raise ContractError(f"UNKNOWN_FIELDS:{','.join(sorted(unknown))}")
    if missing:
        raise ContractError(f"MISSING_FIELDS:{','.join(sorted(missing))}")

    _require_nonempty_string(receipt["run_id"], "RUN_ID_INVALID")

    if not _is_int(receipt["call_index"]) or receipt["call_index"] < 0:
        raise ContractError("CALL_INDEX_INVALID")

    parent_call_index = receipt["parent_call_index"]
    if parent_call_index is not None and (
        not _is_int(parent_call_index) or parent_call_index < 0
    ):
        raise ContractError("PARENT_CALL_INDEX_INVALID")

    _require_nonempty_string(receipt["tool_name"], "TOOL_NAME_INVALID")
    _require_nonempty_string(receipt["tool_version"], "TOOL_VERSION_INVALID")
    _require_sha256(receipt["requested_arguments_hash"], "REQUESTED_HASH_INVALID")
    _require_sha256(receipt["executed_arguments_hash"], "EXECUTED_HASH_INVALID")

    mutation_source = receipt["mutation_source"]
    if mutation_source is not None and not isinstance(mutation_source, str):
        raise ContractError("MUTATION_SOURCE_INVALID")

    if receipt["authorization"] not in {"ALLOWED", "DENIED"}:
        raise ContractError("AUTHORIZATION_INVALID")
    if receipt["mode"] not in {"OBSERVE", "ENFORCE"}:
        raise ContractError("MODE_INVALID")
    if receipt["execution_status"] not in {"COMPLETED", "FAILED", "DENIED"}:
        raise ContractError("UNKNOWN_EXECUTION_STATUS")

    output_hash = receipt["output_hash"]
    if output_hash is not None:
        _require_sha256(output_hash, "OUTPUT_HASH_INVALID")

    normalized_result = receipt.get("normalized_result_sha256")
    if normalized_result is not None:
        _require_sha256(normalized_result, "NORMALIZED_RESULT_HASH_INVALID")

    error = receipt["error"]
    if error is not None:
        if not isinstance(error, dict):
            raise ContractError("ERROR_OBJECT_INVALID")
        if set(error) != {"type", "message"}:
            raise ContractError("ERROR_FIELDS_INVALID")
        _require_nonempty_string(error["type"], "ERROR_TYPE_INVALID")
        if not isinstance(error["message"], str):
            raise ContractError("ERROR_MESSAGE_INVALID")

    if receipt["authority"] is not False:
        raise ContractError("AUTHORITY_MUST_BE_FALSE")

    if (
        receipt["requested_arguments_hash"] != receipt["executed_arguments_hash"]
        and not mutation_source
    ):
        raise ContractError("MUTATION_SOURCE_REQUIRED")

    status = receipt["execution_status"]
    if status == "COMPLETED":
        if output_hash is None or error is not None:
            raise ContractError("COMPLETED_RECEIPT_INVALID")
    elif status == "FAILED":
        if error is None:
            raise ContractError("FAILED_ERROR_REQUIRED")
    elif status == "DENIED":
        if receipt["authorization"] != "DENIED" or output_hash is not None:
            raise ContractError("DENIED_RECEIPT_INVALID")


def validate_signed_envelope(envelope: dict[str, Any]) -> None:
    if not isinstance(envelope, dict) or set(envelope) != {"receipt", "signature"}:
        raise ContractError("SIGNED_ENVELOPE_FIELDS_INVALID")

    validate_phase0_semantics(envelope["receipt"])

    signature = envelope["signature"]
    if not isinstance(signature, dict):
        raise ContractError("SIGNATURE_OBJECT_REQUIRED")
    if set(signature) != {"algorithm", "key_id", "signed_payload_hash", "value"}:
        raise ContractError("SIGNATURE_FIELDS_INVALID")
    if signature["algorithm"] != "TEST-SHA256":
        raise ContractError("SIGNATURE_ALGORITHM_UNSUPPORTED")

    _require_nonempty_string(signature["key_id"], "SIGNATURE_KEY_ID_INVALID")
    _require_sha256(signature["signed_payload_hash"], "SIGNED_PAYLOAD_HASH_INVALID")
    _require_sha256(signature["value"], "SIGNATURE_VALUE_INVALID")

    payload_hash = sha256_value(envelope["receipt"])
    if signature["signed_payload_hash"] != payload_hash:
        raise ContractError("SIGNED_PAYLOAD_HASH_MISMATCH")

    expected = sha256_value({"key_id": signature["key_id"], "payload_hash": payload_hash})
    if signature["value"] != expected:
        raise ContractError("SIGNATURE_VALUE_MISMATCH")
