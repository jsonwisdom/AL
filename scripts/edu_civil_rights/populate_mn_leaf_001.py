#!/usr/bin/env python3
import sys, json, hashlib, datetime, os

LEAF_PATH = "_truth/edu_civil_rights/mn/MN_EDU_CIVIL_RIGHTS_001.leaf.json"
DELTA_DIR = "_truth/edu_civil_rights/mn/deltas"

VALID_CATEGORIES = set([
    "DISABILITY_SECTION_504",
    "DISABILITY_IDEA_RELATED",
    "RACE_COLOR_NATIONAL_ORIGIN",
    "SEX_TITLE_IX",
    "RETALIATION",
    "LANGUAGE_ACCESS",
    "RELIGION",
    "AGE",
    "DISCIPLINE_DISPARITY",
    "ACCESSIBILITY_PHYSICAL_OR_DIGITAL",
    "HARASSMENT_HOSTILE_ENVIRONMENT",
    "SPECIAL_EDUCATION_SERVICES",
    "OTHER_CIVIL_RIGHTS",
    "UNKNOWN_OR_UNCLASSIFIED"
])

VALID_OUTCOMES = set([
    "POSITIVE_RESOLUTION",
    "DISMISSAL",
    "MEDIATED_WITH_REMEDY",
    "MEDIATED_WITHOUT_REMEDY",
    "VOLUNTARY_RESOLUTION_AGREEMENT",
    "CORRECTIVE_ACTION_REQUIRED",
    "NO_VIOLATION_FOUND",
    "WITHDRAWN",
    "REFERRED",
    "ADMINISTRATIVE_CLOSURE",
    "PENDING",
    "UNKNOWN"
])

REQUIRED_ROW_KEYS = [
    "year",
    "state",
    "agency",
    "office",
    "complaint_category",
    "case_count",
    "resolution_count",
    "positive_resolution_count",
    "dismissal_count",
    "pending_count",
    "mediated_count",
    "median_days_to_resolution",
    "source_url",
    "source_hash",
    "retrieved_at",
    "raw_row"
]

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def validate_row(row, idx):
    errors = []
    for key in REQUIRED_ROW_KEYS:
        if key not in row:
            errors.append(f"row[{idx}] missing required key: {key}")

    cat = row.get("complaint_category")
    outcome = row.get("case_outcome")

    if cat is not None and cat not in VALID_CATEGORIES:
        errors.append(f"row[{idx}] invalid complaint_category: {cat}")

    if outcome is not None and outcome not in VALID_OUTCOMES:
        errors.append(f"row[{idx}] invalid case_outcome: {outcome}")

    if row.get("state") != "Minnesota":
        errors.append(f"row[{idx}] state must be Minnesota")

    return errors

def main():
    rows = json.load(sys.stdin)
    if not isinstance(rows, list):
        raise SystemExit("input must be a JSON array")

    with open(LEAF_PATH, "r", encoding="utf-8") as f:
        leaf = json.load(f)

    errors = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row[{idx}] is not an object")
            continue
        errors.extend(validate_row(row, idx))

    if errors:
        os.makedirs(DELTA_DIR, exist_ok=True)
        ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        error_delta = {
            "timestamp": ts,
            "receipt_id": "MN_EDU_CIVIL_RIGHTS_001",
            "status": "REJECTED",
            "errors": errors,
            "rows_attempted": len(rows)
        }
        delta_path = f"{DELTA_DIR}/{ts.replace(':', '')}_rejected_delta.json"
        with open(delta_path, "w", encoding="utf-8") as f:
            json.dump(error_delta, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"Rejected ingestion. Delta: {delta_path}")
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(65)

    leaf["data"]["agency_breakdown"] = rows
    leaf["numeric_fields_populated"] = False
    leaf["source_hashes_present"] = all(bool(r.get("source_hash")) for r in rows) if rows else False
    leaf["ingest_status"] = "POPULATED_WITH_VALIDATED_ROWS"

    leaf["hash"]["value"] = None
    leaf_hash = sha256_hex(canonical_json(leaf))
    leaf["hash"]["value"] = leaf_hash

    with open(LEAF_PATH, "w", encoding="utf-8") as f:
        json.dump(leaf, f, indent=2, sort_keys=True)
        f.write("\n")

    os.makedirs(DELTA_DIR, exist_ok=True)
    ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    delta = {
        "timestamp": ts,
        "receipt_id": "MN_EDU_CIVIL_RIGHTS_001",
        "status": "ACCEPTED",
        "hash": leaf_hash,
        "errors": [],
        "rows_ingested": len(rows)
    }
    delta_path = f"{DELTA_DIR}/{ts.replace(':', '')}_accepted_delta.json"
    with open(delta_path, "w", encoding="utf-8") as f:
        json.dump(delta, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Updated leaf. Hash: {leaf_hash}")
    print(f"Delta: {delta_path}")

if __name__ == "__main__":
    main()
