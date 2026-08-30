#!/usr/bin/env python3
import json, glob, os, sys

TOTAL_STATES = 51  # 50 states + DC

ready = 0
states = []

for path in sorted(glob.glob("_truth/edu_civil_rights/*/*_EDU_CIVIL_RIGHTS_001.leaf.json")):
    leaf = json.load(open(path))
    data = leaf.get("data", {})
    state_code = os.path.basename(os.path.dirname(path)).upper()
    state = data.get("state")

    eligible = (
        leaf.get("numeric_fields_populated") is True and
        bool(leaf.get("hash", {}).get("value")) and
        data.get("aggregates") is not None
    )

    states.append({
        "state_code": state_code,
        "state": state,
        "leaf_path": path,
        "eligible": bool(eligible)
    })

    if eligible:
        ready += 1

coverage = ready / TOTAL_STATES

json.dump({
    "coverage_fraction": coverage,
    "coverage_percent": round(coverage * 100, 2),
    "states_ready": ready,
    "states_total": TOTAL_STATES,
    "states_with_leaf": len(states),
    "states_absent": TOTAL_STATES - len(states),
    "state_breakdown": states,
    "rule": {
        "absent_states_count_in_denominator": True,
        "absent_states_are_not_synthesized_as_rows": True,
        "eligibility_requires_numeric_fields_hash_and_aggregates": True
    }
}, sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\n")
