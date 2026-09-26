from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class CallContext:
    run_id: str
    call_index: int
    parent_call_index: Optional[int]
    tool_name: str
    requested_arguments_hash: str
    executed_arguments_hash: str
    authorization: str
    mode: str
    start_timestamp: str
    tool_version: str
    mutation_source: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VerificationResult:
    ok: bool
    code: str

    @classmethod
    def pass_(cls) -> "VerificationResult":
        return cls(True, "PASS")

    @classmethod
    def fail(cls, code: str) -> "VerificationResult":
        return cls(False, code)
