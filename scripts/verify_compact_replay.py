#!/usr/bin/env python3
import hashlib
import json
import os
import sys

COMPACT_PATH = sys.argv[1] if len(sys.argv) > 1 else "federation/compacts/example-compact-v0.1.json"
PARTICIPANT_EPOCH_DIR = sys.argv[2] if len(sys.argv) > 2 else "federation/participant_epochs"
COMPACT_LEDGER_PATH = sys.argv[3] if len(sys.argv) > 3 else "federation/logs/compact_ledger_v0.1.jsonl"

REQUIRED_COMPACT_CONSTRAINTS = {
    "baseline_mutation": "forbidden",
    "state_sovereignty": "preserved"
}


def fail(code):
    print(f"VERIFY_COMPACT_REPLAY_FAILED:{code}")
    sys.exit(1)


def read_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        fail("MISSING_ARTIFACT")
    except Exception:
        fail("INVALID_JSON")


def load_json(path):
    try:
        return json.loads(read_bytes(path))
    except SystemExit:
        raise
    except Exception:
        fail("INVALID_JSON")


def load_jsonl(path):
    try:
        rows = []
        raw = read_bytes(path).decode("utf-8")
        for line in raw.splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows
    except SystemExit:
        raise
    except Exception:
        fail("INVALID_JSON")


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_hash(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256_bytes(raw)


def validate_compact_schema(compact):
    for key in ["compact_id", "participants", "subject_matter", "constraints", "obligations"]:
        if key not in compact:
            fail("INVALID_COMPACT_SCHEMA")

    constraints = compact.get("constraints", {})
    for key, expected in REQUIRED_COMPACT_CONSTRAINTS.items():
        if constraints.get(key) != expected:
            fail("INVALID_COMPACT_SCHEMA")

    if not isinstance(compact.get("participants"), list) or not compact["participants"]:
        fail("INVALID_COMPACT_SCHEMA")


def load_participant_epochs(compact):
    epochs = {}
    for participant in compact["participants"]:
        state = participant.get("state")
        epoch_id = participant.get("epoch_id")
        epoch_root = participant.get("epoch_root_sha256")
        if not state or not epoch_id or not epoch_root:
            fail("INVALID_COMPACT_SCHEMA")

        path = os.path.join(PARTICIPANT_EPOCH_DIR, f"{epoch_id}.json")
        epoch = load_json(path)
        epochs[state] = epoch

        recorded_root = epoch.get("merkle_root_sha256") or epoch.get("epoch_root_sha256")
        if recorded_root != epoch_root:
            fail(f"EPOCH_ROOT_MISMATCH:{state}")

    return epochs


def recompute_epoch_root(state, epoch):
    # V1 accepts either a root-only participant epoch or a governance_epoch_root_v0.1-style object.
    if "leaf_hashes" not in epoch:
        if epoch.get("merkle_root_sha256") or epoch.get("epoch_root_sha256"):
            return epoch.get("merkle_root_sha256") or epoch.get("epoch_root_sha256")
        fail(f"STATE_EPOCH_ROOT_MISMATCH:{state}")

    h = epoch["leaf_hashes"]
    required = [
        "baseline_sha256",
        "cook_sha256",
        "chicago_sha256",
        "sovereignty_model_sha256",
        "effective_view_sha256",
        "conflict_ledger_sha256"
    ]
    if not all(k in h for k in required):
        fail(f"STATE_EPOCH_ROOT_MISMATCH:{state}")

    def hcat(a, b):
        return hashlib.sha256((a + b).encode("utf-8")).hexdigest()

    l1 = hcat(h["baseline_sha256"], h["cook_sha256"])
    l2 = hcat(h["chicago_sha256"], h["sovereignty_model_sha256"])
    l3 = hcat(h["effective_view_sha256"], h["conflict_ledger_sha256"])
    i1 = hcat(l1, l2)
    return hcat(i1, l3)


def verify_epoch_roots(compact, epochs):
    for participant in compact["participants"]:
        state = participant["state"]
        expected = participant["epoch_root_sha256"]
        computed = recompute_epoch_root(state, epochs[state])
        if computed != expected:
            fail(f"STATE_EPOCH_ROOT_MISMATCH:{state}")


def enumerate_compact_conflicts(compact, _epochs):
    # V1 compact schema may declare replayable conflict records directly.
    return compact.get("conflicts", [])


def compact_conflict_key(row):
    return (
        str(row.get("state_pair")),
        str(row.get("key_path")),
        str(row.get("conflict_type"))
    )


def verify_ledger(conflicts, ledger):
    if sorted(map(compact_conflict_key, conflicts)) != sorted(map(compact_conflict_key, ledger)):
        fail("COMPACT_CONFLICT_ENUMERATION_MISMATCH")

    by_key = {compact_conflict_key(row): row for row in ledger}
    for conflict in conflicts:
        key = compact_conflict_key(conflict)
        recorded = by_key.get(key)
        if recorded is None:
            fail("COMPACT_CONFLICT_ENUMERATION_MISMATCH")

        expected_rule = conflict.get("resolution_rule")
        if expected_rule and recorded.get("resolution_rule") != expected_rule:
            fail("COMPACT_LEDGER_RESOLUTION_MISMATCH")

        if conflict.get("baseline_mutation") is True:
            fail("COMPACT_MUTATES_STATE_BASELINE")


def verify_no_baseline_mutation(compact, ledger):
    constraints = compact.get("constraints", {})
    if constraints.get("baseline_mutation") != "forbidden":
        fail("COMPACT_MUTATES_STATE_BASELINE")

    for row in ledger:
        if row.get("baseline_mutation") is True:
            state = row.get("state") or "UNKNOWN"
            fail(f"COMPACT_VIOLATES_STATE_SOVEREIGNTY:{state}")


def main():
    compact_raw = read_bytes(COMPACT_PATH)
    compact = load_json(COMPACT_PATH)
    ledger = load_jsonl(COMPACT_LEDGER_PATH)

    sha256_bytes(compact_raw)
    validate_compact_schema(compact)
    epochs = load_participant_epochs(compact)
    verify_epoch_roots(compact, epochs)

    conflicts = enumerate_compact_conflicts(compact, epochs)
    verify_ledger(conflicts, ledger)
    verify_no_baseline_mutation(compact, ledger)

    print("VERIFY_COMPACT_REPLAY_SUCCESS")
    sys.exit(0)


if __name__ == "__main__":
    main()
