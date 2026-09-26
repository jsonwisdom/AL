from __future__ import annotations

from .schema import VerificationResult

REQUIRED = {
    "run_id",
    "call_index",
    "tool_name",
    "requested_arguments_hash",
    "executed_arguments_hash",
    "authorization",
    "mode",
    "execution_status",
}


def verify_receipt(receipt: dict) -> VerificationResult:
    missing = REQUIRED - receipt.keys()
    if missing:
        if "requested_arguments_hash" in missing:
            return VerificationResult.fail("MISSING_REQUESTED_HASH")
        if "executed_arguments_hash" in missing:
            return VerificationResult.fail("MISSING_EXECUTED_HASH")
        return VerificationResult.fail("MISSING_REQUIRED_FIELD")

    if receipt["requested_arguments_hash"] != receipt["executed_arguments_hash"]:
        if not receipt.get("mutation_source"):
            return VerificationResult.fail("MUTATION_WITHOUT_SOURCE")

    status = receipt["execution_status"]
    if status == "COMPLETED" and not receipt.get("output_hash"):
        return VerificationResult.fail("MISSING_OUTPUT_HASH")
    if status in {"FAILED", "DENIED"} and receipt.get("output_hash") is not None:
        return VerificationResult.fail("UNEXPECTED_OUTPUT_HASH")
    return VerificationResult.pass_()
