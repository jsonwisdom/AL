#!/usr/bin/env python3
"""
Epoch03 Canonical Membrane Schema Gate.

Validates the hardened membrane schema and recovery receipt field constraints.
This gate exists to prevent DUPLICATE_JSON_KEY_CONTAINS and partial recovery
receipt acceptance from re-entering the constitutional runtime.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    print("FAIL: missing dependency jsonschema", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs/specs/EPOCH03_CANONICAL_MEMBRANE_CONTRACT_V1_0_1.schema.json"
FIXTURE_DIR = ROOT / "fixtures/epoch03/membrane"
PASS_PATH = FIXTURE_DIR / "contract.pass.json"
FAIL_PATHS = [
    FIXTURE_DIR / "contract.fail.missing_previous_chain_hash.json",
    FIXTURE_DIR / "contract.fail.missing_operator_identity.json",
    FIXTURE_DIR / "contract.fail.duplicate_recovery_field.json",
]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    pass_doc = load_json(PASS_PATH)
    pass_errors = sorted(validator.iter_errors(pass_doc), key=lambda e: list(e.path))
    if pass_errors:
        print("FAIL: expected PASS fixture rejected")
        for err in pass_errors:
            print(f"  path={list(err.path)} message={err.message}")
        return 1

    for path in FAIL_PATHS:
        fail_doc = load_json(path)
        errors = list(validator.iter_errors(fail_doc))
        if not errors:
            print(f"FAIL: expected failing fixture passed: {path}")
            return 1

    print("EPOCH03_MEMBRANE_SCHEMA_GATE_PASS")
    print("DUPLICATE_JSON_KEY_CONTAINS_CLASS_BLOCKED")
    print("RECOVERY_RECEIPT_FIELDS_STRUCTURALLY_ENFORCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
