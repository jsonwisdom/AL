#!/usr/bin/env python3
"""
Minimal CE-02 -> REANCHOR_BUNDLE_V1 validator scaffold.

Purpose:
- Detect basin entry from S/R/V/A telemetry.
- Validate that a re-anchor bundle is constitutional re-genesis, not a mythic reset.

This is intentionally small and dependency-light. It is a scaffold, not a full cryptographic implementation.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


P24_COUPLING = 0.91
THRESHOLDS = {"S": 0.35, "R": 0.30, "V": 0.40, "A": 0.70}


class ValidationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def canonical_bytes(obj: Dict[str, Any]) -> bytes:
    """Approximate JCS-style canonical JSON: sorted keys, compact separators."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_bundle_id(bundle: Dict[str, Any]) -> str:
    tmp = copy.deepcopy(bundle)
    tmp["bundle_id"] = None
    return "sha256:" + sha256_hex(canonical_bytes(tmp))


def compute_p24(S: float, R: float, V: float, A: float) -> float:
    return P24_COUPLING * ((S ** 1.4) * (R ** 1.1) * (V ** 1.6) * (A ** 1.8))


def exceeded_metrics(window: Dict[str, Any]) -> List[str]:
    return [k for k, t in THRESHOLDS.items() if float(window.get(k, 0.0)) >= t]


def detect_ce02_basin_entry(windows: List[Dict[str, Any]], consecutive_required: int = 3) -> Tuple[bool, Dict[str, Any]]:
    """Return CE-02 basin entry verdict and trigger record."""
    streak: List[Dict[str, Any]] = []
    for w in windows:
        metrics = exceeded_metrics(w)
        p24 = compute_p24(float(w["S"]), float(w["R"]), float(w["V"]), float(w["A"]))
        passed = (
            bool(w.get("liveness", False))
            and bool(w.get("replay_runnable", False))
            and not bool(w.get("convergent_replay", True))
            and float(w.get("A", 0.0)) >= THRESHOLDS["A"]
            and len(metrics) >= 3
        )
        enriched = dict(w)
        enriched["P24"] = p24
        enriched["thresholds_crossed"] = metrics
        if passed:
            streak.append(enriched)
        else:
            streak = []
        if len(streak) >= consecutive_required:
            return True, {
                "ce02_status": "BASIN_ENTRY_CONFIRMED",
                "consecutive_windows": len(streak),
                "trigger_window_ids": [x["window_id"] for x in streak[-consecutive_required:]],
                "thresholds_crossed": sorted(set().union(*(set(x["thresholds_crossed"]) for x in streak[-consecutive_required:]))),
                "entropy_metrics": streak[-consecutive_required:],
            }
    return False, {"ce02_status": "NO_BASIN_ENTRY"}


