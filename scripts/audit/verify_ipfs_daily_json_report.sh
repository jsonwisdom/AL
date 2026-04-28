#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-standard}"
REPORT="${2:-docs/audit/ipfs_daily/latest.json}"

test -f "$REPORT"

jq -e '
  .repo == "jsonwisdom/AL" and
  .report_id == "ALMS_DAILY_IPFS_JSON_AUDIT" and
  .flywheel == "Meme Court Flywheel" and
  .sponsor == "jaywisdom.base" and
  (.json_file_count >= 0) and
  (.inventory_sha256 | test("^[a-f0-9]{64}$")) and
  (.verdict == "ALMS_IPFS_DAILY_JSON_LOCKED" or .verdict == "ALMS_IPFS_DAILY_JSON_WAIT")
' "$REPORT" >/dev/null

if [ "$MODE" = "--deep" ]; then
  DAY="$(jq -r '.date_utc' "$REPORT")"
  INV="_truth/audit/ipfs_daily/$DAY/inventory.jsonl"

  test -f "$INV"

  EXPECTED="$(jq -r '.inventory_sha256' "$REPORT")"
  ACTUAL="$(sha256sum "$INV" | awk '{print $1}')"

  if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "ALMS_DEEP_VERIFY_FAIL inventory_hash_mismatch expected=$EXPECTED actual=$ACTUAL"
    exit 1
  fi

  while IFS= read -r line; do
    path="$(printf '%s\n' "$line" | jq -r '.path')"
    expected_sha="$(printf '%s\n' "$line" | jq -r '.sha256')"

    test -f "$path"

    actual_sha="$(sha256sum "$path" | awk '{print $1}')"

    if [ "$expected_sha" != "$actual_sha" ]; then
      echo "ALMS_DEEP_VERIFY_FAIL file_hash_mismatch path=$path expected=$expected_sha actual=$actual_sha"
      exit 1
    fi
  done < "$INV"

  echo "ALMS_DAILY_IPFS_JSON_AUDIT_DEEP_VERIFY_OK report=$REPORT inventory=$INV"
else
  echo "ALMS_DAILY_IPFS_JSON_AUDIT_VERIFY_OK report=$REPORT"
fi
