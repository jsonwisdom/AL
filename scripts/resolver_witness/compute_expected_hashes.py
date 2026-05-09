#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATES_DIR = ROOT / "tests" / "resolver_witness" / "fixtures" / "expected_graph_states"

ORDERED_FILES = [
    "convergence_001.json",
    "convergence_002_hash_mismatch.json",
    "convergence_003_revocable_parent.json",
    "convergence_004_missing_attestation.json",
    "convergence_005_schema_violation.json",
]


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main():
    registry = {}
    for filename in ORDERED_FILES:
        obj = json.loads((STATES_DIR / filename).read_text(encoding="utf-8"))
        test_id = obj["test_id"]
        registry[test_id] = hashlib.sha256(canonical_serialize(obj)).hexdigest()
    print(json.dumps(registry, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
