#!/usr/bin/env python3
"""Sovereign Replay Court — Core Runner
Deterministic, interpreter-agnostic verification matrix."""

import hashlib
import platform
import sys
import tempfile
import unicodedata
from pathlib import Path

FIXTURES = {
    "AFP_MINIMAL_001": {
        "canonical": '{"key":"value","version":"1.0"}',
        "expected_sha256": "f0111a1ba3a390b5f42216d81d63d3753bf105d7f7800c5793873ff48fb9091c"
    },
    "AFP_NESTED_002": {
        "canonical": '{"children":[{"key":"a","value":1},{"key":"b","value":"string"},{"key":"nested","value":{"x":100,"y":200,"z":{"deep":true,"id":12345678901234567890}}}],"depth":4,"metadata":{"hash_algorithm":"blake2b","version":"AFP_NESTED_002"},"type":"nested_scope"}',
        "expected_sha256": "07923a377d908ade32545ddd226526bf73422785ad23a936d7aae3e0ee4746ca"
    },
    "UNICODE_EDGE_002": {
        "canonical": '{"case":"unicode_normalization","expected_form":"NFC","fixture":"UNICODE_EDGE_002","pairs":[{"decomposed":"é","label":"latin_e_acute","normalized":"é"},{"decomposed":"Å","label":"latin_a_ring","normalized":"Å"},{"decomposed":"Å","label":"angstrom_sign","normalized":"Å"}],"version":"1.0"}',
        "expected_sha256": "9825c293dc3c7dc1065e45bdc36e8f157ee16879e6078af0bfd997c32f0f6442"
    }
}


def witness_identity():
    if Path("/.dockerenv").exists():
        return "CHAMBER_JUDGE"
    return "HOST_CLERK"


def canonical_bytes(canonical_str):
    normalized = unicodedata.normalize("NFC", canonical_str)
    return normalized.encode("utf-8")


def filesystem_round_trip(canonical_str):
    normalized = unicodedata.normalize("NFC", canonical_str)
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=True) as handle:
        handle.write(normalized)
        handle.flush()
        handle.seek(0)
        observed = handle.read()
    return unicodedata.normalize("NFC", observed) == normalized


def verify_fixture(fixture_id, canonical_str, expected_root):
    actual = hashlib.sha256(canonical_bytes(canonical_str)).hexdigest()
    round_trip_ok = filesystem_round_trip(canonical_str)
    return actual == expected_root and round_trip_ok, actual, round_trip_ok


def main():
    witness = witness_identity()
    print(f"WITNESS: {witness}")
    print(f"PYTHON: {platform.python_version()}")
    print("NORMALIZATION: NFC")
    print("ENCODING: UTF-8")

    failures = []
    for fixture_id, data in FIXTURES.items():
        passed, actual, round_trip_ok = verify_fixture(
            fixture_id,
            data["canonical"],
            data["expected_sha256"],
        )
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {fixture_id}: {actual}")
        print(f"ROUND_TRIP: {fixture_id}: {'PASS' if round_trip_ok else 'FAIL'}")
        if not passed:
            failures.append(
                f"{fixture_id}: expected {data['expected_sha256']}, got {actual}, round_trip={round_trip_ok}"
            )

    if failures:
        print("❌ VERIFICATION FAILED")
        for failure in failures:
            print(f"  {failure}")
        sys.exit(1)

    print("✅ REPLAY_CONFIRMED")
    sys.exit(0)


if __name__ == "__main__":
    main()