def validate_reanchor_bundle(bundle: Dict[str, Any], known_prior_anchors: List[str], observed_states: List[str]) -> Dict[str, Any]:
    # 1. Structural canonicality
    if bundle.get("schema_version") != "REANCHOR_BUNDLE_V1":
        raise ValidationError("INVALID_BUNDLE_STRUCTURE", "schema_version mismatch")
    expected_id = compute_bundle_id(bundle)
    if bundle.get("bundle_id") != expected_id:
        raise ValidationError("INVALID_BUNDLE_STRUCTURE", "bundle_id does not match canonical hash")

    trigger = bundle.get("trigger", {})
    basin = bundle.get("basin", {})

    # 2. CE-02 trigger legitimacy
    if trigger.get("ce02_status") != "BASIN_ENTRY_CONFIRMED":
        raise ValidationError("UNJUSTIFIED_EMERGENCY_DECLARATION", "CE-02 status not confirmed")
    if int(trigger.get("ce02_trigger_record", {}).get("consecutive_windows", 0)) < 1:
        raise ValidationError("UNJUSTIFIED_EMERGENCY_DECLARATION", "no consecutive windows")
    crossed = set(trigger.get("ce02_trigger_record", {}).get("thresholds_crossed", []))
    if not ({"A", "V"} & crossed):
        raise ValidationError("UNJUSTIFIED_EMERGENCY_DECLARATION", "A or V threshold not crossed")
    metrics = trigger.get("entropy_metrics", [])
    if not metrics:
        raise ValidationError("UNJUSTIFIED_EMERGENCY_DECLARATION", "missing entropy metrics")
    latest = metrics[-1]
    p24 = compute_p24(float(latest["S"]), float(latest["R"]), float(latest["V"]), float(latest["A"]))
    basin_conditions = float(latest["A"]) >= 0.70 and latest.get("convergent_replay") is False
    if not (p24 >= 1.0 or basin_conditions):
        raise ValidationError("UNJUSTIFIED_EMERGENCY_DECLARATION", "neither P24 nor basin condition satisfied")

    # 3. Contested region correctness
    span = trigger.get("contested_region_span", {})
    if span.get("from_anchor") not in known_prior_anchors:
        raise ValidationError("INVALID_CONTESTED_REGION", "unknown prior anchor")
    if span.get("to_state") not in observed_states:
        raise ValidationError("INVALID_CONTESTED_REGION", "unobserved terminal state")
    if int(span.get("height", 0)) <= 0:
        raise ValidationError("INVALID_CONTESTED_REGION", "empty contested span")

    # 4. CE-03 external quorum constraints
    quorum = bundle.get("external_quorum", {})
    members = quorum.get("members", [])
    if not members:
        raise ValidationError("MYTHIC_AUTHORITY_RISK", "empty external quorum")
    for m in members:
        if m.get("environment_hash") == basin.get("environment_hash"):
            raise ValidationError("MYTHIC_AUTHORITY_RISK", "environment inherited from basin")
        if m.get("ruleset_hash") == basin.get("ruleset_hash"):
            raise ValidationError("MYTHIC_AUTHORITY_RISK", "ruleset inherited from basin")
        if m.get("interpretation_surface_hash") == basin.get("interpretation_surface_hash"):
            raise ValidationError("MYTHIC_AUTHORITY_RISK", "interpretation surface inherited from basin")
    if quorum.get("dissent_preserved") is not True:
        raise ValidationError("MYTHIC_AUTHORITY_RISK", "dissent not preserved")
    if len(bundle.get("dissent_reports", [])) == 0 and "no dissent recorded" not in bundle.get("majority_report_text", ""):
        raise ValidationError("MYTHIC_AUTHORITY_RISK", "no dissent reports and no explicit no-dissent statement")

    # 5. Deliberation integrity
    if not bundle.get("majority_report_hash"):
        raise ValidationError("ARBITRARY_REANCHOR", "missing majority report hash")
    if not bundle.get("replay_contract_hash"):
        raise ValidationError("ARBITRARY_REANCHOR", "missing replay contract hash")
    contract = bundle.get("replay_contract", {})
    required_regions = {"preserved_as_valid", "preserved_as_contested", "preserved_as_invalidated"}
    if not contract.get("new_replay_horizon") or not required_regions.issubset(set(contract.get("regions", {}).keys())):
        raise ValidationError("ARBITRARY_REANCHOR", "replay contract incomplete")

    # 6. New replay horizon invariants
    horizon = bundle.get("new_replay_horizon", {})
    if horizon.get("prior_anchor_link") != span.get("from_anchor"):
        raise ValidationError("FAILED_REGENESIS", "new horizon does not link to prior anchor")
    if horizon.get("contested_history_preserved") is not True:
        raise ValidationError("FAILED_REGENESIS", "contested history not preserved")
    if horizon.get("forward_replay", {}).get("executable") is not True:
        raise ValidationError("FAILED_REGENESIS", "forward replay not executable")
    if horizon.get("forward_replay", {}).get("convergent_across_independent_verifiers") is not True:
        raise ValidationError("FAILED_REGENESIS", "forward replay not convergent")

    # 7. Signature completeness (scaffold: presence check; real implementation verifies crypto signatures)
    signatures = bundle.get("signatures", {})
    quorum_sigs = signatures.get("quorum_signatures", [])
    if len(quorum_sigs) < len(members):
        raise ValidationError("UNSIGNED_AUTHORITY_IMPORT", "missing quorum signatures")
    signed_ids = {s.get("member_id") for s in quorum_sigs}
    if any(m.get("member_id") not in signed_ids for m in members):
        raise ValidationError("UNSIGNED_AUTHORITY_IMPORT", "not every member signed")

    # 8. Constitutional memory
    memory_warning = None
    if not bundle.get("canonical_encoded_lesson"):
        memory_warning = "MEMORY_LAYER_INCOMPLETE"

    return {"status": "REANCHOR_BUNDLE_ACCEPTED", "warning": memory_warning, "bundle_id": bundle["bundle_id"]}


def finalize_bundle(bundle: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(bundle)
    out["bundle_id"] = compute_bundle_id(out)
    return out
