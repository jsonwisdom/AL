#!/usr/bin/env python3
"""Sovereign Replay Court — Core Runner
Deterministic, interpreter-agnostic verification matrix."""

import hashlib
import sys

FIXTURES = {
    "AFP_MINIMAL_001": {
        "canonical": '{"key":"value","version":"1.0"}',
        "expected_sha256": "27e37c8d23fb3e1f841de98731d54241da2825f6bfdc78bc3f7c9b8100eeb812"
    },
    "AFP_NESTED_002": {
        "canonical": '{"children":[{"key":"a","value":1},{"key":"b","value":"string"},{"key":"nested","value":{"x":100,"y":200,"z":{"deep":true,"id":12345678901234567890}}}],"depth":4,"metadata":{"hash_algorithm":"blake2b","version":"AFP_NESTED_002"},"type":"nested_scope"}',
        "expected_sha256": "75fe512e17fd630336da1554228b68c1f821066b9b5d0d7b3c078101dabc0c3a"
    }
}


def verify_fixture(fixture_id, canonical_str, expected_root):
    actual = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()
    return actual == expected_root, actual


def main():
    failures = []
    for fixture_id, data in FIXTURES.items():
        passed, actual = verify_fixture(
            fixture_id,
            data["canonical"],
            data["expected_sha256"],
        )
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
