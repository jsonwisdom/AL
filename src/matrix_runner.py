#!/usr/bin/env python3
"""Sovereign Replay Court — Core Runner
Deterministic, interpreter-agnostic verification matrix."""

import hashlib
import platform
import sys
from pathlib import Path

FIXTURES = {
    "AFP_MINIMAL_001": {
        "canonical": '{"key":"value","version":"1.0"}',
        "expected_sha256": "27e37c8d23fb3e1f841de98731d54241da2825f6bfdc78bc3f7c9b8100eeb812"
    },
    "AFP_NESTED_002": {
        "canonical": '{"children":[{"key":"a","value":1},{"key":"b","value":"string"},{"key":"nested","value":{"x":100,"y":200,"z":{"deep":true,"id":12345678901234567890}}}],"depth":4,"metadata":{"hash_algorithm":"blake2b","version":"AFP_NESTED_002"},"type":"nested_scope"}',
        "expected_sha256": "75fe512e17fd630336da1554228b68c1f821066b9b5d0d7b3c078101dabc0c3a"
    },
    "UNICODE_EDGE_002": {
        "canonical": '{"case":"unicode_normalization","expected_form":"NFC","fixture":"UNICODE_EDGE_002","pairs":[{"decomposed":"e\\u0301","label":"latin_e_acute","normalized":"\\u00e9"},{"decomposed":"A\\u030a","label":"latin_a_ring","normalized":"\\u00c5"},{"decomposed":"\\u212b","label":"angstrom_sign","normalized":"\\u00c5"}],"version":"1.0"}',
        "expected_sha256": "52336cd649d551e306837e6698557cc6fd53b5461c28a7b738a3e2868acbad25"
    }
}


def witness_identity():
    if Path("/.dockerenv").exists():
        return "CHAMBER_JUDGE"
    return "HOST_CLERK"


def verify_fixture(fixture_id, canonical_str, expected_root):
    actual = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()
    return actual == expected_root, actual


def main():
    witness = witness_identity()
    print(f"WITNESS: {witness}")
    print(f"PYTHON: {platform.python_version()}")

    failures = []
    for fixture_id, data in FIXTURES.items():
        passed, actual = verify_fixture(
            fixture_id,
            data["canonical"],
            data["expected_sha256"],
        )
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {fixture_id}: {actual}")
        if not passed:
            failures.append(
                f"{fixture_id}: expected {data['expected_sha256']}, got {actual}"
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
