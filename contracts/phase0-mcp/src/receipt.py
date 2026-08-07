from __future__ import annotations

from typing import Any

from .canonicalize import sha256_value


def build_contract_receipt(
    *,
    fixture: dict[str, Any],
    adapter_commit_sha: str,
    test_command: str,
    exit_code: int,
    output: Any | None,
    result: str,
    failure_reason: str | None,
) -> dict[str, Any]:
    return {
        "input_fixture_sha256": sha256_value(fixture),
        "adapter_commit_sha": adapter_commit_sha,
        "test_command": test_command,
        "exit_code": exit_code,
        "output_sha256": None if output is None else sha256_value(output),
        "compatibility_result": result,
        "failure_reason": failure_reason,
        "authority": False,
    }
