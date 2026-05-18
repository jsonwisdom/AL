#!/usr/bin/env python3
"""Verify ALMS Root Seal manifests.

Level 0 checks the identity of the minimal replay surface before
continuity drills, receipt replay, oath generation, or settlement framing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = [
    "seal_id",
    "seal_format_version",
    "version",
    "seal_type",
    "status",
    "repo",
    "branch",
    "commit",
    "includes",
    "law",
    "hash_algorithm",
    "canonicalization",
    "previous_seal_root",
    "file_hashes",
    "root_sha256",
]

REQUIRED_CANONICALIZATION = {
    "json_sort_keys": True,
    "utf8_no_bom": True,
    "newline": "LF",
    "path_sort": "lexicographic",
    "file_hash_sort": "lexicographic",
}

SEAL_ID_RE = re.compile(r"^ALMS_ROOT_\d{3}_REPLAY_SEAL$")
VERSION_RE = re.compile(r"^\d{3}$")
FORMAT_VERSION_RE = re.compile(r"^0\.\d+$")
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


def fail(message: str) -> None:
    print(f"ROOT_SEAL_DIVERGED: {message}")
    raise SystemExit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        raw = handle.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(f"UTF-8 BOM detected: {path}")
    if b"\r\n" in raw or b"\r" in raw:
        fail(f"non-LF newline detected: {path}")
    digest.update(raw)
    return digest.hexdigest()


def canonical_root(file_hashes: dict[str, str]) -> str:
    ordered = {key: file_hashes[key] for key in sorted(file_hashes)}
    payload = json.dumps(ordered, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        raw = handle.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(f"UTF-8 BOM detected: {path}")
    if b"\r\n" in raw or b"\r" in raw:
        fail(f"non-LF newline detected: {path}")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        fail("seal is not a JSON object")
    return data


def require_regex(name: str, value: Any, pattern: re.Pattern[str]) -> None:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        fail(f"invalid {name}: {value}")


def verify(seal_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    seal = load_json(seal_path)

    for key in REQUIRED_TOP_LEVEL:
        if key not in seal:
            fail(f"missing required field: {key}")

    require_regex("seal_id", seal.get("seal_id"), SEAL_ID_RE)
    require_regex("seal_format_version", seal.get("seal_format_version"), FORMAT_VERSION_RE)
    require_regex("version", seal.get("version"), VERSION_RE)
    require_regex("commit", seal.get("commit"), COMMIT_RE)

    if seal.get("seal_type") not in {"identity_root", "epoch_seal"}:
        fail(f"invalid seal_type: {seal.get('seal_type')}")
    if seal.get("hash_algorithm") != "sha256":
        fail(f"unsupported hash_algorithm: {seal.get('hash_algorithm')}")

    previous = seal.get("previous_seal_root")
    if previous is not None:
        require_regex("previous_seal_root", previous, SHA256_RE)

    canonicalization = seal.get("canonicalization")
    if canonicalization != REQUIRED_CANONICALIZATION:
        fail("canonicalization rules mismatch")

    includes = seal.get("includes")
    if not isinstance(includes, list) or not includes:
        fail("includes must be a non-empty list")
    if any(not isinstance(path, str) for path in includes):
        fail("includes must contain only strings")
    if includes != sorted(includes):
        fail("includes must be lexicographically sorted")
    if len(includes) != len(set(includes)):
        fail("includes contains duplicate paths")

    pinned_hashes = seal.get("file_hashes")
    if not isinstance(pinned_hashes, dict):
        fail("file_hashes must be an object")
    if list(pinned_hashes.keys()) != sorted(pinned_hashes.keys()):
        fail("file_hashes keys must be lexicographically sorted")

    computed: dict[str, str] = {}
    for rel_path in includes:
        rel = Path(rel_path)
        if rel_path.startswith("/") or ".." in rel.parts:
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

    for rel_path, digest in pinned_hashes.items():
        require_regex(f"file_hashes[{rel_path}]", digest, SHA256_RE)

    mismatches = [path for path in sorted(computed) if computed[path] != pinned_hashes.get(path)]
    if mismatches:
        fail("hash mismatch: " + ", ".join(mismatches))

    computed_root = canonical_root(computed)
    require_regex("root_sha256", seal.get("root_sha256"), SHA256_RE)
    if computed_root != seal.get("root_sha256"):
        fail(f"root mismatch: recorded={seal.get('root_sha256')} computed={computed_root}")

    print("ROOT_SEAL_CONFIRMED")
    print(f"seal_id: {seal.get('seal_id')}")
    print(f"seal_format_version: {seal.get('seal_format_version')}")
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
