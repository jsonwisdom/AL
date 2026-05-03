#!/usr/bin/env python3
"""Validate ALMS version registry and version receipts against JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate
except Exception as exc:
    print(f"JSONSCHEMA_IMPORT_FAIL {exc}")
    sys.exit(2)

REGISTRY = Path("alms/version_registry.json")
REGISTRY_SCHEMA = Path("schemas/alms_version_registry.schema.json")
RECEIPT_SCHEMA = Path("schemas/alms_version_receipt.schema.json")
RECEIPT_DIR = Path("alms/version_receipts")


def load_json(path: Path):
    return json.loads(path.read_text())


def main() -> int:
    required = [REGISTRY, REGISTRY_SCHEMA, RECEIPT_SCHEMA]
    for path in required:
        if not path.exists():
            print(f"MISSING_REQUIRED_FILE {path}")
            return 1

    validate(instance=load_json(REGISTRY), schema=load_json(REGISTRY_SCHEMA))
    print(f"REGISTRY_SCHEMA_PASS {REGISTRY}")

    if RECEIPT_DIR.exists():
        schema = load_json(RECEIPT_SCHEMA)
        for receipt_path in sorted(RECEIPT_DIR.glob("*.json")):
            validate(instance=load_json(receipt_path), schema=schema)
            print(f"RECEIPT_SCHEMA_PASS {receipt_path}")
    else:
        print("NO_VERSION_RECEIPTS_YET")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
