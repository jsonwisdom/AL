#!/usr/bin/env python3
"""Verify ALMS Root Seal manifests.

Level 0 checks the identity of the minimal replay surface before
continuity drills, receipt replay, oath generation, or settlement framing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = [
    "seal_id",
    "version",
    "status",
    "repo",
    "branch",
    "includes",
    "file_hashes",
    "root_sha256",
    "law",
]


def fail(message: str) -> None:
    print(f"ROOT_SEAL_DIVERGED: {message}")
    raise SystemExit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_root(file_hashes: dict[str, str]) -> str:
    payload = json.dumps(file_hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        fail("seal is not a JSON object")
    return data


def verify(seal_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    seal = load_json(seal_path)

    for key in REQUIRED_TOP_LEVEL:
        if key not in seal:
            fail(f"missing required field: {key}")

    includes = seal.get("includes")
    if not isinstance(includes, list) or not includes:
        fail("includes must be a non-empty list")

    if len(includes) != len(set(includes)):
        fail("includes contains duplicate paths")

    pinned_hashes = seal.get("file_hashes")
    if not isinstance(pinned_hashes, dict):
        fail("file_hashes must be an object")

    computed: dict[str, str] = {}
    for rel_path in includes:
        if not isinstance(rel_path, str) or rel_path.startswith("/") or ".." in Path(rel_path).parts:
            fail(f"invalid include path: {rel_path}")
        file_path = repo_root / rel_path
        if not file_path.is_file():
            fail(f"missing included file: {rel_path}")
        computed[rel_path] = sha256_file(file_path)

    missing_pins = sorted(set(computed) - set(pinned_hashes))
    extra_pins = sorted(set(pinned_hashes) - set(computed))
    if missing_pins:
        fail(f"missing pinned hashes: {', '.join(missing_pins)}")
    if extra_pins:
        fail(f"extra pinned hashes: {', '.join(extra_pins)}")

    mismatches = [path for path in sorted(computed) if computed[path] != pinned_hashes.get(path)]
    if mismatches:
        fail("hash mismatch: " + ", ".join(mismatches))

    computed_root = canonical_root(computed)
    if computed_root != seal.get("root_sha256"):
        fail(f"root mismatch: recorded={seal.get('root_sha256')} computed={computed_root}")

    print("ROOT_SEAL_CONFIRMED")
    print(f"seal_id: {seal.get('seal_id')}")
    print(f"version: {seal.get('version')}")
    print(f"included_files: {len(includes)}")
    print(f"root_sha256: {computed_root}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an ALMS root seal manifest.")
    parser.add_argument("seal", help="Path to root seal JSON")
    args = parser.parse_args()
    verify(Path(args.seal))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
