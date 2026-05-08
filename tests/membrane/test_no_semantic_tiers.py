import yaml
from pathlib import Path

ALLOWED_OPERATIONAL_FEATURES = {
    "crawl_frequency_minutes",
    "api_rate_limit_per_minute",
    "webhook_concurrency",
    "retention_days",
    "export_enabled",
    "sla_percent",
    "support_tier",
    "signed_feed_delivery",
    "on_prem_runner",
    "white_label_rendering",
}

FORBIDDEN_FEATURES = {
    "premium_verdict",
    "risk_scoring",
    "trust_scoring",
    "sentiment_analysis",
    "priority_verdict",
    "customer_override",
    "paid_unlock",
    "private_interpretation",
    "target_priority",
    "receipt_suppression",
    "custom_allowed_surface",
}

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "billing.yaml.example"


def load_config():
    with CONFIG.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def all_feature_kinds(cfg):
    kinds = []
    for tier in cfg["tiers"]:
        for flag in tier["feature_flags"]:
            kinds.append(flag["feature_kind"])
    return kinds


def test_only_operational_feature_kinds_exist():
    cfg = load_config()
    for kind in all_feature_kinds(cfg):
        assert kind in ALLOWED_OPERATIONAL_FEATURES, (
            f"Non-operational feature detected: {kind}"
        )


def test_forbidden_feature_kinds_never_appear():
    cfg = load_config()
    present = set(all_feature_kinds(cfg))
    violations = present & FORBIDDEN_FEATURES
    assert not violations, (
        f"Forbidden semantic feature kinds detected: {violations}"
    )


def test_enterprise_cannot_introduce_semantic_authority():
    cfg = load_config()

    public = next(t for t in cfg["tiers"] if t["name"] == "public")
    enterprise = next(t for t in cfg["tiers"] if t["name"] == "enterprise")

    public_kinds = {f["feature_kind"] for f in public["feature_flags"]}
    enterprise_kinds = {f["feature_kind"] for f in enterprise["feature_flags"]}

    semantic_drift = enterprise_kinds & FORBIDDEN_FEATURES

    assert not semantic_drift, (
        f"Enterprise tier introduced semantic authority: {semantic_drift}"
    )


def test_red_team_risk_scoring_rejected():
    injected = {
        "feature_kind": "risk_scoring",
        "value": True,
    }

    assert injected["feature_kind"] not in ALLOWED_OPERATIONAL_FEATURES, (
        "Risk scoring must never become an allowed operational feature"
    )

    assert injected["feature_kind"] in FORBIDDEN_FEATURES, (
        "Risk scoring must remain explicitly forbidden"
    )


def test_all_allowed_features_are_operational_not_semantic():
    taxonomy = {
        "crawl_frequency_minutes": "operations",
        "api_rate_limit_per_minute": "operations",
        "webhook_concurrency": "operations",
        "retention_days": "operations",
        "export_enabled": "operations",
        "sla_percent": "operations",
        "support_tier": "operations",
        "signed_feed_delivery": "operations",
        "on_prem_runner": "operations",
        "white_label_rendering": "operations",
    }

    for feature in ALLOWED_OPERATIONAL_FEATURES:
        assert taxonomy.get(feature) == "operations", (
            f"Allowed feature is not classified as operational: {feature}"
        )
