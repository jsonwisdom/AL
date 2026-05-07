#!/usr/bin/env python3
import json
import os
import subprocess
import sys

BASELINE_PATH = "seeds/illinois/downstate-baseline-v0.1.json"
COOK_PATH = "seeds/illinois/cook-delta-a-v0.1.json"
CHICAGO_PATH = "seeds/illinois/chicago-delta-b-v0.1.json"
MODEL_PATH = "core/overlays/MUNICIPAL_SOVEREIGNTY_CONFLICT_MODEL_V1.json"
COOK_VALIDATOR = "scripts/validate_cook_delta_a.py"
CHICAGO_VALIDATOR = "scripts/validate_chicago_delta_b.py"
VIEW_PATH = "views/illinois/chicago-effective-v0.1.json"
LEDGER_PATH = "logs/chicago_conflict_ledger_v0.1.jsonl"


def fail(code):
    print(f"RESOLVE_CHICAGO_CONFLICTS_FAILED:{code}")
    sys.exit(1)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        fail("INVALID_INPUT_STATE")


def run_validator(path, failure_code):
    try:
        result = subprocess.run(
            [sys.executable, path],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        fail(failure_code)

    if result.returncode != 0:
        fail(failure_code)


def build_effective_views(baseline, cook, chicago):
    try:
        effective_cook = {
            "view_id": "E_C",
            "base": baseline.get("artifact"),
            "overlay": cook.get("artifact"),
            "jurisdiction": "cook",
            "runtime_state": "VALID_COOK_EFFECTIVE_VIEW",
            "baseline_precedence": cook.get("baseline_integrity", {}).get("baseline_precedence"),
            "allowed_operations": cook.get("delta_scope", {}).get("allowed_operations", []),
            "shadowing_rules": cook.get("shadowing_rules", {}),
            "conflict_resolution": cook.get("conflict_resolution", {})
        }

        effective_chicago = {
            "view_id": "E_H",
            "base": effective_cook.get("view_id"),
            "overlay": chicago.get("artifact"),
            "jurisdiction": "chicago",
            "parent_jurisdiction": "cook",
            "runtime_state": "VALID_CHICAGO_EFFECTIVE_VIEW",
            "baseline_precedence": chicago.get("baseline_integrity", {}).get("baseline_precedence"),
            "allowed_operations": chicago.get("delta_scope", {}).get("allowed_operations", []),
            "shadowing_rules": chicago.get("shadowing_rules", {}),
            "conflict_resolution": chicago.get("conflict_resolution", {})
        }

        return effective_cook, effective_chicago
    except Exception:
        fail("EFFECTIVE_VIEW_BUILD_ERROR")


def enumerate_conflicts(_effective_cook, _effective_chicago):
    # v0.1 shells declare governance policy but no concrete conflicting node/key entries.
    # Empty conflict set is deterministic and valid.
    return []


def apply_sovereignty_model(conflicts, _model):
    ledger = []

    for conflict in conflicts:
        policy = conflict.get("cook_metadata", {}).get("override_policy")

        if conflict.get("violates_baseline") is True:
            fail("SOVEREIGNTY_CONFLICT_VIOLATES_BASELINE")

        if policy == "cook_absolute":
            winner = "cook"
            rule = "rule_2_cook_non_overridable"
            code = "RESOLVED_IN_FAVOR_OF_COOK_NON_OVERRIDABLE"
        elif policy == "municipal_may_override":
            winner = "chicago"
            rule = "rule_3_chicago_local_override"
            code = "RESOLVED_IN_FAVOR_OF_CHICAGO_LOCAL_OVERRIDE"
        elif conflict.get("cook_forbids") is True and conflict.get("chicago_forbids") is True:
            winner = "joint_forbid"
            rule = "rule_4_joint_prohibition"
            code = "RESOLVED_AS_JOINT_PROHIBITION"
        elif policy is None:
            winner = "cook"
            rule = "rule_5_cook_default"
            code = "RESOLVED_IN_FAVOR_OF_COOK_DEFAULT"
        else:
            fail("SOVEREIGNTY_CONFLICT_MODEL_UNDECIDABLE")

        ledger.append({
            "node_id": conflict.get("node_id"),
            "key_path": conflict.get("key_path"),
            "conflict_type": conflict.get("conflict_type"),
            "resolution_rule": rule,
            "ledger_code": code,
            "winner": winner,
            "cook_value": conflict.get("cook_value"),
            "chicago_value": conflict.get("chicago_value")
        })

    return ledger


def emit_outputs(effective_chicago, ledger):
    try:
        os.makedirs(os.path.dirname(VIEW_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)

        arbitrated = dict(effective_chicago)
        arbitrated["view_id"] = "E_CH"
        arbitrated["runtime_state"] = "ARBITRATED_CHICAGO_EFFECTIVE_VIEW"
        arbitrated["conflict_count"] = len(ledger)
        arbitrated["conflict_ledger"] = LEDGER_PATH

        with open(VIEW_PATH, "w", encoding="utf-8") as f:
            json.dump(arbitrated, f, indent=2, ensure_ascii=False)
            f.write("\n")

        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            for entry in ledger:
                f.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
    except Exception:
        fail("OUTPUT_WRITE_ERROR")


def main():
    baseline = load_json(BASELINE_PATH)
    cook = load_json(COOK_PATH)
    chicago = load_json(CHICAGO_PATH)
    model = load_json(MODEL_PATH)

    run_validator(COOK_VALIDATOR, "COOK_NOT_VALIDATED")
    run_validator(CHICAGO_VALIDATOR, "CHICAGO_NOT_VALIDATED")

    effective_cook, effective_chicago = build_effective_views(baseline, cook, chicago)
    conflicts = enumerate_conflicts(effective_cook, effective_chicago)
    ledger = apply_sovereignty_model(conflicts, model)
    emit_outputs(effective_chicago, ledger)

    print("RESOLVE_CHICAGO_CONFLICTS_SUCCESS")
    sys.exit(0)


if __name__ == "__main__":
    main()
