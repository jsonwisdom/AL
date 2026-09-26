import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "boss_bre_al_checked_in_replay.py"
SPEC = importlib.util.spec_from_file_location("boss_bre_al_checked_in_replay", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = replay
SPEC.loader.exec_module(replay)

CLAIM_TYPE = replay.CLAIM_TYPE
EXTRACTED = replay.EXTRACTED
HASH_MATCH = replay.HASH_MATCH
PUBLIC_CONTENT_CLAIM = replay.PUBLIC_CONTENT_CLAIM
run_replay = replay.run_replay


FORBIDDEN_LEAD_LANGUAGE = (
    "fraud proven",
    "criminal finding",
    "confirmed corruption",
    "illegal payment",
)


def _run(tmp_path: Path) -> tuple[dict, list[dict]]:
    outdir = tmp_path / "al_checked_in_replay"
    summary = run_replay(REPO_ROOT, outdir, "2026-08-25T23:50:00Z")
    leads_path = outdir / "latest_anomaly_leads.jsonl"
    leads = [json.loads(line) for line in leads_path.read_text(encoding="utf-8").splitlines() if line]
    return summary, leads


def test_replay_stays_lead_only(tmp_path: Path) -> None:
    summary, leads = _run(tmp_path)

    assert summary["artifact"] == "AL_CHECKED_IN_BYTES_REPLAY"
    assert summary["claim_type"] == CLAIM_TYPE
    assert summary["public_content_claim"] == PUBLIC_CONTENT_CLAIM
    assert summary["authority"] is False
    assert summary["verified"] is False
    assert summary["network_fetch"] is False
    assert summary["pass_flipped"] is False
    assert summary["fraud_verdict"] is False
    assert summary["al_pass_gate"] == "INDETERMINATE"
    assert summary["status"] != "PASS"
    assert summary["hash_status"] == HASH_MATCH
    assert summary["hash_match"] is True
    assert summary["source_pdf_sha256"] == summary["claim_hash"]
    assert summary["lead_count"] == len(leads)
    assert summary["lead_count"] == summary["high_count"] + summary["medium_count"] + summary["low_count"]
    assert leads


@pytest.mark.parametrize("field", ["claim_status", "public_content_claim"])
def test_every_lead_is_blocked_pending_review(tmp_path: Path, field: str) -> None:
    _, leads = _run(tmp_path)
    expected = CLAIM_TYPE if field == "claim_status" else PUBLIC_CONTENT_CLAIM
    for lead in leads:
        assert lead[field] == expected
        assert lead["authority"] is False
        assert lead["fraud_verdict"] is False
        assert lead["human_review_required"] is True
        assert lead["no_fake_green"] is True
        blob = json.dumps(lead).lower()
        for term in FORBIDDEN_LEAD_LANGUAGE:
            assert term not in blob


def test_content_and_evidence_chain_leads(tmp_path: Path) -> None:
    summary, leads = _run(tmp_path)
    rule_ids = {lead["rule_id"] for lead in leads}

    assert "BBRISK_CLAIM_REPLAY_PENDING" in rule_ids
    assert "BBRISK_PLACEHOLDER_SOURCE_PENDING" in rule_ids
    assert "BBRISK_CI_PASS_VS_GATE" in rule_ids
    assert "BBRISK_RULE_COVERAGE_GAP" in rule_ids
    assert "BBRISK_LARGE_DOLLAR_AMOUNT" not in rule_ids
    assert "BBRISK_GATE_DOC_STALE" not in rule_ids

    if summary["extract_status"] == EXTRACTED:
        assert "BBRISK_MEDICAID_CMS_WITHHOLDING" in rule_ids
        assert "BBRISK_FRAUD_RISK_LANGUAGE" in rule_ids
        assert "BBRISK_DEFICIT_SHORTFALL_VARIANCE" in rule_ids
        assert "BBRISK_PROGRAM_REDUCTION_OR_RESERVE_DRAW" in rule_ids
        assert "BBRISK_FORECAST_VOLATILITY" in rule_ids


def test_missing_pdf_is_blocked_not_pass(tmp_path: Path) -> None:
    outdir = tmp_path / "missing"
    root = tmp_path / "root"
    (root / "fixtures/al/sources").mkdir(parents=True)
    (root / "data").mkdir(parents=True)
    (root / "docs/audit").mkdir(parents=True)
    (root / "alms/national").mkdir(parents=True)
    (root / "fixtures/al/al_budget_2026_claim.json").write_text(
        (REPO_ROOT / "fixtures/al/al_budget_2026_claim.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / "data/boss_bre_anomaly_rules.json").write_text(
        (REPO_ROOT / "data/boss_bre_anomaly_rules.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / "docs/audit/AL_PASS_GATE.md").write_text("INDETERMINATE\n", encoding="utf-8")
    (root / "fixtures/al/sources/al_budget_snapshot_2026-05-03.txt").write_text(
        "OFFICIAL_SOURCE_PENDING\n",
        encoding="utf-8",
    )
    (root / "alms/national/national_root_ci_latest.json").write_text(
        json.dumps({"states": [{"state": "AL", "status": "INDETERMINATE"}]}),
        encoding="utf-8",
    )

    summary = replay.run_replay(root, outdir, "2026-08-25T23:50:00Z")
    leads = [json.loads(line) for line in (outdir / "latest_anomaly_leads.jsonl").read_text().splitlines() if line]
    assert summary["hash_status"] == "SOURCE_BYTES_MISSING"
    assert summary["pass_flipped"] is False
    assert any(lead["rule_id"] == "BBRISK_MISSING_PAYLOAD" for lead in leads)
