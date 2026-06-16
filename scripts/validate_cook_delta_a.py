#!/usr/bin/env python3
import hashlib
import json
import sys

COOK_PATH = "seeds/illinois/cook-delta-a-v0.1.json"
BASELINE_PATH = "seeds/illinois/downstate-baseline-v0.1.json"

ALLOWED_OPS = {"add", "shadow"}
FORBIDDEN_OPS = {"delete", "rebase", "rewrite"}


def reject(code):
    print(f"INVALID_COOK_DELTA_A:{code}")
    sys.exit(1)


def load_json_bytes(path, code):
    try:
        with open(path, "rb") as f:
            raw = f.read()
        return json.loads(raw), raw
    except Exception:
        reject(code)


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def check_overlay_contract(cook):
    if "extends" not in cook:
        reject("MISSING_EXTENDS_FIELD")

    if "overlay_type" not in cook:
        reject("OVERLAY_TYPE_MISSING")

    if cook.get("extends") != BASELINE_PATH:
        reject("EXTENDS_TARGET_MISMATCH")

    if cook.get("overlay_type") != "QUASI_STATE_COUNTY_DELTA":
        reject("OVERLAY_TYPE_INVALID")

    bi = cook.get("baseline_integrity", {})

    if bi.get("modifies_baseline") is not False:
        reject("MODIFIES_BASELINE_NOT_FALSE")

    if bi.get("baseline_precedence") != "absolute":
        reject("BASELINE_PRECEDENCE_NOT_ABSOLUTE")

    shadow = cook.get("shadowing_rules", {})

    if shadow.get("shadowing_allowed") != "delta_scoped_only":
        reject("SHADOWING_POLICY_VIOLATION")

    if shadow.get("cross_jurisdiction_shadowing") != "forbidden":
        reject("SHADOWING_POLICY_VIOLATION")


def recompute_baseline_hash(cook, baseline_bytes):
    computed_hash = sha256_bytes(baseline_bytes)
    bi = cook.get("baseline_integrity", {})
    baseline_hash = bi.get("baseline_hash")

    if baseline_hash is None:
        reject("BASELINE_HASH_MISSING")

    if baseline_hash == "PENDING_BASELINE_SHA256":
        return computed_hash, "BASELINE_HASH_PENDING"

    if baseline_hash != computed_hash:
        reject("BASELINE_HASH_MISMATCH")

    return computed_hash, "BASELINE_HASH_MATCH"


def compute_declared_delta_ops(cook):
    scope = cook.get("delta_scope", {})
    allowed = set(scope.get("allowed_operations", []))
    forbidden = set(scope.get("forbidden_operations", []))

    # v0.1 overlay shell declares operation classes, not a concrete diff graph yet.
    # Treat declared operation policy as the executable graph boundary for this stage.
    return allowed, forbidden


def enforce_allowed_operations(allowed, forbidden):
    if not allowed.issubset(ALLOWED_OPS):
        reject("DECLARED_ALLOWED_OPERATION_INVALID")

    if forbidden != FORBIDDEN_OPS:
        reject("FORBIDDEN_OPERATION_SET_MISMATCH")

    if allowed & forbidden:
        reject("OPERATION_POLICY_CONFLICT")


def enforce_shadowing_scope(cook):
    scope = cook.get("delta_scope", {})
    shadow = cook.get("shadowing_rules", {})

    if scope.get("jurisdiction") != "cook":
        reject("DELTA_SCOPE_NOT_COOK")

    if shadow.get("cross_jurisdiction_shadowing") != "forbidden":
        reject("CROSS_JURISDICTION_SHADOWING_DETECTED")

    if shadow.get("shadowing_allowed") != "delta_scoped_only":
        reject("GLOBAL_NODE_SHADOWING_FORBIDDEN")


def topology_contamination_check(cook, baseline):
    if baseline.get("topology_model") != "DOWNSTATE_LINEAR_TOPOLOGY":
        reject("BASELINE_TOPOLOGY_INVALID")

    if cook.get("baseline_integrity", {}).get("modifies_baseline") is not False:
        reject("BASELINE_TOPOLOGY_MUTATION_DETECTED")

    if cook.get("conflict_resolution", {}).get("baseline_precedence") != "absolute":
        reject("DOWNSTATE_LINEAR_TOPOLOGY_CONTAMINATED")

    blocked = set(cook.get("blocked_actions", []))
    required = {
        "baseline_mutation",
        "baseline_topology_rewrite",
        "cross_jurisdiction_shadowing",
        "overlay_delete_baseline_nodes",
        "overlay_rebase"
    }

    if not required.issubset(blocked):
        reject("BLOCKED_ACTIONS_INCOMPLETE")


def main():
    cook_path = sys.argv[1] if len(sys.argv) > 1 else COOK_PATH
    baseline_path = sys.argv[2] if len(sys.argv) > 2 else BASELINE_PATH

    if cook_path != COOK_PATH:
        reject("COOK_PATH_MISMATCH")

    if baseline_path != BASELINE_PATH:
        reject("BASELINE_PATH_MISMATCH")

    cook, _cook_bytes = load_json_bytes(cook_path, "INVALID_COOK_JSON")
    baseline, baseline_bytes = load_json_bytes(baseline_path, "INVALID_BASELINE_JSON")

    check_overlay_contract(cook)
    recompute_baseline_hash(cook, baseline_bytes)
    allowed, forbidden = compute_declared_delta_ops(cook)
    enforce_allowed_operations(allowed, forbidden)
    enforce_shadowing_scope(cook)
    topology_contamination_check(cook, baseline)

    print("VALID_COOK_DELTA_A")
    sys.exit(0)


if __name__ == "__main__":
    main()
