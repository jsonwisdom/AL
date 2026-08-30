#!/usr/bin/env python3
import json, glob, os, sys

states = []

for path in sorted(glob.glob("_truth/edu_civil_rights/*/*_EDU_CIVIL_RIGHTS_001.leaf.json")):
    leaf = json.load(open(path))
    data = leaf.get("data", {})
    aggregates = data.get("aggregates")
    state_code = os.path.basename(os.path.dirname(path)).upper()
    hash_present = bool(leaf.get("hash", {}).get("value"))
    numeric_fields_populated = bool(leaf.get("numeric_fields_populated"))
    aggregates_present = aggregates is not None

    states.append({
        "state_code": state_code,
        "state_name": data.get("state"),
        "year": data.get("year"),
        "leaf_path": path,
        "schema_status": leaf.get("schema_status"),
        "ingest_status": leaf.get("ingest_status"),
        "numeric_fields_populated": numeric_fields_populated,
        "hash_present": hash_present,
        "aggregates_present": aggregates_present,
        "national_output_eligible": bool(numeric_fields_populated and hash_present and aggregates_present)
    })

json.dump({"states": states}, sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\n")
