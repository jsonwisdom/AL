#!/usr/bin/env python3
"""
Membrane tests for config/trusted_issuers.yaml.

Governance surfaces must themselves be governed.
"""

from pathlib import Path
import yaml

CONFIG_PATH = Path("config/trusted_issuers.yaml")

FORBIDDEN_TERMS = {
    "guilt",
    "intent",
    "motive",
    "corruption",
    "threat",
    "risk_score",
    "bad_actor",
    "law_enforcement",
    "police",
    "prosecution",
    "intelligence",
    "surveillance",
    "Threat Assessment Bureau",
}


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_required_top_level_fields_exist():
    data = load_config()
    assert "trusted_issuers" in data
    assert "policy" in data


def test_all_issuers_have_required_fields():
    data = load_config()
    required = {
        "issuer_id",
        "name",
        "category",
        "credential_scope",
        "issuer_url",
        "did_or_jwks_ref",
        "revocation_endpoint",
        "added_by_pr",
        "rationale",
        "operational_state",
    }

    for issuer in data["trusted_issuers"]:
        missing = required - set(issuer.keys())
        assert not missing, f"Issuer missing required fields: {missing}"


def test_no_forbidden_semantics_present():
    raw = CONFIG_PATH.read_text(encoding="utf-8")
    lowered = raw.lower()

    for term in FORBIDDEN_TERMS:
        assert term.lower() not in lowered, f"Forbidden governance term present: {term}"


def test_all_issuers_have_revocation_endpoint():
    data = load_config()
    for issuer in data["trusted_issuers"]:
        assert issuer["revocation_endpoint"], f"Issuer missing revocation endpoint: {issuer['issuer_id']}"


def test_all_issuers_have_pr_traceability():
    data = load_config()
    for issuer in data["trusted_issuers"]:
        assert issuer["added_by_pr"], f"Issuer missing PR traceability: {issuer['issuer_id']}"


def test_no_law_enforcement_jurisdiction_creep():
    data = load_config()

    forbidden_categories = {
        "law_enforcement",
        "police",
        "prosecution",
        "intelligence",
        "surveillance",
    }

    for issuer in data["trusted_issuers"]:
        category = issuer.get("category", "").lower()
        assert category not in forbidden_categories, (
            f"Forbidden issuer category detected: {category}"
        )


if __name__ == "__main__":
    test_required_top_level_fields_exist()
    test_all_issuers_have_required_fields()
    test_no_forbidden_semantics_present()
    test_all_issuers_have_revocation_endpoint()
    test_all_issuers_have_pr_traceability()
    test_no_law_enforcement_jurisdiction_creep()
    print("TRUSTED_ISSUER_MEMBRANE_PASS")
