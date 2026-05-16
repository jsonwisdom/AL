"""Witness receipt and legitimacy tests."""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from witness.receipts.dependencies import get_primary_runtime_receipt, get_runtime_evidence_state
from witness_court_pilot_v4 import app


NEGATIVE_STATE = {
    "runtime_converged": False,
    "evidence_path": None,
    "render_blocking": False,
    "claim_boundary": "No valid runtime receipt found. No runtime legitimacy claim.",
}


def valid_receipt_data() -> dict:
    return {
        "receipt_version": "witness_ci_runtime_receipt_v0.1",
        "receipt_type": "EPHEMERAL_CI_RUNTIME_RECEIPT",
        "status": "CONVERGED_BY_CI",
        "render_status": "OPTIONAL_HOSTING_LAYER",
        "timestamp": "2026-05-16T04:00:00Z",
        "repo": "jsonwisdom/AL",
        "branch": "project/witness-v0.4-runtime",
        "commit_sha": "e6ab11ae5088c1bed34dd82fc33b253d3122396c",
        "workflow_name": "Witness v0.4 Project Runtime Check",
        "workflow_run": "1234567890",
        "workflow_attempt": "1",
        "runtime": "uvicorn",
        "runtime_mode": "EPHEMERAL_CI_RUNTIME",
        "project_root": "projects/witness-v0.4-runtime",
        "checks": [
            "pip_install",
            "py_compile",
            "uvicorn_boot",
            "health_endpoint",
            "summarize_endpoint",
            "convergence_receipt_endpoint",
        ],
        "claim_boundary": "proves ephemeral CI runtime convergence only; does not prove persistent continuity or live hosted availability",
    }


def patch_loader_path(monkeypatch, receipt_path: Path) -> None:
    get_primary_runtime_receipt.cache_clear()
    monkeypatch.setattr(
        "witness.receipts.dependencies.load_ci_runtime_receipt",
        lambda: __import__("witness.receipts.loader", fromlist=["load_ci_runtime_receipt"]).load_ci_runtime_receipt(path=receipt_path),
    )


def test_positive_receipt_validation(tmp_path, monkeypatch):
    receipt_path = tmp_path / "ci-runtime-receipt.json"
    receipt_path.write_text(json.dumps(valid_receipt_data()), encoding="utf-8")
    patch_loader_path(monkeypatch, receipt_path)

    state = get_runtime_evidence_state()

    assert state["runtime_converged"] is True
    assert state["evidence_path"] == "EPHEMERAL_CI_RUNTIME_RECEIPT"
    assert state["render_blocking"] is False
    assert state["commit_sha"] == "e6ab11ae5088c1bed34dd82fc33b253d3122396c"
    assert "proves ephemeral CI runtime convergence only" in state["claim_boundary"]


def test_malformed_receipt_rejection(tmp_path, monkeypatch):
    receipt_path = tmp_path / "ci-runtime-receipt.json"
    receipt_path.write_text("{invalid json", encoding="utf-8")
    patch_loader_path(monkeypatch, receipt_path)

    assert get_runtime_evidence_state() == NEGATIVE_STATE


def test_missing_required_checks_rejection(tmp_path, monkeypatch):
    data = valid_receipt_data()
    data["checks"] = ["pip_install", "py_compile"]
    receipt_path = tmp_path / "ci-runtime-receipt.json"
    receipt_path.write_text(json.dumps(data), encoding="utf-8")
    patch_loader_path(monkeypatch, receipt_path)

    assert get_runtime_evidence_state() == NEGATIVE_STATE


def test_no_file_negative_path(tmp_path, monkeypatch):
    receipt_path = tmp_path / "missing-ci-runtime-receipt.json"
    patch_loader_path(monkeypatch, receipt_path)

    assert get_runtime_evidence_state() == NEGATIVE_STATE


def test_legitimacy_endpoint_positive(tmp_path, monkeypatch):
    receipt_path = tmp_path / "ci-runtime-receipt.json"
    receipt_path.write_text(json.dumps(valid_receipt_data()), encoding="utf-8")
    patch_loader_path(monkeypatch, receipt_path)

    response = TestClient(app).get("/legitimacy")
    assert response.status_code == 200
    data = response.json()

    assert data["runtime_converged"] is True
    assert data["evidence_path"] == "EPHEMERAL_CI_RUNTIME_RECEIPT"
    assert data["render_blocking"] is False


def test_legitimacy_endpoint_no_receipt(tmp_path, monkeypatch):
    receipt_path = tmp_path / "missing-ci-runtime-receipt.json"
    patch_loader_path(monkeypatch, receipt_path)

    response = TestClient(app).get("/legitimacy")
    assert response.status_code == 200
    assert response.json() == NEGATIVE_STATE
