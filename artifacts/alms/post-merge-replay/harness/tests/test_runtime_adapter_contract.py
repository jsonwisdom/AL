from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "runtime_adapter_protocol.json"
ADAPTER_PATH = ROOT / "adapters" / "subprocess_adapter.py"
BEDROCK_SHA = "59448d850d355854956cb5834ebef17f7f14c7dc"
EXPECTED_IDS = ["F001", "F002", "F003", "F004", "F005", "F006"]

spec = importlib.util.spec_from_file_location("subprocess_adapter", ADAPTER_PATH)
assert spec and spec.loader
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def matrix() -> list[dict[str, str]]:
    return [
        {
            "failure_id": failure_id,
            "name": f"vector_{failure_id}",
            "expected_state": "CONTAINED",
        }
        for failure_id in EXPECTED_IDS
    ]


def valid_output() -> dict:
    return {
        "adapter_version": "1.0.0",
        "bedrock_sha": BEDROCK_SHA,
        "vectors": [
            {
                "failure_id": failure_id,
                "name": f"vector_{failure_id}",
                "injected": True,
                "observed_state": "CONTAINED",
                "expected_state": "CONTAINED",
                "events": [{"kind": "observation", "detail": failure_id}],
                "counter_before": index,
                "counter_after": index + 1,
            }
            for index, failure_id in enumerate(EXPECTED_IDS)
        ],
    }


class RuntimeAdapterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.protocol = json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))

    def test_valid_six_vector_output_matches_protocol(self) -> None:
        errors = list(Draft202012Validator(self.protocol).iter_errors(valid_output()))
        self.assertEqual(errors, [])

    def test_wrong_sha_is_rejected_before_runtime_execution(self) -> None:
        with self.assertRaisesRegex(ValueError, "bedrock SHA must equal"):
            adapter.run_all_vectors(
                matrix(),
                "0" * 40,
                Path("./cvd_runtime"),
                self.protocol,
            )

    def test_all_six_vectors_are_required_in_order(self) -> None:
        with self.assertRaisesRegex(ValueError, "ordered F001-F006"):
            adapter.run_all_vectors(
                matrix()[:-1],
                BEDROCK_SHA,
                Path("./cvd_runtime"),
                self.protocol,
            )

    def test_inactive_vector_is_rejected_by_protocol(self) -> None:
        output = valid_output()
        output["vectors"][0]["injected"] = False
        errors = list(Draft202012Validator(self.protocol).iter_errors(output))
        self.assertTrue(errors)

    def test_empty_events_are_rejected_by_protocol(self) -> None:
        output = valid_output()
        output["vectors"][0]["events"] = []
        errors = list(Draft202012Validator(self.protocol).iter_errors(output))
        self.assertTrue(errors)

    def test_counter_regression_fails_closed(self) -> None:
        runtime_results = []
        for index, failure in enumerate(matrix()):
            runtime_results.append(
                {
                    "failure_id": failure["failure_id"],
                    "injected": True,
                    "observed_state": "CONTAINED",
                    "events": [{"kind": "observation", "detail": failure["failure_id"]}],
                    "counter_before": index + 1,
                    "counter_after": index if index == 2 else index + 2,
                }
            )
        with patch.object(adapter, "run_vector_subprocess", side_effect=runtime_results):
            with self.assertRaisesRegex(RuntimeError, "counter regression"):
                adapter.run_all_vectors(
                    matrix(), BEDROCK_SHA, Path("./cvd_runtime"), self.protocol
                )

    def test_state_mismatch_fails_closed(self) -> None:
        runtime_results = []
        for index, failure in enumerate(matrix()):
            runtime_results.append(
                {
                    "failure_id": failure["failure_id"],
                    "injected": True,
                    "observed_state": "WRONG" if index == 0 else "CONTAINED",
                    "events": [{"kind": "observation", "detail": failure["failure_id"]}],
                    "counter_before": index,
                    "counter_after": index + 1,
                }
            )
        with patch.object(adapter, "run_vector_subprocess", side_effect=runtime_results):
            with self.assertRaisesRegex(RuntimeError, "observed 'WRONG'"):
                adapter.run_all_vectors(
                    matrix(), BEDROCK_SHA, Path("./cvd_runtime"), self.protocol
                )


if __name__ == "__main__":
    unittest.main()
