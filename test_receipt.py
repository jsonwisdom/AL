import json
from pathlib import Path

from receipt import verify_attestations, verify_hashes, verify_invariants
from claim_pipeline import create_claim_verification_receipt


def test_good_receipt_passes(tmp_path):
    receipt = create_claim_verification_receipt("Test claim.", human_approved=True)
    p = tmp_path / "receipt.json"
    p.write_text(json.dumps(receipt), encoding="utf-8")
    from receipt import verify_receipt
    assert verify_receipt(p)["valid"] is True


def test_authority_true_fails():
    receipt = create_claim_verification_receipt("Test claim.", human_approved=True)
    receipt["authority"] = True
    assert verify_invariants(receipt) is False


def test_bad_hash_fails():
    receipt = create_claim_verification_receipt("Test claim.", human_approved=True)
    receipt["final_hash"] = "sha256:" + "0" * 64
    assert verify_hashes(receipt) is False


def test_mutated_section_fails():
    receipt = create_claim_verification_receipt("Test claim.", human_approved=True)
    receipt["extraction"]["extra"] = True
    assert verify_hashes(receipt) is False


def test_missing_attestation_fails():
    receipt = create_claim_verification_receipt("Test claim.", human_approved=True)
    receipt["attestations"] = []
    assert verify_attestations(receipt) is False


def test_unknown_signed_section_fails():
    receipt = create_claim_verification_receipt("Test claim.", human_approved=True)
    receipt["attestations"][0]["signed_section"] = "truth"
    assert verify_attestations(receipt) is False
