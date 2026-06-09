"""Deterministic verification harness for the ComputerWisdom validator.

This module compares validator output against fixture expected_state values.
It does not emit receipts, create authority, mutate the repository, or perform
network calls. Receipt generation is intentionally isolated in receipt_gen.py.
"""

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

try:
    from .validator import evaluate
except ImportError:  # pragma: no cover - supports direct script execution
    from validator import evaluate


TYPE_1_LOGIC_DEVIATION = "TYPE_1_LOGIC_DEVIATION"
TYPE_2_INVARIANT_BREACH = "TYPE_2_INVARIANT_BREACH"
TYPE_3_NON_DETERMINISTIC = "TYPE_3_NON_DETERMINISTIC"


@dataclass(frozen=True)
class VerificationResult:
    """One deterministic comparison between a fixture and validator output."""

    fixture_name: str
    expected_state: str
    evaluated_state: str
    verification_result: str
    failure_class: str | None


def classify_failure(expected_state: str, evaluated_state: str) -> str | None:
    """Classify state mismatch without changing validator behavior."""
    if expected_state == evaluated_state:
        return None
    return TYPE_1_LOGIC_DEVIATION


def verify_fixture(fixture: Mapping[str, Any]) -> VerificationResult:
    """Evaluate one fixture and return a pure verification result."""
    fixture_name = fixture["name"]
    input_data = fixture["input"]
    expected_state = fixture["expected_state"]
    evaluated_state = evaluate(input_data)
    failure_class = classify_failure(expected_state, evaluated_state)
    verification_result = "MATCH" if failure_class is None else "MISMATCH"

    return VerificationResult(
        fixture_name=fixture_name,
        expected_state=expected_state,
        evaluated_state=evaluated_state,
        verification_result=verification_result,
        failure_class=failure_class,
    )


def run_verification_suite(fixtures: Iterable[Mapping[str, Any]]) -> list[VerificationResult]:
    """Run validator verification over fixtures without side effects."""
    return [verify_fixture(fixture) for fixture in fixtures]


def suite_passed(results: Iterable[VerificationResult]) -> bool:
    """Return True only when every fixture matched its expected state."""
    return all(result.verification_result == "MATCH" for result in results)
