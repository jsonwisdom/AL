#!/usr/bin/env python3
"""
Proof Blob Membrane Compliance Tests

These tests enforce the constitutional boundary from specs/proof_blob_v0.1.md:
proof_blob objects may prove replay-visible procedural state only.
They must not emit or imply guilt, intent, corruption, moral status, or institutional legitimacy scores.
"""

import json
from pathlib import Path

FORBIDDEN_KEYS = {
    "guilt",
    "guilt_score",
    "intent",
    "intent_score",
    "corruption",
    "corruption_score",
    "fraud_score",
    "moral_score",
    "legitimacy_score",
    "institutional_reputation",
    "trust_score",
    "bad_actor_score",
    "culpability",
    "culpability_score",
}

FORBIDDEN_VALUE_TERMS = {
    "GUILTY",
    "CORRUPT",
    "CORRUPTION_LIKELY",
    "INTENT_PROVEN",
    "MOTIVE_PROVEN",
    "BAD_ACTOR",
    "ILLEGITIMATE_INSTITUTION",
}

ALLOWED_VERDICTS = {
    "FOUND",
    "NOT_FOUND",
    "REPLAY_FAIL",
    "REFUSAL_CAPTURE_R1",
    "REFUSAL_CAPTURE_R2",
    "REFUSAL_CAPTURE_R3",
    "MANIFEST_MISMATCH",
    "DOCKET_GAP",
    "EVIDENCE_INACCESSIBLE",
}


def walk_json(value):
    if isinstance(value, dict):
        for k, v in value.items():
            yield k, v
            yield from walk_json(v)
    elif isinstance(value, list):
        for item in value:
            yield from walk_json(item)


def assert_membrane(obj, source="<object>"):
    for key, value in walk_json(obj):
        assert key not in FORBIDDEN_KEYS, f"Forbidden proof_blob key {key!r} in {source}"
        if isinstance(value, str):
            assert value not in FORBIDDEN_VALUE_TERMS, f"Forbidden proof_blob value {value!r} in {source}"

    if obj.get("artifact") == "PROOF_BLOB_V0_1":
        verdict = obj.get("verdict")
        assert verdict in ALLOWED_VERDICTS, f"Unsupported proof_blob verdict {verdict!r} in {source}"


def test_good_404_proof_blob_passes():
    obj = {
        "artifact": "PROOF_BLOB_V0_1",
        "receipt_id": "404_R1_fixture",
        "track_id": "TRACK_404",
        "circuit_id": "404_v1",
        "target_url": "https://example.gov/missing.pdf",
        "canonical_hash": "sha256:abc",
        "crawl_timestamp": "2026-05-07T12:14:55Z",
        "verdict": "NOT_FOUND",
        "public_inputs": {
            "url_hash": "sha256:def",
            "expected_manifest_hash": "sha256:fed"
        },
        "proof_ref": "proofs/fixture.stark",
        "merkle_root": "sha256:123",
        "restricted_layer_ref": None,
        "state": "REPLAYABLE"
    }
    assert_membrane(obj, "good_404_fixture")


def test_forbidden_guilt_score_fails():
    obj = {
        "artifact": "PROOF_BLOB_V0_1",
        "receipt_id": "bad_fixture",
        "verdict": "NOT_FOUND",
        "guilt_score": 0.7
    }
    try:
        assert_membrane(obj, "bad_guilt_score_fixture")
    except AssertionError:
        return
    raise AssertionError("Forbidden guilt_score was accepted")


def test_forbidden_corruption_verdict_fails():
    obj = {
        "artifact": "PROOF_BLOB_V0_1",
        "receipt_id": "bad_fixture",
        "verdict": "CORRUPTION_LIKELY"
    }
    try:
        assert_membrane(obj, "bad_corruption_verdict_fixture")
    except AssertionError:
        return
    raise AssertionError("Forbidden corruption verdict was accepted")


if __name__ == "__main__":
    test_good_404_proof_blob_passes()
    test_forbidden_guilt_score_fails()
    test_forbidden_corruption_verdict_fails()
    print(json.dumps({
        "artifact": "PROOF_BLOB_MEMBRANE_TEST_RESULTS_V1",
        "verdict": "PASS"
    }, indent=2))
