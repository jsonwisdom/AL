from __future__ import annotations


class FakeTool:
    name = "fake_tool"
    description = "Deterministic fake tool"
    parameters = {"type": "object"}
    file_access = False
    version = "1.0"

    def __init__(self, result=None, error=None):
        self.result = result if result is not None else {"ok": True}
        self.error = error
        self.call_count = 0
        self.last_params = None

    def call(self, params, **kwargs):
        self.call_count += 1
        self.last_params = params
        if self.error:
            raise self.error
        return self.result
