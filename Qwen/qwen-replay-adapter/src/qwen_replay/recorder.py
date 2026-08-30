from __future__ import annotations

import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from .schema import CallContext


class ReceiptRecorder:
    def __init__(
        self,
        *,
        mode: str = "OBSERVE",
        authorizer: Optional[Callable[[str, Any], bool]] = None,
        run_id: Optional[str] = None,
    ) -> None:
        if mode not in {"OBSERVE", "ENFORCE"}:
            raise ValueError("mode must be OBSERVE or ENFORCE")
        self.mode = mode
        self.authorizer = authorizer
        self.run_id = run_id or str(uuid.uuid4())
        self._lock = threading.Lock()
        self._next_call_index = 0
        self._local = threading.local()
        self.receipts: list[dict[str, Any]] = []

    def allocate_call_index(self) -> int:
        with self._lock:
            index = self._next_call_index
            self._next_call_index += 1
            return index

    def current_parent(self) -> Optional[int]:
        return getattr(self._local, "current_call_index", None)

    def begin_call(
        self,
        *,
        tool_name: str,
        requested_arguments_hash: str,
        executed_arguments_hash: str,
        parent_call_index: Optional[int],
        tool_version: str,
        start_timestamp: Optional[str] = None,
    ) -> CallContext:
        call_index = self.allocate_call_index()
        if parent_call_index is None:
            parent_call_index = self.current_parent()
        allowed = True
        if self.mode == "ENFORCE" and self.authorizer is not None:
            allowed = bool(self.authorizer(tool_name, requested_arguments_hash))
        context = CallContext(
            run_id=self.run_id,
            call_index=call_index,
            parent_call_index=parent_call_index,
            tool_name=tool_name,
            requested_arguments_hash=requested_arguments_hash,
            executed_arguments_hash=executed_arguments_hash,
            authorization="ALLOWED" if allowed else "DENIED",
            mode=self.mode,
            start_timestamp=start_timestamp or datetime.now(timezone.utc).isoformat(),
            tool_version=tool_version,
        )
        self._local.current_call_index = call_index
        return context

    def _append(self, receipt: dict[str, Any]) -> None:
        with self._lock:
            self.receipts.append(receipt)

    def record_success(self, context: CallContext, *, output_hash: str) -> None:
        data = context.to_dict()
        data.update({"execution_status": "COMPLETED", "output_hash": output_hash})
        self._append(data)
        self._local.current_call_index = context.parent_call_index

    def record_denial(self, context: CallContext) -> None:
        data = context.to_dict()
        data.update({"execution_status": "DENIED", "output_hash": None})
        self._append(data)
        self._local.current_call_index = context.parent_call_index

    def record_error(self, context: CallContext, *, error_type: str, error_message: str) -> None:
        data = context.to_dict()
        data.update({
            "execution_status": "FAILED",
            "output_hash": None,
            "error_type": error_type,
            "error_message": error_message,
        })
        self._append(data)
        self._local.current_call_index = context.parent_call_index
