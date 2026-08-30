#!/usr/bin/env python3
import json, glob, sys

states = []

for path in glob.glob("_truth/edu_civil_rights/*/*_EDU_CIVIL_RIGHTS_001.leaf.json"):
    leaf = json.load(open(path))
    data = leaf.get("data", {})
    ag = data.get("aggregates")

    if not ag:
        continue

    if not leaf.get("numeric_fields_populated"):
        continue

    if not leaf.get("hash", {}).get("value"):
        continue

    states.append({
        "state": data.get("state"),
        "year": data.get("year"),
        "case_count": ag.get("case_count"),
        "resolution_count": ag.get("resolution_count"),
        "positive_resolution_count": ag.get("positive_resolution_count"),
        "hash": leaf.get("hash", {}).get("value")
    })

json.dump({"states": states}, sys.stdout, indent=2, sort_keys=True)
