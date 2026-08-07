from __future__ import annotations

import pytest

from qwen_replay import AuditedTool, ReceiptRecorder, verify_receipt
from conftest import FakeTool


def test_qv_001_normal_execution():
    tool = FakeTool(result={"answer": 42})
    recorder = ReceiptRecorder(run_id="RUN-001")
    wrapped = AuditedTool(tool, recorder)
    assert wrapped.call('{"x":1}') == {"answer": 42}
    assert tool.call_count == 1
    assert verify_receipt(recorder.receipts[0]).ok


def test_qv_003_policy_denial():
    tool = FakeTool()
    recorder = ReceiptRecorder(mode="ENFORCE", authorizer=lambda *_: False, run_id="RUN-003")
    wrapped = AuditedTool(tool, recorder)
    with pytest.raises(PermissionError):
        wrapped.call({"x": 1})
    assert tool.call_count == 0
    receipt = recorder.receipts[0]
    assert receipt["execution_status"] == "DENIED"
    assert verify_receipt(receipt).ok


def test_qv_004_tool_exception():
    error = RuntimeError("boom")
    tool = FakeTool(error=error)
    recorder = ReceiptRecorder(run_id="RUN-004")
    wrapped = AuditedTool(tool, recorder)
    with pytest.raises(RuntimeError, match="boom"):
        wrapped.call("raw code()")
    receipt = recorder.receipts[0]
    assert receipt["execution_status"] == "FAILED"
    assert receipt["error_type"] == "RuntimeError"
    assert verify_receipt(receipt).ok


def test_qv_005_deterministic_nested_graph():
    recorder = ReceiptRecorder(run_id="RUN-005")
    parent = AuditedTool(FakeTool(result="parent"), recorder)
    child_a = AuditedTool(FakeTool(result="a"), recorder)
    child_b = AuditedTool(FakeTool(result="b"), recorder)

    parent.call({"node": "parent"})
    child_a.call({"node": "a"}, parent_call_index=0)
    child_b.call({"node": "b"}, parent_call_index=0)

    assert [r["call_index"] for r in recorder.receipts] == [0, 1, 2]
    assert [r["parent_call_index"] for r in recorder.receipts] == [None, 0, 0]
    assert all(verify_receipt(r).ok for r in recorder.receipts)
