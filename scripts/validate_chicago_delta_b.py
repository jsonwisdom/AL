#!/usr/bin/env python3
import hashlib
import json
import sys

BASELINE_PATH = "seeds/illinois/downstate-baseline-v0.1.json"
COOK_PATH = "seeds/illinois/cook-delta-a-v0.1.json"
CHICAGO_PATH = "seeds/illinois/chicago-delta-b-v0.1.json"

ALLOWED_OPS = {"add", "shadow"}
FORBIDDEN_OPS = {"delete", "rebase", "rewrite"}


def reject(code):
    print(f"INVALID_CHICAGO_DELTA_B:{code}")
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


def check_overlay_contract(chicago):
    if chicago.get("extends") != COOK_PATH:
        reject("EXTENDS_TARGET_MISMATCH")

    if chicago.get("overlay_type") != "MUNICIPAL_DELTA":
        reject("OVERLAY_TYPE_INVALID")

    bi = chicago.get("baseline_integrity", {})

    if bi.get("modifies_baseline") is not False:
        reject("MODIFIES_BASELINE_NOT_FALSE")

    if bi.get("baseline_precedence") != "absolute":
        reject("BASELINE_PRECEDENCE_NOT_ABSOLUTE")

    scope = chicago.get("delta_scope", {})

    if scope.get("jurisdiction") != "chicago":
        reject("DELTA_SCOPE_NOT_CHICAGO")

    if scope.get("parent_jurisdiction") != "cook":
        reject("PARENT_JURISDICTION_NOT_COOK")


def recompute_baseline_hash(chicago, baseline_bytes):
    computed_hash = sha256_bytes(baseline_bytes)
    bi = chicago.get("baseline_integrity", {})
    baseline_hash = bi.get("baseline_hash")

    if baseline_hash is None:
        reject("BASELINE_HASH_MISSING")

    if baseline_hash == "PENDING_BASELINE_SHA256":
        return computed_hash

    if baseline_hash != computed_hash:
        reject("BASELINE_HASH_MISMATCH")

    return computed_hash


def compute_declared_delta_ops(chicago):
    scope = chicago.get("delta_scope", {})
    allowed = set(scope.get("allowed_operations", []))
    forbidden = set(scope.get("forbidden_operations", []))
    return allowed, forbidden


def enforce_allowed_operations(allowed, forbidden):
    if not allowed.issubset(ALLOWED_OPS):
        reject("DECLARED_ALLOWED_OPERATION_INVALID")

    if forbidden != FORBIDDEN_OPS:
        reject("FORBIDDEN_OPERATION_SET_MISMATCH")


def enforce_shadowing_scope(chicago):
    shadow = chicago.get("shadowing_rules", {})

    if shadow.get("shadowing_allowed") != "delta_scoped_only":
        reject("SHADOWING_POLICY_VIOLATION")

    if shadow.get("cross_jurisdiction_shadowing") != "forbidden":
        reject("CROSS_JURISDICTION_SHADOWING_DETECTED")

    if shadow.get("upward_shadowing_into_cook") != "forbidden":
        reject("UPWARD_SHADOWING_INTO_COOK_DETECTED")

    if shadow.get("upward_shadowing_into_baseline") != "forbidden":
        reject("UPWARD_SHADOWING_INTO_BASELINE_DETECTED")


def topology_contamination_check(baseline):
    if baseline.get("topology_model") != "DOWNSTATE_LINEAR_TOPOLOGY":
        reject("DOWNSTATE_LINEAR_TOPOLOGY_CONTAMINATED")


def main():
    baseline, baseline_bytes = load_json_bytes(BASELINE_PATH, "INVALID_BASELINE_JSON")
    _cook, _cook_bytes = load_json_bytes(COOK_PATH, "INVALID_COOK_JSON")
    chicago, _chicago_bytes = load_json_bytes(CHICAGO_PATH, "INVALID_CHICAGO_JSON")

    check_overlay_contract(chicago)
    recompute_baseline_hash(chicago, baseline_bytes)

    allowed, forbidden = compute_declared_delta_ops(chicago)
    enforce_allowed_operations(allowed, forbidden)
    enforce_shadowing_scope(chicago)
    topology_contamination_check(baseline)

    print("VALID_CHICAGO_DELTA_B")
    sys.exit(0)


if __name__ == "__main__":
    main()
