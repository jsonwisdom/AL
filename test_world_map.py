import json

import pytest

from claim_pipeline import create_claim_verification_receipt
from world_map import append_world_map_entry, eligible_for_ingest, load_receipt


@pytest.fixture
def approved_receipt(tmp_path):
    r = create_claim_verification_receipt("Approved test claim.", human_approved=True)
    p = tmp_path / f"{r['receipt_id']}.json"
    p.write_text(json.dumps(r, indent=2), encoding="utf-8")
    return p


@pytest.fixture
def pending_receipt(tmp_path):
    r = create_claim_verification_receipt("Pending test claim.")
    p = tmp_path / f"{r['receipt_id']}.json"
    p.write_text(json.dumps(r, indent=2), encoding="utf-8")
    return p


def test_pending_receipt_rejected(pending_receipt, tmp_path):
    assert eligible_for_ingest(pending_receipt) is False
    assert append_world_map_entry(pending_receipt, tmp_path / "map.jsonl") is None


def test_approved_executed_receipt_accepted(approved_receipt, tmp_path):
    assert eligible_for_ingest(approved_receipt) is True
    map_id = append_world_map_entry(approved_receipt, tmp_path / "map.jsonl")
    assert map_id is not None
    assert map_id.startswith("wm_rec_")


def test_authority_true_rejected(tmp_path):
    r = create_claim_verification_receipt("Bad authority.", human_approved=True)
    r["authority"] = True
    p = tmp_path / "bad_authority.json"
    p.write_text(json.dumps(r), encoding="utf-8")
    assert eligible_for_ingest(p) is False


def test_invalid_hash_rejected(approved_receipt, tmp_path):
    data = load_receipt(approved_receipt)
    data["final_hash"] = "sha256:" + "0" * 64
    p = tmp_path / "bad_hash.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    assert eligible_for_ingest(p) is False


def test_entry_preserves_receipt_identity(approved_receipt, tmp_path):
    map_file = tmp_path / "world_map.jsonl"
    append_world_map_entry(approved_receipt, map_file)
    entry = json.loads(map_file.read_text(encoding="utf-8").splitlines()[0])
    receipt = load_receipt(approved_receipt)
    assert entry["receipt_id"] == receipt["receipt_id"]
    assert entry["final_hash"] == receipt["final_hash"]
    assert entry["authority"] is False
    assert entry["authorization_result"] == "granted"


def test_entry_preserves_policy_hash(approved_receipt, tmp_path):
    map_file = tmp_path / "world_map.jsonl"
    append_world_map_entry(approved_receipt, map_file)
    entry = json.loads(map_file.read_text(encoding="utf-8").splitlines()[0])
    receipt = load_receipt(approved_receipt)
    assert entry["policy_hash"] == receipt["policy"]["policy_hash"]
    assert entry["policy_hash"].startswith("sha256:")
