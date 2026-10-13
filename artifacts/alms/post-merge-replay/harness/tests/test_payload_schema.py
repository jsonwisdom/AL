from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"
BEDROCK_SHA = "59448d850d355854956cb5834ebef17f7f14c7dc"


def valid_payload() -> dict:
    results = []
    states = [
        "ALARM",
        "DEGRADED",
        "CRITICAL",
        "CRITICAL",
        "CRITICAL_FAIL_CLOSED",
        "STABLE_PREVIOUS_STATE",
    ]
    for index, state in enumerate(states):
        failure_id = f"F{index + 1:03d}"
        results.append(
            {
                "failure_id": failure_id,
                "vector": f"vector_{failure_id}",
                "injected": True,
                "observed_state": state,
                "expected_state": state,
                "passed": True,
                "events": [
                    {
                        "sequence": index,
                        "event": "observed containment",
                        "observed_state": state,
                        "evidence_sha256": f"{index + 1:064x}",
                    }
                ],
                "counters_before": index,
                "counters_after": index + 1,
                "recovery_action": "retain constitutional state",
                "blast_radius": "isolated test vector",
            }
        )
    return {
        "cro_id": "CRO-PAYLOAD-TEST-001",
        "replay_root": BEDROCK_SHA,
        "bedrock_sha": BEDROCK_SHA,
        "replay_started_at": "2026-07-15T16:00:00Z",
        "replay_completed_at": "2026-07-15T16:00:00Z",
        "replay_verdict": {
            "status": "GREEN",
            "reason": "All vectors contained and counters monotonic.",
        },
        "failure_results": results,
        "monotonic_counters": {"before": 0, "after": 6, "monotonic": True},
    }


class PayloadSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload_schema = json.loads(
            (SCHEMAS / "CRO.payload.schema.json").read_text(encoding="utf-8")
        )
        cls.receipt_schema = json.loads(
            (SCHEMAS / "CRO.schema.json").read_text(encoding="utf-8")
        )
        cls.format_checker = FormatChecker()

    def errors(self, schema: dict, instance: dict) -> list:
        validator = Draft202012Validator(
            schema, format_checker=self.format_checker
        )
        return list(validator.iter_errors(instance))

    def test_unsigned_green_payload_satisfies_payload_schema(self) -> None:
        self.assertEqual(self.errors(self.payload_schema, valid_payload()), [])

    def test_unsigned_payload_does_not_satisfy_final_receipt_schema(self) -> None:
        errors = self.errors(self.receipt_schema, valid_payload())
        self.assertTrue(errors)
        self.assertTrue(any("signature_chain" in error.message for error in errors))

    def test_signature_chain_is_forbidden_in_payload(self) -> None:
        payload = valid_payload()
        payload["signature_chain"] = []
        self.assertTrue(self.errors(self.payload_schema, payload))

    def test_wrong_bedrock_is_rejected(self) -> None:
        payload = valid_payload()
        payload["bedrock_sha"] = "0" * 40
        self.assertTrue(self.errors(self.payload_schema, payload))

    def test_red_or_failed_vector_cannot_masquerade_as_green(self) -> None:
        payload = valid_payload()
        payload["failure_results"][0]["passed"] = False
        self.assertFalse(
            all(item["passed"] for item in payload["failure_results"]),
            "GREEN derivation must fail when any vector is not passed",
        )


if __name__ == "__main__":
    unittest.main()
