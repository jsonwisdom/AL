#!/usr/bin/env python3
"""
Validate ALMS attestation candidates against v1 schema and graph rules.

- Enforces JSON Schema (v1)
- Enforces graph integrity via verify_attestation_graph.py

Usage:
  python scripts/validate_attestation_candidate.py _truth/anchors/*.json
"""

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path("schemas/ATTESTATION_CANDIDATE.v1.schema.json")


def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema(candidate_path: Path):
    schema = load_json(SCHEMA_PATH)
    candidate = load_json(candidate_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(candidate), key=lambda e: e.path)
    if errors:
        print(f"[FAIL] Schema validation errors in {candidate_path}:")
        for e in errors:
            print(f"  - {list(e.path)}: {e.message}")
        sys.exit(1)


def validate_graph(candidate_path: Path):
    result = subprocess.run(
        [sys.executable, "scripts/verify_attestation_graph.py", "--candidate", str(candidate_path)],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        sys.exit(result.returncode)


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_attestation_candidate.py <candidate.json> [more.json...]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"[FAIL] File not found: {p}")
            sys.exit(1)

        print(f"Validating candidate schema: {p}")
        validate_schema(p)

        print(f"Validating attestation graph: {p}")
        validate_graph(p)

        print(f"[OK] Candidate valid: {p}\n")


if __name__ == "__main__":
    main()
