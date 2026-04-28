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
  ((.prev_day_inventory_sha256 == "GENESIS") or (.prev_day_inventory_sha256 | test("^[a-f0-9]{64}$"))) and
  (.chain_rule == "today links to yesterday by prev_day_inventory_sha256; GENESIS is allowed only when no previous daily inventory exists") and
  (.verdict == "ALMS_IPFS_DAILY_JSON_LOCKED" or .verdict == "ALMS_IPFS_DAILY_JSON_WAIT")
' "$REPORT" >/dev/null

if [ "$MODE" = "--deep" ]; then
  DAY="$(jq -r '.date_utc' "$REPORT")"
  PREV_DAY="$(jq -r '.prev_day_utc' "$REPORT")"
  INV="_truth/audit/ipfs_daily/$DAY/inventory.jsonl"
  PREV_INV="_truth/audit/ipfs_daily/$PREV_DAY/inventory.jsonl"

  test -f "$INV"

  EXPECTED="$(jq -r '.inventory_sha256' "$REPORT")"
  ACTUAL="$(sha256sum "$INV" | awk '{print $1}')"

  if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "ALMS_DEEP_VERIFY_FAIL inventory_hash_mismatch expected=$EXPECTED actual=$ACTUAL"
    exit 1
  fi

  EXPECTED_PREV="$(jq -r '.prev_day_inventory_sha256' "$REPORT")"

  if [ "$EXPECTED_PREV" = "GENESIS" ]; then
    if [ -f "$PREV_INV" ]; then
      ACTUAL_PREV="$(sha256sum "$PREV_INV" | awk '{print $1}')"
      echo "ALMS_CHAIN_BREAK genesis_claim_but_previous_inventory_exists prev_day=$PREV_DAY actual_prev=$ACTUAL_PREV"
      exit 1
    fi
  else
    if [ ! -f "$PREV_INV" ]; then
      echo "ALMS_CHAIN_BREAK previous_inventory_missing prev_day=$PREV_DAY expected_prev=$EXPECTED_PREV"
      exit 1
    fi

    ACTUAL_PREV="$(sha256sum "$PREV_INV" | awk '{print $1}')"

    if [ "$EXPECTED_PREV" != "$ACTUAL_PREV" ]; then
      echo "ALMS_CHAIN_BREAK previous_inventory_hash_mismatch prev_day=$PREV_DAY expected=$EXPECTED_PREV actual=$ACTUAL_PREV"
      exit 1
    fi
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

  echo "ALMS_DAILY_IPFS_JSON_AUDIT_DEEP_VERIFY_OK report=$REPORT inventory=$INV chain_prev=$EXPECTED_PREV"
else
  echo "ALMS_DAILY_IPFS_JSON_AUDIT_VERIFY_OK report=$REPORT"
fi
