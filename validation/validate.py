#!/usr/bin/env python3
"""Fail-closed validator for the Gray Baby C01-C10 validation bundle."""
from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # fail closed
    raise SystemExit(f"jsonschema dependency missing: {exc}")

ROOT = Path(__file__).resolve().parent
PLAN_DIR = ROOT / "plans"
SCHEMA_DIR = ROOT / "schemas"
RECEIPT_PATH = ROOT / "validation_receipt.yaml"
EXPECTED_PLANS = [f"C{i:02d}.yaml" for i in range(1, 11)]
SCHEMAS = {
    "runtime": SCHEMA_DIR / "runtime-test-plan.schema.json",
    "receipt": SCHEMA_DIR / "test-receipt.schema.json",
    "authorization": SCHEMA_DIR / "test-authorization.schema.json",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def content_manifest_hash(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for path in sorted(paths, key=lambda p: p.as_posix()):
        rel = path.relative_to(ROOT).as_posix().encode("utf-8")
        h.update(rel)
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def format_error(filename: str, error: Any) -> str:
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{filename}:{location}: {error.message}"


def run_negative_tests(schema: dict[str, Any]) -> list[dict[str, Any]]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    valid_plan = {
        "test_id": "C01",
        "target_standard": "GB-015",
        "environment": {
            "type": "ISOLATED_TEST_ENVIRONMENT",
            "production_data": False,
            "external_side_effects": False,
            "environment_version": "NEGATIVE_TEST_FIXTURE",
        },
        "fixture": {
            "synthetic_data_only": True,
            "fixture_description": "Synthetic negative test fixture",
            "fixture_hash": "PENDING_UNTIL_CREATED",
        },
        "execution": {
            "entry_point": "NEGATIVE_TEST",
            "action": "Validate rejection behavior",
            "expected_stop_condition": "Invalid input must fail",
            "maximum_operations": 1,
            "timeout_seconds": 1,
        },
        "observations": {
            "expected_logs": [],
            "expected_receipts": [],
            "expected_state_changes": [],
            "forbidden_state_changes": [],
        },
        "safety": {
            "rollback_procedure": "No state created",
            "resource_limit": {"maximum_operations": 1},
            "network_scope": "FULLY_ISOLATED_NO_EXTERNAL_CALLS",
            "human_consent_required": True,
            "destructive_action": False,
        },
        "result": {
            "execution_state": "NOT_EXECUTED",
            "observed_result": "UNOBSERVED",
        },
        "authority": False,
    }

    cases: list[tuple[str, dict[str, Any]]] = []

    missing_action = deepcopy(valid_plan)
    del missing_action["execution"]["action"]
    cases.append(("MISSING_EXECUTION_ACTION", missing_action))

    authority_true = deepcopy(valid_plan)
    authority_true["authority"] = True
    cases.append(("AUTHORITY_TRUE", authority_true))

    invalid_enum = deepcopy(valid_plan)
    invalid_enum["result"]["observed_result"] = "GREEN"
    cases.append(("INVALID_RESULT_ENUM", invalid_enum))

    placeholder = {"test_id": "C01", "target_standard": "GB-015"}
    cases.append(("PLACEHOLDER_PLAN", placeholder))

    results = []
    for case_id, payload in cases:
        errors = list(validator.iter_errors(payload))
        results.append({
            "case_id": case_id,
            "expected": "REJECT",
            "observed": "REJECT" if errors else "ACCEPT",
            "error_count": len(errors),
            "result": "PASS" if errors else "FAIL",
        })
    return results


def main() -> int:
    errors: list[str] = []
    file_hashes: dict[str, str] = {}
    plan_data: list[dict[str, Any]] = []

    required_paths = list(SCHEMAS.values()) + [PLAN_DIR / name for name in EXPECTED_PLANS]
    for path in required_paths:
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")

    schemas: dict[str, dict[str, Any]] = {}
    if not errors:
        for name, path in SCHEMAS.items():
            try:
                schemas[name] = load_json(path)
                Draft202012Validator.check_schema(schemas[name])
                file_hashes[path.relative_to(ROOT).as_posix()] = sha256_bytes(path.read_bytes())
            except Exception as exc:
                errors.append(f"schema error {path.name}: {exc}")

    test_ids: list[str] = []
    if "runtime" in schemas:
        validator = Draft202012Validator(schemas["runtime"], format_checker=FormatChecker())
        for name in EXPECTED_PLANS:
            path = PLAN_DIR / name
            if not path.is_file():
                continue
            try:
                data = load_yaml(path)
                if not isinstance(data, dict):
                    errors.append(f"{name}: root must be an object")
                    continue
                plan_data.append(data)
                test_ids.append(str(data.get("test_id", "")))
                file_hashes[path.relative_to(ROOT).as_posix()] = sha256_bytes(path.read_bytes())
                for error in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
                    errors.append(format_error(name, error))
            except Exception as exc:
                errors.append(f"{name}: parse error: {exc}")

    duplicates = sorted({test_id for test_id in test_ids if test_ids.count(test_id) > 1})
    if duplicates:
        errors.append(f"duplicate test IDs: {', '.join(duplicates)}")

    expected_ids = {f"C{i:02d}" for i in range(1, 11)}
    actual_ids = set(test_ids)
    if actual_ids != expected_ids:
        errors.append(f"test ID set mismatch: expected={sorted(expected_ids)} actual={sorted(actual_ids)}")

    negative_tests = run_negative_tests(schemas["runtime"]) if "runtime" in schemas else []
    for test in negative_tests:
        if test["result"] != "PASS":
            errors.append(f"negative test failed: {test['case_id']}")

    manifest_paths = [path for path in required_paths if path.is_file()]
    receipt = {
        "validator_version": "0.3.1",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "files_checked": [path.relative_to(ROOT).as_posix() for path in manifest_paths],
        "file_hashes": file_hashes,
        "input_manifest_hash": content_manifest_hash(manifest_paths) if manifest_paths else None,
        "yaml_parse_result": "FAIL" if any("parse error" in e for e in errors) else "PASS",
        "schema_validation_result": "FAIL" if errors else "PASS",
        "enum_validation_result": "FAIL" if any("not one of" in e or "not in" in e for e in errors) else "PASS",
        "duplicate_test_ids": len(duplicates),
        "negative_tests": negative_tests,
        "unresolved_errors": errors,
        "exit_code": 1 if errors else 0,
        "authority": False,
    }

    RECEIPT_PATH.write_text(yaml.safe_dump(receipt, sort_keys=False), encoding="utf-8")
    print(yaml.safe_dump(receipt, sort_keys=False), end="")
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
