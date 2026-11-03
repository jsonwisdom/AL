from __future__ import annotations

from typing import Any

from .canonicalize import parse_receipt_input, sha256_value
from .recorder import ReceiptRecorder


class AuditedTool:
    """Composition wrapper for a Qwen-compatible tool object."""

    def __init__(self, tool: Any, recorder: ReceiptRecorder):
        self._tool = tool
        self._recorder = recorder
        self.name = tool.name
        self.description = getattr(tool, "description", "")
        self.parameters = getattr(tool, "parameters", [])

    @property
    def file_access(self) -> bool:
        return bool(getattr(self._tool, "file_access", False))

    def call(self, params: str | dict, **kwargs: Any) -> Any:
        parent_call_index = kwargs.pop("parent_call_index", None)
        receipt_input = parse_receipt_input(params)
        requested_hash = sha256_value(receipt_input)
        executed_hash = sha256_value(parse_receipt_input(params))

        context = self._recorder.begin_call(
            tool_name=self.name,
            requested_arguments_hash=requested_hash,
            executed_arguments_hash=executed_hash,
            parent_call_index=parent_call_index,
            tool_version=str(getattr(self._tool, "version", "unknown")),
        )

        if context.authorization == "DENIED":
            self._recorder.record_denial(context)
            raise PermissionError(f"Tool denied: {self.name}")

        try:
            result = self._tool.call(params, **kwargs)
            self._recorder.record_success(context, output_hash=sha256_value(result))
            return result
        except Exception as error:
            self._recorder.record_error(
                context,
                error_type=type(error).__name__,
                error_message=str(error),
            )
            raise
