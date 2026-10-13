import sys, json

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

rows = json.load(sys.stdin)["rows"]

out = []
for r in rows:
    out.append({
        "year": None,
        "state": "Minnesota",
        "agency": None,
        "office": None,
        "complaint_category": None,
        "case_count": None,
        "resolution_count": None,
        "positive_resolution_count": None,
        "dismissal_count": None,
        "pending_count": None,
        "mediated_count": None,
        "median_days_to_resolution": None,
        "source_url": None,
        "source_hash": None,
        "retrieved_at": None,
        "raw_row": r
    })

json.dump(out, sys.stdout, indent=2)
