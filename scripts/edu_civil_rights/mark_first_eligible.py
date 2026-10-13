#!/usr/bin/env python3
import json, glob, os, datetime

def utc_ts():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def load_leaf(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def is_eligible(leaf):
    data = leaf.get("data", {})
    return (
        leaf.get("numeric_fields_populated") is True and
        bool(leaf.get("hash", {}).get("value")) and
        data.get("aggregates") is not None
    )

def has_first_eligible_event(delta_path, receipt_id):
    if not os.path.exists(delta_path):
        return False
    with open(delta_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            if entry.get("receipt_id") == receipt_id and entry.get("event") == "FIRST_ELIGIBLE":
                return True
    return False

for path in sorted(glob.glob("_truth/edu_civil_rights/*/*_EDU_CIVIL_RIGHTS_001.leaf.json")):
    leaf = load_leaf(path)
    data = leaf.get("data", {})
    receipt_id = leaf.get("receipt_id")
    state_dir = os.path.dirname(path)
    delta_path = os.path.join(state_dir, f"{receipt_id}.deltas.jsonl")

    if not is_eligible(leaf):
        continue

    if has_first_eligible_event(delta_path, receipt_id):
        continue

    entry = {
        "timestamp": utc_ts(),
        "receipt_id": receipt_id,
        "event": "FIRST_ELIGIBLE",
        "hash": leaf.get("hash", {}).get("value"),
        "numeric_fields_populated": leaf.get("numeric_fields_populated"),
        "aggregates": data.get("aggregates")
    }

    os.makedirs(state_dir, exist_ok=True)
    with open(delta_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")

    print(f"FIRST_ELIGIBLE recorded for {receipt_id}")
