#!/usr/bin/env python3
"""PUBLIC_VERIFIER_V1.

Minimal external verifier for replay membrane artifacts.
Authority: NONE.
This verifier checks evidence consistency only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SELF_EXCLUDED = "sha256:SELF_EXCLUDED"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return "0x" + hashlib.sha256(data).hexdigest()


def sha256_profile(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    return sha256_hex(canonical_json_bytes(value))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)

    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")

    return value


def assert_profile_hash(profile: dict[str, Any]) -> str:
    declared = profile.get("profile_hash")

    if not isinstance(declared, str):
        raise ValueError("profile_hash missing or invalid")

    excluded = dict(profile)
    excluded["profile_hash"] = SELF_EXCLUDED

    computed = sha256_profile(canonical_json_bytes(excluded))

    if computed != declared:
        raise ValueError(f"profile hash mismatch: {computed} != {declared}")

    return computed


def fail(reason: str) -> int:
    result = {
        "verifier_id": "PUBLIC_VERIFIER_V1",
        "verdict": "INVALID",
        "reason": reason,
        "authority": False,
    }

    print(json.dumps(result, sort_keys=True, indent=2))
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="public_verifier")

    parser.add_argument("--manifest", required=True)
    parser.add_argument("--comparison", required=True)
    parser.add_argument("--determinism-audit", required=True)
    parser.add_argument("--invariant-profile", required=True)
    parser.add_argument("--canon-profile", required=True)

    args = parser.parse_args(argv)

    try:
        manifest = load_json(Path(args.manifest))
        comparison = load_json(Path(args.comparison))
        determinism = load_json(Path(args.determinism_audit))
        invariant_profile = load_json(Path(args.invariant_profile))
        canon_profile = load_json(Path(args.canon_profile))

        invariant_hash = assert_profile_hash(invariant_profile)
        canon_hash = assert_profile_hash(canon_profile)

        if manifest.get("profile_hash_invariant") != invariant_hash:
            return fail("manifest invariant profile hash mismatch")

        if manifest.get("profile_hash_canon") != canon_hash:
            return fail("manifest canon profile hash mismatch")

        if determinism.get("invariant_profile_hash") != invariant_hash:
            return fail("determinism audit invariant profile hash mismatch")

        if determinism.get("canon_profile_hash") != canon_hash:
            return fail("determinism audit canon profile hash mismatch")

        if determinism.get("manifest_hash_1") != determinism.get("manifest_hash_2"):
            return fail("manifest determinism mismatch")

        if determinism.get("trace_hash_red_1") != determinism.get("trace_hash_red_2"):
            return fail("red trace determinism mismatch")

        if determinism.get("trace_hash_green_1") != determinism.get("trace_hash_green_2"):
            return fail("green trace determinism mismatch")

        if not comparison.get("opposite_lawful_outcomes"):
            return fail("comparison report does not assert opposite lawful outcomes")

        if manifest.get("authority") is True:
            return fail("authority claim present in manifest")

        if comparison.get("authority") is True:
            return fail("authority claim present in comparison report")

        if determinism.get("authority") is True:
            return fail("authority claim present in determinism audit report")

        result = {
            "verifier_id": "PUBLIC_VERIFIER_V1",
            "verdict": "VALID",
            "reason": "all public verification checks passed",
            "authority": False,
        }

        print(json.dumps(result, sort_keys=True, indent=2))
        return 0

    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
