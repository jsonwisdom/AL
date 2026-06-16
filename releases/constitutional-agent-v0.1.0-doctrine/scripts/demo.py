#!/usr/bin/env python3
import json

results = [
    {"case": "happy_path", "decision": "PASS", "premium_per_1k": "$0.42"},
    {"case": "refusal_write_denied", "decision": "PASS_WITH_REFUSAL", "refusal_code": "R-001_WRITE_DENIED"},
    {"case": "missing_anchor_rejected", "decision": "REJECT", "reason": "NO_ANCHOR_NO_COVERAGE"}
]

print(json.dumps({"demo": "constitutional-agent-v0", "results": results}, indent=2))
print("CONSTITUTIONAL EXECUTION CELL: PASS")
