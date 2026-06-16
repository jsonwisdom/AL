import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "dashboards" / "404_overview" / "build.py"

spec = importlib.util.spec_from_file_location("dashboard_404_build", BUILD_PATH)
dashboard_build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard_build)


def test_dashboard_rejects_forbidden_verdict(tmp_path, monkeypatch):
    receipts_dir = tmp_path / "receipts"
    day_dir = receipts_dir / "2026-05-07"
    day_dir.mkdir(parents=True)

    bad_receipt = {
        "receipt_id": "bad_risk_score_fixture",
        "circuit_id": "404_v1",
        "target_url": "https://example.gov/file.pdf",
        "crawl_timestamp": "2026-05-07T00:00:00Z",
        "verdict": "RISK_SCORE"
    }

    (day_dir / "bad.json").write_text(json.dumps(bad_receipt), encoding="utf-8")

    monkeypatch.setattr(dashboard_build, "RECEIPTS_DIR", receipts_dir)
    monkeypatch.setattr(dashboard_build, "OUTPUT_DIR", tmp_path / "public")

    with pytest.raises(RuntimeError, match="forbidden verdict"):
        dashboard_build.build_dashboard()


def test_dashboard_rejects_forbidden_extra_semantic_field(tmp_path, monkeypatch):
    receipts_dir = tmp_path / "receipts"
    day_dir = receipts_dir / "2026-05-07"
    day_dir.mkdir(parents=True)

    bad_receipt = {
        "receipt_id": "bad_extra_field_fixture",
        "circuit_id": "404_v1",
        "target_url": "https://example.gov/file.pdf",
        "crawl_timestamp": "2026-05-07T00:00:00Z",
        "verdict": "FOUND",
        "RISK_SCORE": 0.91
    }

    (day_dir / "bad.json").write_text(json.dumps(bad_receipt), encoding="utf-8")

    monkeypatch.setattr(dashboard_build, "RECEIPTS_DIR", receipts_dir)
    monkeypatch.setattr(dashboard_build, "OUTPUT_DIR", tmp_path / "public")

    with pytest.raises(RuntimeError, match="forbidden receipt field"):
        dashboard_build.build_dashboard()
