#!/usr/bin/env python3
"""
Epoch03 Membrane Level 3 Gate.

This validator is the sole constitutional witness emitter for the Epoch03
membrane. Witness strings are printed only after the evidence has replayed.
No workflow echo or wrapper may emit these strings lawfully.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    print("FAIL: missing dependency jsonschema", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs/specs/EPOCH03_CANONICAL_MEMBRANE_CONTRACT_V1_0_1.schema.json"
FIXTURE_DIR = ROOT / "fixtures/epoch03/membrane"
RUNTIME_LOG_PATH = ROOT / "fixtures/runtime/cw_recovery_log.json"

PASS_PATH = FIXTURE_DIR / "contract.pass.json"
FAIL_DUPLICATE_PATH = FIXTURE_DIR / "contract.fail.duplicate_recovery_field.json"
FAIL_MISSING_PREV_PATH = FIXTURE_DIR / "contract.fail.missing_previous_chain_hash.json"
FAIL_MISSING_OPERATOR_PATH = FIXTURE_DIR / "contract.fail.missing_operator_identity.json"

REQUIRED_RECOVERY_FIELDS = {
    "previous_chain_hash",
    "recovery_timestamp_utc",
    "recovery_reason",
    "operator_identity",
}
SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")


def die(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def require_path(obj: dict[str, Any], path: list[str]) -> Any:
    cur: Any = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            raise AssertionError(f"missing schema path: {'.'.join(path)}")
        cur = cur[key]
    return cur


def validate_pass(validator: Draft202012Validator, path: Path) -> bool:
    doc = load_json(path)
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            print(f"FAIL: {path} rejected at {list(err.path)}: {err.message}", file=sys.stderr)
        return False
    return True


def validate_fail(validator: Draft202012Validator, path: Path) -> bool:
    doc = load_json(path)
    errors = list(validator.iter_errors(doc))
    if not errors:
        print(f"FAIL: expected fixture to fail but it passed: {path}", file=sys.stderr)
        return False
    return True


def assert_schema_recovery_structure(schema: dict[str, Any]) -> None:
    recovery_fields = require_path(
        schema,
        ["properties", "recovery", "properties", "receipt_required_fields"],
    )
    if recovery_fields.get("minItems") != 4:
        raise AssertionError("receipt_required_fields.minItems must equal 4")
    if recovery_fields.get("uniqueItems") is not True:
        raise AssertionError("receipt_required_fields.uniqueItems must be true")

    all_of = recovery_fields.get("allOf")
    if not isinstance(all_of, list) or len(all_of) != 4:
        raise AssertionError("receipt_required_fields.allOf must contain four clauses")

    found: set[str] = set()
    for clause in all_of:
        try:
            const = clause["contains"]["const"]
        except Exception as exc:  # noqa: BLE001
            raise AssertionError("allOf clause must contain contains.const") from exc
        found.add(const)

    if found != REQUIRED_RECOVERY_FIELDS:
        raise AssertionError(f"recovery allOf constants mismatch: {sorted(found)}")


def validate_runtime_recovery_log(path: Path) -> bool:
    log = load_json(path)
    if not isinstance(log, dict):
        return False
    if log.get("log_id") != "cw_recovery_log":
        return False
    entries = log.get("entries")
    if not isinstance(entries, list) or not entries:
        return False

    previous_tail: str | None = None
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            return False
        if not REQUIRED_RECOVERY_FIELDS.issubset(entry.keys()):
            return False
        if not SHA256_RE.match(str(entry.get("previous_chain_hash"))):
            return False
        if not SHA256_RE.match(str(entry.get("restored_head_hash", ""))):
            return False
        if not SHA256_RE.match(str(entry.get("recovery_block_hash", ""))):
            return False
        if not entry.get("operator_identity"):
            return False
        if not entry.get("recovery_reason"):
            return False
        if not entry.get("recovery_timestamp_utc"):
            return False
        if previous_tail is not None and entry["previous_chain_hash"] != previous_tail:
            print(
                f"FAIL: runtime recovery log discontinuity at entry {index}",
                file=sys.stderr,
            )
            return False
        previous_tail = entry["recovery_block_hash"]
    return True


def main() -> int:
    try:
        schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        assert_schema_recovery_structure(schema)
    except Exception as exc:  # noqa: BLE001
        return die(f"schema integrity failed: {exc}")

    validator = Draft202012Validator(schema)

    if not validate_fail(validator, FAIL_DUPLICATE_PATH):
        return 1
    print("DUPLICATE_JSON_KEY_CONTAINS_CLASS_BLOCKED")

    if not validate_pass(validator, PASS_PATH):
        return 1
    if not validate_fail(validator, FAIL_MISSING_PREV_PATH):
        return 1
    if not validate_fail(validator, FAIL_MISSING_OPERATOR_PATH):
        return 1
    if not validate_runtime_recovery_log(RUNTIME_LOG_PATH):
        return die("runtime cw_recovery_log fixture failed validation")
    print("RECOVERY_RECEIPT_FIELDS_STRUCTURALLY_ENFORCED")

    print("EPOCH03_MEMBRANE_SCHEMA_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
