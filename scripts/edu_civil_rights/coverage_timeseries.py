#!/usr/bin/env python3
import json, os, datetime

COVERAGE_PATH = "_truth/edu_civil_rights/national/coverage.json"
TIMESERIES_PATH = "_truth/edu_civil_rights/national/coverage_timeseries.jsonl"

if not os.path.exists(COVERAGE_PATH):
    raise SystemExit(f"missing coverage snapshot: {COVERAGE_PATH}")

with open(COVERAGE_PATH, "r", encoding="utf-8") as f:
    snapshot = json.load(f)

entry = {
    "timestamp": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    "coverage_fraction": snapshot.get("coverage_fraction"),
    "coverage_percent": snapshot.get("coverage_percent"),
    "states_ready": snapshot.get("states_ready"),
    "states_total": snapshot.get("states_total"),
    "states_with_leaf": snapshot.get("states_with_leaf"),
    "states_absent": snapshot.get("states_absent"),
    "state_breakdown": snapshot.get("state_breakdown"),
    "properties": {
        "append_only": True,
        "no_mutation": True,
        "no_interpretation": True,
        "no_smoothing": True
    }
}

os.makedirs(os.path.dirname(TIMESERIES_PATH), exist_ok=True)

with open(TIMESERIES_PATH, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")

print("Timeseries entry appended.")
print(TIMESERIES_PATH)
