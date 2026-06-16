#!/usr/bin/env python3
"""
E05 Resolver Replay Checker

Verifies the E05 ENS/IPFS discovery payload against local repository bytes.
Run from the jsonwisdom/AL repository root after pulling master.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "bundle_path": "bundles/e05/e05.discovery.bundle.json",
    "bundle_sha256": "60e117e759cf1f19375233dd59a5eac6076b1f4b0d7fe5d07dc0352dd778141c",
    "bundle_receipt_path": "receipts/e05/e05.discovery.bundle.sha256.txt",
    "artifact_path": "artifacts/epoch03/IMG_9629.png",
    "artifact_sha256": "36f3a099fe616ebd73f642b90d30b1dc9d05a4d65d8ad9e56070b36b55515b7e",
    "artifact_receipt_path": "receipts/epoch03/IMG_9629.sha256.txt",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_file(rel_path: str) -> Path:
    path = ROOT / rel_path
    if not path.is_file():
        raise SystemExit(f"FAIL_MISSING_FILE: {rel_path}")
    return path


def require_hash(rel_path: str, expected_hash: str) -> None:
    path = require_file(rel_path)
    observed = sha256_file(path)
    if observed != expected_hash:
        raise SystemExit(
            f"FAIL_HASH_MISMATCH: {rel_path}\nexpected={expected_hash}\nobserved={observed}"
        )
    print(f"PASS_SHA256 {rel_path} {observed}")


def require_receipt_contains(rel_path: str, expected_hash: str, expected_target: str) -> None:
    path = require_file(rel_path)
    text = path.read_text(encoding="utf-8")
    if expected_hash not in text or expected_target not in text:
        raise SystemExit(f"FAIL_RECEIPT_MISMATCH: {rel_path}")
    print(f"PASS_RECEIPT {rel_path}")


def main() -> None:
    require_hash(EXPECTED["bundle_path"], EXPECTED["bundle_sha256"])
    require_receipt_contains(
        EXPECTED["bundle_receipt_path"],
        EXPECTED["bundle_sha256"],
        EXPECTED["bundle_path"],
    )
    require_hash(EXPECTED["artifact_path"], EXPECTED["artifact_sha256"])
    require_receipt_contains(
        EXPECTED["artifact_receipt_path"],
        EXPECTED["artifact_sha256"],
        EXPECTED["artifact_path"],
    )
    print("MATCH_CONFIRMED E05_REPLAY_VERIFIED")


if __name__ == "__main__":
    main()
