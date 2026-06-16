import copy

import pytest

from lineage.pending_claims_v1 import (
    COALESCED,
    DUPLICATE_CLAIM,
    NEW_CLAIM,
    process_claim,
)

HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64
TRACE_HASH = "sha256:" + "c" * 64
OUTPUT_COMMITMENT = "sha256:" + "d" * 64
MANIFEST_HASH = "sha256:" + "e" * 64

TEST_POLICY = {
    "policy_version": "NAMESPACE_POLICY_V1",
    "protected_namespaces": [
        {
            "namespace_id": "ns-internal",
            "pattern": "doc:internal-*",
            "protection_mode": "LOCAL_ONLY",
            "alert_on_violation": True,
            "exceptions": [],
        },
        {
            "namespace_id": "ns-shared",
            "pattern": "doc:shared-*",
            "protection_mode": "ALLOW",
            "alert_on_violation": False,
            "exceptions": [],
        },
    ],
    "default_rule": {
        "protection_mode": "QUARANTINE",
        "description": "Unrecognized namespaces require manual review before admission.",
    },
}


def base_claim(**overrides):
    claim = {
        "asset_id": "doc:shared-research-042",
        "asset_hash": HASH_A,
        "trace_hash": TRACE_HASH,
        "output_commitment": OUTPUT_COMMITMENT,
        "manifest_hash": MANIFEST_HASH,
        "origin": "E1-PRIME",
        "signature": "sig-e1",
        "timestamp_utc": "2026-05-07T00:00:00Z",
    }
    claim.update(overrides)
    return claim


def valid_receipt(**overrides):
    receipt = {
        "receipt_type": "VERIFIER_RECEIPT_V1",
        "verifier_version": "CBREv1.2+",
        "opcode_table_id": "0x0001",
        "trace_status": "VERIFIED_TRACE",
        "trace_hash": TRACE_HASH,
        "output_commitment": OUTPUT_COMMITMENT,
        "verified_at_utc": "2026-05-07T00:00:01Z",
    }
    receipt.update(overrides)
    return receipt


def test_local_only_external_claim_rejected_before_pending_mutation():
    pending = []
    claim = base_claim(asset_id="doc:internal-secret-99", origin="E1-PRIME")

    with pytest.raises(ValueError) as exc:
        process_claim(claim, valid_receipt(), pending, namespace_policy=TEST_POLICY)

    assert "NAMESPACE_REJECTED" in str(exc.value)
    assert pending == []


def test_quarantine_unknown_namespace_rejected_before_pending_mutation():
    pending = []
    claim = base_claim(asset_id="doc:unknown-novel-asset", origin="E1-PRIME")

    with pytest.raises(ValueError) as exc:
        process_claim(claim, valid_receipt(), pending, namespace_policy=TEST_POLICY)

    assert "NAMESPACE_REJECTED" in str(exc.value)
    assert "QUARANTINED" in str(exc.value)
    assert pending == []


def test_allowed_namespace_bad_receipt_rejected_before_pending_mutation():
    pending = []
    claim = base_claim()
    bad_receipt = valid_receipt(trace_hash="sha256:" + "f" * 64)

    with pytest.raises(ValueError) as exc:
        process_claim(claim, bad_receipt, pending, namespace_policy=TEST_POLICY)

    assert "REJECTED_TRACE: TRACE_HASH_MISMATCH" in str(exc.value)
    assert pending == []


def test_allowed_namespace_good_receipt_creates_new_claim():
    pending = []
    claim = base_claim()

    status, updated = process_claim(claim, valid_receipt(), pending, namespace_policy=TEST_POLICY)

    assert status == NEW_CLAIM
    assert len(updated) == 1
    assert updated[0]["asset_id"] == claim["asset_id"]
    assert updated[0]["asset_hash"] == claim["asset_hash"]
    assert updated[0]["trace_status"] == "VERIFIED_TRACE"
    assert updated[0]["adoption_status"] == "ELIGIBLE"
    assert updated[0]["attestors"][0]["branch_id"] == "E1-PRIME"


def test_same_hash_new_origin_coalesces_attestor():
    pending = []
    claim_a = base_claim(origin="E1-PRIME", signature="sig-e1")
    status, pending = process_claim(claim_a, valid_receipt(), pending, namespace_policy=TEST_POLICY)
    assert status == NEW_CLAIM

    claim_b = base_claim(origin="E2-EXTERNAL", signature="sig-e2")
    status, pending = process_claim(claim_b, valid_receipt(), pending, namespace_policy=TEST_POLICY)

    assert status == COALESCED
    assert len(pending) == 1
    assert [a["branch_id"] for a in pending[0]["attestors"]] == ["E1-PRIME", "E2-EXTERNAL"]


def test_same_hash_same_origin_duplicate_no_mutation():
    pending = []
    claim = base_claim(origin="E1-PRIME", signature="sig-e1")
    status, pending = process_claim(claim, valid_receipt(), pending, namespace_policy=TEST_POLICY)
    assert status == NEW_CLAIM

    before = copy.deepcopy(pending)
    status, after = process_claim(claim, valid_receipt(), pending, namespace_policy=TEST_POLICY)

    assert status == DUPLICATE_CLAIM
    assert after == before


def test_same_asset_id_different_hash_stages_competing_claims():
    pending = []
    claim_a = base_claim(asset_hash=HASH_A)
    status, pending = process_claim(claim_a, valid_receipt(), pending, namespace_policy=TEST_POLICY)
    assert status == NEW_CLAIM

    claim_b = base_claim(asset_hash=HASH_B, signature="sig-b")
    status, pending = process_claim(claim_b, valid_receipt(), pending, namespace_policy=TEST_POLICY)

    assert status == NEW_CLAIM
    assert len(pending) == 2
    assert {c["asset_hash"] for c in pending} == {HASH_A, HASH_B}
