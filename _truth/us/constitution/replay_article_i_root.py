#!/usr/bin/env python3
"""
ALMS public replay verifier for Article I.

This script verifies the Article I aggregate root from repo-resident manifests.
It accepts local repo files by default and can be adapted to raw GitHub fetches.

Rule: ALMS_GLOBAL_MERKLE_RULE_V1
- section leaf = SHA256(section_id + ':' + section_root_sha256)
- parent = SHA256(left_raw_digest || right_raw_digest)
- odd leaf promoted unchanged
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_ARTICLE_I_ROOT = "2c595278a5a1ecbafd00544bdcd81a5473b4a13775950d5300e2b44c1bbcd518"
RULE_ID = "ALMS_GLOBAL_MERKLE_RULE_V1"
SECTIONS = [
    ("USC-A1-S8", ROOT / "a1_s8_merkle_manifest.json"),
    ("USC-A1-S9", ROOT / "a1_s9_merkle_manifest.json"),
    ("USC-A1-S10", ROOT / "a1_s10_merkle_manifest.json"),
]


def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def read_section_root(section_id: str, path: Path) -> str:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("rule_id") != RULE_ID:
        raise SystemExit(f"BLOCKED: {path} rule mismatch: {manifest.get('rule_id')}")
    root = manifest.get("root_sha256")
    if not isinstance(root, str) or len(root) != 64:
        raise SystemExit(f"BLOCKED: {path} missing 64-hex root_sha256")
    int(root, 16)
    return root


def compute_article_root() -> str:
    leaves = []
    for section_id, path in SECTIONS:
        section_root = read_section_root(section_id, path)
        leaves.append(sha256_bytes(f"{section_id}:{section_root}".encode("utf-8")))
    h89 = sha256_bytes(leaves[0] + leaves[1])
    article_root = sha256_bytes(h89 + leaves[2]).hex()
    return article_root


def main() -> int:
    root = compute_article_root()
    print(json.dumps({
        "artifact": "USC_ARTICLE_I_PUBLIC_REPLAY",
        "rule_id": RULE_ID,
        "computed_article_i_root_sha256": root,
        "expected_article_i_root_sha256": EXPECTED_ARTICLE_I_ROOT,
        "status": "PASS" if root == EXPECTED_ARTICLE_I_ROOT else "FAIL",
    }, sort_keys=True))
    return 0 if root == EXPECTED_ARTICLE_I_ROOT else 1


if __name__ == "__main__":
    raise SystemExit(main())
