import json

import pytest

from claim_pipeline import create_claim_verification_receipt
from map_query import find_by_claim_text, find_by_receipt_id, load_world_map, summarize_map
from world_map import append_world_map_entry


@pytest.fixture
def populated_map(tmp_path):
    map_file = tmp_path / "test_map.jsonl"

    r1 = create_claim_verification_receipt("Approved test claim about AI.", human_approved=True)
    p1 = tmp_path / f"{r1['receipt_id']}.json"
    p1.write_text(json.dumps(r1, indent=2), encoding="utf-8")
    append_world_map_entry(p1, map_file)

    r2 = create_claim_verification_receipt("Second claim on verification.", human_approved=True)
    p2 = tmp_path / f"{r2['receipt_id']}.json"
    p2.write_text(json.dumps(r2, indent=2), encoding="utf-8")
    append_world_map_entry(p2, map_file)

    return map_file


def test_summary_counts_entries(populated_map):
    summary = summarize_map(populated_map)
    assert summary["total_entries"] == 2
    assert summary["message"].startswith("Projection from verified")


def test_receipt_lookup_returns_exact_entry(populated_map):
    entries = load_world_map(populated_map)
    rid = entries[0]["receipt_id"]
    result = find_by_receipt_id(rid, populated_map)
    assert result is not None
    assert result["receipt_id"] == rid
    assert result["authority"] is False


def test_claim_search_returns_matching_entry(populated_map):
    results = find_by_claim_text("AI", populated_map)
    assert len(results) >= 1
    assert any("AI" in c["text"] for c in results[0]["claims"])


def test_empty_map_returns_safe_zero_summary(tmp_path):
    summary = summarize_map(tmp_path / "empty.jsonl")
    assert summary["total_entries"] == 0
    assert summary["status"] == "empty_map"
