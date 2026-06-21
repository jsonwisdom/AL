#!/usr/bin/env python3
import sys
import json

KEYS = [
    "raw_pdf_sha256",
    "normalized_pdf_text_sha256",
    "extracted_table_sha256",
    "http_metadata_sha256"
]

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if len(sys.argv) < 3:
    print("Usage: compare_receipts.py <baseline.json> <current.json>")
    sys.exit(1)

baseline = load(sys.argv[1])
current = load(sys.argv[2])

comparable = [k for k in KEYS if k in baseline and k in current]

if not comparable:
    print(json.dumps({"status": "NO_COMPARABLE_HASH_FIELDS"}, indent=2))
    sys.exit(0)

diffs = {}
for k in comparable:
    if baseline.get(k) != current.get(k):
        diffs[k] = {
            "baseline": baseline.get(k),
            "current": current.get(k)
        }

if diffs:
    print("ANOMALY_DETECTED")
    print(json.dumps(diffs, indent=2))
else:
    print("NO_ANOMALY")
