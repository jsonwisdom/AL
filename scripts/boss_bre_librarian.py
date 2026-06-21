#!/usr/bin/env python3
"""Boss Bre Librarian.
Scans jurisdiction receipts and comments a master summary on issue #348.
Doctrine: NO_FAKE_GREEN. Summaries only; no public claim promotion.
"""

import glob
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
RECEIPTS = sorted(glob.glob(str(ROOT / "projects/mn-fiscal-replay/live_fetch/*/MN_001_forensic_receipt.json")))
MASTER_ISSUE = os.environ.get("BOSS_BRE_MASTER_ISSUE", "348")

summary = {
    "utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "lanes": [],
    "blocked": 0,
    "missing_payload": 0,
    "review_required": 0,
    "no_diff_detected": 0,
    "confirmed_green": 0,
}

for receipt_path in RECEIPTS:
    lane = Path(receipt_path).parent.name
    try:
        receipt = json.loads(Path(receipt_path).read_text())
    except Exception as exc:
        receipt = {
            "status": "RECEIPT_PARSE_BLOCKED",
            "public_content_claim": "BLOCKED",
            "blocked_reason": str(exc),
        }

    status = receipt.get("status", "UNKNOWN")
    claim = receipt.get("public_content_claim", "BLOCKED")
    counts = receipt.get("counts", {})

    row = {
        "lane": lane,
        "status": status,
        "claim": claim,
        "possible_content_deltas": counts.get("possible_content_deltas"),
        "table_layout_reflow": counts.get("table_layout_reflow"),
        "page_header_shift": counts.get("page_header_shift"),
    }
    summary["lanes"].append(row)

    if claim == "BLOCKED":
        summary["blocked"] += 1
    if status == "FORENSIC_PAYLOAD_MISSING":
        summary["missing_payload"] += 1
    elif status == "FORENSIC_REVIEW_REQUIRED":
        summary["review_required"] += 1
    elif status == "NO_DIFF_DETECTED":
        summary["no_diff_detected"] += 1
    elif claim != "BLOCKED":
        summary["confirmed_green"] += 1

body = f"""## Boss Bre 15m Sweep Summary
UTC: {summary['utc']}

**Gate status**
- BLOCKED: {summary['blocked']}
- MISSING PAYLOAD: {summary['missing_payload']}
- REVIEW REQUIRED: {summary['review_required']}
- NO DIFF DETECTED: {summary['no_diff_detected']}
- CONFIRMED GREEN: {summary['confirmed_green']}

**Lanes**
```json
{json.dumps(summary['lanes'], indent=2)}
```

PUBLIC_CONTENT_CLAIM: BLOCKED_BY_DEFAULT  
HUMAN_REVIEW_REQUIRED: TRUE  
NO_FAKE_GREEN: ACTIVE
"""

subprocess.run(["gh", "issue", "comment", MASTER_ISSUE, "--body", body], check=False)

# Open per-lane issues only when review is required. Missing payload stays on master summary to avoid issue spam.
for lane in summary["lanes"]:
    if lane["status"] != "FORENSIC_REVIEW_REQUIRED":
        continue
    title = f"{lane['lane']} forensic review required"
    issue_body = (
        f"Auto-opened by Boss Bre.\n\n"
        f"Lane: {lane['lane']}\n"
        f"Status: {lane['status']}\n"
        f"Claim: {lane['claim']}\n"
        f"Possible content deltas: {lane.get('possible_content_deltas')}\n\n"
        "PUBLIC_CONTENT_CLAIM: BLOCKED\n"
        "HUMAN_REVIEW_REQUIRED: TRUE\n"
        "NO_FAKE_GREEN: ACTIVE\n"
    )
    subprocess.run([
        "gh", "issue", "create",
        "--title", title,
        "--body", issue_body,
        "--label", "forensic-review",
        "--label", "NO_FAKE_GREEN",
    ], check=False)
