#!/usr/bin/env python3
"""
Strict acceptance runner for ALMS Claim Extractor v0.1.

This runner compares extractor output against golden fixtures byte-for-byte
at the canonical JSON object level. Any drift exits non-zero.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[3]
EXTRACTOR_DIR = ROOT / "claims" / "extractor"
GOLDEN_DIR = EXTRACTOR_DIR / "tests" / "fixtures" / "golden"

sys.path.insert(0, str(EXTRACTOR_DIR))

from extractor import ClaimExtractor  # noqa: E402


CASES = {
    "001_simple_claim": ["001_simple_claim.json"],
    "002_multi_claim_split": [
        "002_multi_claim_split_1.json",
        "002_multi_claim_split_2.json",
    ],
    "003_refusal_vague": ["003_refusal_vague.json"],
    "004_contradiction": ["004_contradiction.json"],
    "005_unicode_canonical": ["005_unicode_canonical.json"],
}


REQUIRED_TOP_LEVEL = {
    "claim_id",
    "ingestion_id",
    "version",
    "extracted_claim",
    "confidence",
    "needs_clarification",
    "context_window",
    "normalization",
    "raw_hash",
    "candidate_canonical_hash",
    "regime",
}

ALLOWED_TOP_LEVEL = REQUIRED_TOP_LEVEL


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def assert_schema_shape(fixture: Dict[str, Any]) -> None:
    keys = set(fixture.keys())
    if keys != REQUIRED_TOP_LEVEL:
        missing = sorted(REQUIRED_TOP_LEVEL - keys)
        extra = sorted(keys - ALLOWED_TOP_LEVEL)
        raise AssertionError(f"schema key mismatch missing={missing} extra={extra}")

    if fixture["version"] != "fixture-v1":
        raise AssertionError("version must be fixture-v1")

    if fixture["normalization"] != {
        "unicode": "NFC",
        "whitespace": "canonical",
        "case": "preserve",
        "json": "JCS",
    }:
        raise AssertionError("normalization object mismatch")

    if fixture["regime"].get("canonicalizer") != "ALMS_EXTRACTOR_V1":
        raise AssertionError("canonicalizer mismatch")

    if not isinstance(fixture["candidate_canonical_hash"], str):
        raise AssertionError("candidate_canonical_hash must be string")

    if not fixture["candidate_canonical_hash"].startswith("sha256:"):
        raise AssertionError("candidate_canonical_hash must use sha256: prefix")

    if fixture["confidence"] >= 0.95:
        if fixture["needs_clarification"] is not False:
            raise AssertionError("high confidence fixture must not need clarification")
        if not isinstance(fixture["extracted_claim"], str):
            raise AssertionError("high confidence fixture must include extracted_claim")
    else:
        if fixture["needs_clarification"] is not True:
            raise AssertionError("low confidence fixture must need clarification")
        if fixture["extracted_claim"] is not None:
            raise AssertionError("low confidence fixture must null extracted_claim")


def assert_hashes(raw_text: str, fixture: Dict[str, Any]) -> None:
    if fixture["raw_hash"] != sha256_text(raw_text):
        raise AssertionError(f"raw_hash mismatch for {fixture['claim_id']}")

    without_candidate = dict(fixture)
    expected_candidate = without_candidate.pop("candidate_canonical_hash")
    actual_candidate = "sha256:" + hashlib.sha256(
        canonical_json(without_candidate).encode("utf-8")
    ).hexdigest()
    if expected_candidate != actual_candidate:
        raise AssertionError(f"candidate_canonical_hash mismatch for {fixture['claim_id']}")


def run_case(case_name: str, expected_files: List[str]) -> None:
    raw_path = GOLDEN_DIR / f"{case_name}.txt"
    raw_text = raw_path.read_text(encoding="utf-8").strip()
    expected = [load_json(GOLDEN_DIR / filename) for filename in expected_files]

    ingestion_id = expected[0]["ingestion_id"]
    extractor = ClaimExtractor()
    actual = extractor.extract_claims({"ingestion_id": ingestion_id, "raw_text": raw_text})

    if actual != expected:
        print(f"\n❌ DRIFT: {case_name}")
        print("Expected:")
        print(json.dumps(expected, indent=2, ensure_ascii=False))
        print("Actual:")
        print(json.dumps(actual, indent=2, ensure_ascii=False))
        raise AssertionError(f"golden mismatch: {case_name}")

    for fixture in actual:
        assert_schema_shape(fixture)
        assert_hashes(raw_text, fixture)

    print(f"✅ {case_name}: {len(actual)} fixture(s)")


def main() -> int:
    print("🧪 ALMS Claim Extractor — strict golden acceptance")
    for case_name, expected_files in CASES.items():
        run_case(case_name, expected_files)
    print("\n✅ CLAIM_EXTRACTOR_ACCEPTANCE_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
