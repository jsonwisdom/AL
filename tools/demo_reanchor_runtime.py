#!/usr/bin/env python3
"""
Demo harness for CE-02 basin detection and REANCHOR_BUNDLE_V1 validation.

Cases:
1. CE-02 detects basin entry from three consecutive stressed windows.
2. Valid re-anchor bundle is accepted.
3. Mythic reset bundle is rejected because contested history is erased.
4. Inherited quorum bundle is rejected because CE-03 non-inheritance fails.
"""
from __future__ import annotations

import copy

from reanchor_runtime import (
    ValidationError,
    detect_ce02_basin_entry,
    finalize_bundle,
    validate_reanchor_bundle,
)


KNOWN_PRIOR_ANCHORS = ["anchor:stable-001"]
OBSERVED_STATES = ["state:fractured-009"]


def make_windows():
    return [
        {
            "window_id": "W-000001",
            "S": 0.42,
            "R": 0.34,
            "V": 0.48,
            "A": 0.74,
            "liveness": True,
            "replay_runnable": True,
            "convergent_replay": False,
        },
        {
            "window_id": "W-000002",
            "S": 0.46,
            "R": 0.39,
            "V": 0.51,
            "A": 0.77,
            "liveness": True,
            "replay_runnable": True,
            "convergent_replay": False,
        },
        {
            "window_id": "W-000003",
            "S": 0.49,
            "R": 0.44,
            "V": 0.54,
            "A": 0.81,
            "liveness": True,
            "replay_runnable": True,
            "convergent_replay": False,
        },
    ]


def make_valid_bundle(trigger_record):
    bundle = {
        "schema_version": "REANCHOR_BUNDLE_V1",
        "bundle_id": None,
        "basin": {
            "environment_hash": "env:basin",
            "ruleset_hash": "rules:basin",
            "interpretation_surface_hash": "interp:basin",
        },
        "trigger": {
            "ce02_status": "BASIN_ENTRY_CONFIRMED",
            "ce02_trigger_record": trigger_record,
            "entropy_metrics": trigger_record["entropy_metrics"],
            "contested_region_span": {
                "from_anchor": "anchor:stable-001",
                "to_state": "state:fractured-009",
                "height": 9,
            },
        },
        "external_quorum": {
            "decision_rule": "two_thirds",
            "dissent_preserved": True,
            "members": [
                {
                    "member_id": "verifier:alpha",
                    "public_key": "pub:alpha",
                    "environment_hash": "env:external-alpha",
                    "ruleset_hash": "rules:external-alpha",
                    "interpretation_surface_hash": "interp:external-alpha",
                },
                {
                    "member_id": "verifier:beta",
                    "public_key": "pub:beta",
                    "environment_hash": "env:external-beta",
                    "ruleset_hash": "rules:external-beta",
                    "interpretation_surface_hash": "interp:external-beta",
                },
                {
                    "member_id": "verifier:gamma",
                    "public_key": "pub:gamma",
                    "environment_hash": "env:external-gamma",
                    "ruleset_hash": "rules:external-gamma",
                    "interpretation_surface_hash": "interp:external-gamma",
                },
            ],
        },
        "majority_report_text": "External quorum found basin entry. no dissent recorded",
        "majority_report_hash": "sha256:majority-report",
        "dissent_reports": [],
        "replay_contract_hash": "sha256:replay-contract",
        "replay_contract": {
            "new_replay_horizon": "anchor:regenesis-001",
            "regions": {
                "preserved_as_valid": ["anchor:stable-001"],
                "preserved_as_contested": ["state:fractured-009"],
                "preserved_as_invalidated": [],
            },
        },
        "new_replay_horizon": {
            "prior_anchor_link": "anchor:stable-001",
            "contested_history_preserved": True,
            "forward_replay": {
                "executable": True,
                "convergent_across_independent_verifiers": True,
            },
        },
        "signatures": {
            "quorum_signatures": [
                {"member_id": "verifier:alpha", "signature": "sig:alpha"},
                {"member_id": "verifier:beta", "signature": "sig:beta"},
                {"member_id": "verifier:gamma", "signature": "sig:gamma"},
            ]
        },
        "canonical_encoded_lesson": "We did not fix history. We marked where it broke, showed how authority entered, preserved disagreement, and anchored what comes next.",
    }
    return finalize_bundle(bundle)


def run_case(name, fn):
    print(f"\n=== {name} ===")
    try:
        result = fn()
        print("PASS", result)
    except ValidationError as exc:
        print("REFUSED", exc.code, exc.message)
    except AssertionError as exc:
        print("FAILED", exc)


def main():
    windows = make_windows()
    detected, trigger_record = detect_ce02_basin_entry(windows)

    run_case(
        "CE-02 detects basin entry",
        lambda: {"detected": detected, "trigger": trigger_record} if detected else (_ for _ in ()).throw(AssertionError("basin not detected")),
    )

    valid_bundle = make_valid_bundle(trigger_record)

    run_case(
        "Valid re-anchor bundle accepted",
        lambda: validate_reanchor_bundle(valid_bundle, KNOWN_PRIOR_ANCHORS, OBSERVED_STATES),
    )

    mythic_reset = copy.deepcopy(valid_bundle)
    mythic_reset["new_replay_horizon"]["contested_history_preserved"] = False
    mythic_reset = finalize_bundle(mythic_reset)
    run_case(
        "Mythic reset rejected",
        lambda: validate_reanchor_bundle(mythic_reset, KNOWN_PRIOR_ANCHORS, OBSERVED_STATES),
    )

    inherited_quorum = copy.deepcopy(valid_bundle)
    inherited_quorum["external_quorum"]["members"][0]["environment_hash"] = "env:basin"
    inherited_quorum = finalize_bundle(inherited_quorum)
    run_case(
        "Inherited quorum rejected",
        lambda: validate_reanchor_bundle(inherited_quorum, KNOWN_PRIOR_ANCHORS, OBSERVED_STATES),
    )


if __name__ == "__main__":
    main()
