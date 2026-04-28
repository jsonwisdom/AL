#!/usr/bin/env bash
set -euo pipefail

REPORT="${1:-docs/audit/ipfs_daily/latest.json}"

test -f "$REPORT"

jq -e '
  .repo == "jsonwisdom/AL" and
  .report_id == "ALMS_DAILY_IPFS_JSON_AUDIT" and
  (.json_file_count >= 0) and
  (.inventory_sha256 | test("^[a-f0-9]{64}$")) and
  (.verdict == "ALMS_IPFS_DAILY_JSON_LOCKED" or .verdict == "ALMS_IPFS_DAILY_JSON_WAIT")
' "$REPORT" >/dev/null

echo "ALMS_DAILY_IPFS_JSON_AUDIT_VERIFY_OK report=$REPORT"
