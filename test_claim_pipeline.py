from claim_pipeline import create_claim_verification_receipt
from receipt import verify_attestations, verify_hashes, verify_invariants


def test_pipeline_creates_valid_receipt_without_approval():
    r = create_claim_verification_receipt("Test claim.")
    assert r["authority"] is False
    assert r["authorization"]["result"] == "pending_human"
    assert r["execution"]["actions"] == []
    assert r["execution"]["status"] == "receipt_only"
    assert verify_invariants(r)
    assert verify_hashes(r)
    assert verify_attestations(r)


def test_pipeline_with_approval_adds_authorizer():
    r = create_claim_verification_receipt("Test claim.", human_approved=True)
    roles = [a["role"] for a in r["attestations"]]
    assert "authorizer" in roles
    assert r["authorization"]["result"] == "granted"
    assert r["execution"]["status"] == "executed"
    assert verify_hashes(r)


def test_verified_support_is_not_truth():
    r = create_claim_verification_receipt("Test claim.")
    assert "truth" not in r
    assert r["authority"] is False
    assert r["verification"]["result"] in ("partial", "pass", "fail")


def test_every_claim_has_evidence_mapping():
    r = create_claim_verification_receipt("Claim one. Claim two.")
    claims = r["extraction"]["claims"]
    evidence = r["evidence"]["items"]
    assert len(claims) == 2
    for claim in claims:
        assert any(item["supports_claim"] == claim["claim_id"] for item in evidence)


def test_pipeline_embeds_policy_hash():
    r = create_claim_verification_receipt("Test claim.")
    assert r["policy"]["policy_version"] == "POLICY_CLAIM_VERIFICATION_V0_1"
    assert r["policy"]["policy_hash"].startswith("sha256:")
