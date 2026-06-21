#!/usr/bin/env python3
"""Boss Bre Librarian v1.6.
Scans jurisdiction receipts, scanner inventory, learning state, and v1.5 scan results;
comments master summary on issue #348 and routes review-required lanes without claim promotion.
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
BOSS_BRE_DIR = ROOT / "projects/mn-fiscal-replay/boss_bre"
LATEST_SCAN = BOSS_BRE_DIR / "latest_sweep_summary.json"
LEARN_FILE = BOSS_BRE_DIR / "boss_bre_learning_state.json"
SIM_SCAN_RECEIPT = BOSS_BRE_DIR / "BOSS_BRE_SIMULATED_ARTIFACT_SCAN_V1_5_RECEIPT.json"
SIM_SCAN_DETAILS = BOSS_BRE_DIR / "BOSS_BRE_SIMULATED_ARTIFACT_SCAN_V1_5_DETAILS.jsonl"


def read_json(path, fallback):
    try:
        return json.loads(Path(path).read_text())
    except Exception as exc:
        data = dict(fallback)
        data["blocked_reason"] = str(exc)
        data["public_content_claim"] = "BLOCKED_PENDING_HUMAN_REVIEW"
        data["no_fake_green"] = True
        return data


def gh(args):
    return subprocess.run(["gh"] + args, text=True, capture_output=True, check=False)


summary = {
    "utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "routing_version": "1.6",
    "lanes": [],
    "blocked": 0,
    "missing_payload": 0,
    "review_required": 0,
    "no_diff_detected": 0,
    "non_blocked_summary_count": 0,
    "routed_review_count": 0,
}

for receipt_path in RECEIPTS:
    lane = Path(receipt_path).parent.name
    try:
        receipt = json.loads(Path(receipt_path).read_text())
    except Exception as exc:
        receipt = {
            "status": "RECEIPT_PARSE_BLOCKED",
            "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
            "blocked_reason": str(exc),
        }

    status = receipt.get("status", "UNKNOWN")
    claim = receipt.get("public_content_claim", "BLOCKED_PENDING_HUMAN_REVIEW")
    counts = receipt.get("counts", {})

    row = {
        "lane": lane,
        "status": status,
        "claim": claim,
        "possible_content_deltas": counts.get("possible_content_deltas"),
        "table_layout_reflow": counts.get("table_layout_reflow"),
        "page_header_shift": counts.get("page_header_shift"),
        "routing": "MASTER_SUMMARY_ONLY",
    }

    if status == "FORENSIC_REVIEW_REQUIRED":
        row["routing"] = "HUMAN_REVIEW_QUEUE"

    summary["lanes"].append(row)

    if str(claim).startswith("BLOCKED"):
        summary["blocked"] += 1
    if status == "FORENSIC_PAYLOAD_MISSING":
        summary["missing_payload"] += 1
    elif status == "FORENSIC_REVIEW_REQUIRED":
        summary["review_required"] += 1
    elif status == "NO_DIFF_DETECTED":
        summary["no_diff_detected"] += 1
    elif not str(claim).startswith("BLOCKED"):
        summary["non_blocked_summary_count"] += 1

scan_summary = read_json(
    LATEST_SCAN,
    {"status": "SCAN_SUMMARY_MISSING_OR_PARSE_BLOCKED"},
)
learning_state = read_json(
    LEARN_FILE,
    {"status": "LEARNING_STATE_MISSING_OR_PARSE_BLOCKED"},
)
sim_scan_receipt = read_json(
    SIM_SCAN_RECEIPT,
    {"status": "SIMULATED_ARTIFACT_SCAN_RECEIPT_MISSING_OR_PARSE_BLOCKED"},
)

sim_details = []
try:
    for line in SIM_SCAN_DETAILS.read_text().splitlines():
        if line.strip():
            sim_details.append(json.loads(line))
except Exception as exc:
    sim_details = [{
        "status": "SIMULATED_ARTIFACT_SCAN_DETAILS_MISSING_OR_PARSE_BLOCKED",
        "blocked_reason": str(exc),
        "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
        "no_fake_green": True,
    }]

body = f"""## Boss Bre 15m Sweep Summary v1.6
UTC: {summary['utc']}

**Scanner / learning state**
```json
{json.dumps(scan_summary, indent=2)}
```

**What Boss Bre learned for next run**
```json
{json.dumps(learning_state, indent=2)}
```

**Simulated artifact scan v1.5**
```json
{json.dumps(sim_scan_receipt, indent=2)}
```

**Simulated artifact scan details**
```json
{json.dumps(sim_details, indent=2)}
```

**Gate status**
- BLOCKED: {summary['blocked']}
- MISSING PAYLOAD: {summary['missing_payload']}
- REVIEW REQUIRED: {summary['review_required']}
- NO DIFF DETECTED: {summary['no_diff_detected']}
- NON-BLOCKED SUMMARY COUNT: {summary['non_blocked_summary_count']}
- ROUTED REVIEW COUNT: {summary['routed_review_count']}

**Lanes**
```json
{json.dumps(summary['lanes'], indent=2)}
```

PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW  
HUMAN_REVIEW_REQUIRED: TRUE  
NO_FAKE_GREEN: ACTIVE
"""

gh(["issue", "comment", MASTER_ISSUE, "--body", body])

# Open per-lane issues only when review is required. Missing payload stays on master summary to avoid issue spam.
for lane in summary["lanes"]:
    if lane["status"] != "FORENSIC_REVIEW_REQUIRED":
        continue

    title = f"Boss Bre review queue: {lane['lane']} forensic review required"
    existing = gh([
        "issue", "list",
        "--state", "open",
        "--search", f"{title} in:title",
        "--json", "number,title",
        "--limit", "10",
    ])
    if existing.returncode == 0:
        try:
            rows = json.loads(existing.stdout or "[]")
        except Exception:
            rows = []
        if any(row.get("title") == title for row in rows):
            continue

    issue_body = (
        "Auto-opened by Boss Bre v1.6 routing.\n\n"
        f"Lane: {lane['lane']}\n"
        f"Status: {lane['status']}\n"
        f"Claim: {lane['claim']}\n"
        f"Possible content deltas: {lane.get('possible_content_deltas')}\n\n"
        "Routing posture: HUMAN_REVIEW_QUEUE only.\n"
        "No public finding or final conclusion is authorized by this issue.\n\n"
        "PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW\n"
        "HUMAN_REVIEW_REQUIRED: TRUE\n"
        "NO_FAKE_GREEN: ACTIVE\n"
    )
    created = gh([
        "issue", "create",
        "--title", title,
        "--body", issue_body,
        "--label", "forensic-review",
        "--label", "NO_FAKE_GREEN",
    ])
    if created.returncode == 0:
        summary["routed_review_count"] += 1
