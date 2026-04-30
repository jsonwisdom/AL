#!/usr/bin/env python3
import json, hashlib, datetime, os
from statistics import median

LEAF_PATH = "_truth/edu_civil_rights/mn/MN_EDU_CIVIL_RIGHTS_001.leaf.json"
DELTA_DIR = "_truth/edu_civil_rights/mn/deltas"

RESOLUTION_OUTCOMES = set([
    "POSITIVE_RESOLUTION",
    "DISMISSAL",
    "MEDIATED_WITH_REMEDY",
    "MEDIATED_WITHOUT_REMEDY",
    "VOLUNTARY_RESOLUTION_AGREEMENT",
    "CORRECTIVE_ACTION_REQUIRED",
    "NO_VIOLATION_FOUND",
    "WITHDRAWN",
    "REFERRED",
    "ADMINISTRATIVE_CLOSURE"
])

POSITIVE_RESOLUTION_OUTCOMES = set([
    "POSITIVE_RESOLUTION",
    "CORRECTIVE_ACTION_REQUIRED",
    "VOLUNTARY_RESOLUTION_AGREEMENT",
    "MEDIATED_WITH_REMEDY"
])

DISMISSAL_OUTCOMES = set([
    "DISMISSAL",
    "ADMINISTRATIVE_CLOSURE"
])

PENDING_OUTCOMES = set([
    "PENDING"
])

MEDIATED_OUTCOMES = set([
    "MEDIATED_WITH_REMEDY",
    "MEDIATED_WITHOUT_REMEDY"
])

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

with open(LEAF_PATH, "r", encoding="utf-8") as f:
    leaf = json.load(f)

rows = leaf.get("data", {}).get("agency_breakdown", [])

case_count = 0
resolution_count = 0
positive_resolution_count = 0
dismissal_count = 0
pending_count = 0
mediated_count = 0
days_to_resolution = []

for r in rows:
    case_count += 1
    outcome = r.get("case_outcome")
    days = r.get("days_to_resolution")

    if outcome in RESOLUTION_OUTCOMES:
        resolution_count += 1

    if outcome in POSITIVE_RESOLUTION_OUTCOMES:
        positive_resolution_count += 1

    if outcome in DISMISSAL_OUTCOMES:
        dismissal_count += 1

    if outcome in PENDING_OUTCOMES:
        pending_count += 1

    if outcome in MEDIATED_OUTCOMES:
        mediated_count += 1

    if isinstance(days, (int, float)):
        days_to_resolution.append(days)

median_days_to_resolution = median(days_to_resolution) if days_to_resolution else None

leaf["data"]["aggregates"] = {
    "case_count": case_count,
    "resolution_count": resolution_count,
    "positive_resolution_count": positive_resolution_count,
    "dismissal_count": dismissal_count,
    "pending_count": pending_count,
    "mediated_count": mediated_count,
    "median_days_to_resolution": median_days_to_resolution
}

leaf["numeric_fields_populated"] = case_count > 0
leaf["ingest_status"] = "AGGREGATED_FROM_VALIDATED_ROWS"
leaf["hash"]["value"] = None
leaf_hash = sha256_hex(canonical_json(leaf))
leaf["hash"]["value"] = leaf_hash

with open(LEAF_PATH, "w", encoding="utf-8") as f:
    json.dump(leaf, f, indent=2, sort_keys=True)
    f.write("\n")

os.makedirs(DELTA_DIR, exist_ok=True)
ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
delta_path = f"{DELTA_DIR}/{ts.replace(':', '')}_aggregate_delta.json"
with open(delta_path, "w", encoding="utf-8") as f:
    json.dump({
        "timestamp": ts,
        "receipt_id": "MN_EDU_CIVIL_RIGHTS_001",
        "status": "AGGREGATED",
        "hash": leaf_hash,
        "aggregates": leaf["data"]["aggregates"],
        "rules": {
            "pending_is_not_resolution": True,
            "aggregation_source": "validated_rows_only",
            "inference": "disabled"
        }
    }, f, indent=2, sort_keys=True)
    f.write("\n")

print(f"Aggregates computed. Hash: {leaf_hash}")
print(f"Delta: {delta_path}")
