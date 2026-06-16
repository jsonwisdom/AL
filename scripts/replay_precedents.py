#!/usr/bin/env python3
"""Replay Court precedent replay harness.

Loads replay-court/precedents/*.json and verifies that recorded precedent
fixtures retain their expected verdicts and violation sets.

v0 is fixture-level replay: it protects validator evolution by making known
constitutional outcomes machine-checkable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PRECEDENTS_DIR = Path("replay-court/precedents")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_violations(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict) and "type" in item:
                out.append(str(item["type"]))
            else:
                raise ValueError(f"Unsupported violation item: {item!r}")
        return sorted(out)
    raise ValueError(f"Unsupported violations value: {value!r}")


def validate_fixture(path: Path) -> list[str]:
    data = load_json(path)
    errors: list[str] = []

    precedent_id = data.get("precedent_id")
    expected_verdict = data.get("expected_verdict")
    receipt = data.get("receipt", {})
    actual_verdict = receipt.get("verdict") or data.get("verdict")

    if not precedent_id:
        errors.append("missing precedent_id")
    if expected_verdict not in {"PASS", "FAIL"}:
        errors.append(f"invalid expected_verdict: {expected_verdict!r}")
    if actual_verdict != expected_verdict:
        errors.append(f"verdict mismatch: expected {expected_verdict!r}, got {actual_verdict!r}")

    expected_violations = normalize_violations(data.get("expected_violations"))
    actual_violations = normalize_violations(receipt.get("violations", data.get("violations", [])))

    if actual_violations != expected_violations:
        errors.append(
            "violation mismatch: "
            f"expected {expected_violations!r}, got {actual_violations!r}"
        )

    if data.get("protected_core_modified") is True:
        receipt_value = receipt.get("protected_core_modified")
        if receipt_value is not True:
            errors.append("protected_core_modified expected true but receipt did not confirm true")

    return errors


def main() -> int:
    fixture_paths = sorted(PRECEDENTS_DIR.glob("*.json"))
    if not fixture_paths:
        print("PRECEDENT_REPLAY_UNOBSERVED: no precedent fixtures found")
        return 0

    failed = False
    results: list[dict[str, Any]] = []

    for path in fixture_paths:
        errors = validate_fixture(path)
        result = {
            "fixture": str(path),
            "status": "FAIL" if errors else "PASS",
            "errors": errors,
        }
        results.append(result)
        if errors:
            failed = True

    print(json.dumps({"precedent_replay_results": results}, indent=2, sort_keys=True))

    if failed:
        print("PRECEDENT_REPLAY_FAIL")
        return 1

    print("PRECEDENT_REPLAY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
