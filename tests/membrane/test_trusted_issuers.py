#!/usr/bin/env python3
"""
Membrane tests for config/trusted_issuers.yaml.

Governance surfaces must themselves be governed.
The policy is allowed to name forbidden terms; issuer entries are not.
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
    "threat assessment bureau",
}


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def issuer_text(issuer):
    fields = [
        issuer.get("issuer_id", ""),
        issuer.get("name", ""),
        issuer.get("category", ""),
        issuer.get("issuer_url", ""),
        issuer.get("did_or_jwks_ref", ""),
        issuer.get("revocation_endpoint", ""),
        issuer.get("added_by_pr", ""),
        issuer.get("rationale", ""),
        issuer.get("operational_state", ""),
        " ".join(issuer.get("credential_scope", [])),
    ]
    return "\n".join(str(x).lower() for x in fields)


def test_required_top_level_fields_exist():
    data = load_config()
    assert "trusted_issuers" in data
    assert "policy" in data


def test_policy_declares_membrane_controls():
    data = load_config()
    policy = data["policy"]
    assert policy.get("operator_signature_required") is True
    assert policy.get("no_ghost_anchor") is True
    assert policy.get("config_changes_require_pr") is True
    assert policy.get("revocation_endpoint_required") is True
    assert policy.get("added_by_pr_required") is True
    assert policy.get("rationale_required") is True
    assert "forbidden_semantics" in policy


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


def test_no_forbidden_semantics_in_issuer_entries():
    data = load_config()

    for issuer in data["trusted_issuers"]:
        text = issuer_text(issuer)
        for term in FORBIDDEN_TERMS:
            assert term not in text, (
                f"Forbidden governance term present in issuer {issuer.get('issuer_id')}: {term}"
            )


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
    test_policy_declares_membrane_controls()
    test_all_issuers_have_required_fields()
    test_no_forbidden_semantics_in_issuer_entries()
    test_all_issuers_have_revocation_endpoint()
    test_all_issuers_have_pr_traceability()
    test_no_law_enforcement_jurisdiction_creep()
    print("TRUSTED_ISSUER_MEMBRANE_PASS")
