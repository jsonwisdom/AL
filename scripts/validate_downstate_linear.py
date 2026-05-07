#!/usr/bin/env python3
import json
import sys

REQUIRED_COUNTY_NODES = {
    "SANGAMON_SHERIFF",
    "SANGAMON_CIRCUIT_CLERK",
    "SANGAMON_STATES_ATTORNEY"
}

REQUIRED_NODE_TAGS = {
    "STATE_LAYER",
    "COUNTY_LAYER",
    "MUNICIPAL_NON_SOVEREIGN"
}


def fail(msg):
    print(f"VALIDATION_FAIL: {msg}")
    sys.exit(1)


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("state") != "Illinois":
        fail("state mismatch")

    if data.get("topology_model") != "DOWNSTATE_LINEAR_TOPOLOGY":
        fail("topology_model mismatch")

    canon = data.get("canonicalization_order")
    if canon != ["state", "county", "municipal_non_sovereign"]:
        fail("canonicalization_order mismatch")

    rules = data.get("inheritance_rules", {})

    if rules.get("municipal_override_allowed") is not False:
        fail("municipal_override_allowed must be false")

    if rules.get("shadowing_allowed") is not False:
        fail("shadowing_allowed must be false")

    node_tags = set(data.get("node_tags", {}).keys())

    if node_tags != REQUIRED_NODE_TAGS:
        fail("node_tags mismatch")

    inst = data.get("sample_instantiation", {})
    nodes = inst.get("nodes", [])

    ids = {n.get("node_id") for n in nodes}

    missing = REQUIRED_COUNTY_NODES - ids

    if missing:
        fail(f"missing county nodes: {sorted(missing)}")

    municipal_nodes = [
        n for n in nodes
        if n.get("node_tag") == "MUNICIPAL_NON_SOVEREIGN"
    ]

    if not municipal_nodes:
        fail("missing municipal_non_sovereign node")

    print("VALIDATION_PASS: DOWNSTATE_LINEAR_TOPOLOGY_V1")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_downstate_linear.py <path>")
        sys.exit(1)

    main(sys.argv[1])
