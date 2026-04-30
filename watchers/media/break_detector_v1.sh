#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — BREAK DETECTOR V1
# PURPOSE: Enforce same witness → same root / different witness → different root
# RULE: No NLP, no heuristics, no semantic inference

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <previous_merged_receipt_json> <current_merged_receipt_json>" >&2
  exit 2
fi

PREV_JSON="$1"
CURR_JSON="$2"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$TIMESTAMP_UTC" '{break_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
}

[ -f "$PREV_JSON" ] || hard_fail "PREVIOUS_FILE_NOT_FOUND"
[ -f "$CURR_JSON" ] || hard_fail "CURRENT_FILE_NOT_FOUND"

jq -e '.resolved_url and .norm_hash and .timestamp_utc' "$PREV_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_PREVIOUS_INPUT"
jq -e '.resolved_url and .norm_hash and .timestamp_utc' "$CURR_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_CURRENT_INPUT"

PREV_RESOLVED_URL="$(jq -r '.resolved_url' "$PREV_JSON")"
CURR_RESOLVED_URL="$(jq -r '.resolved_url' "$CURR_JSON")"

if [ "$PREV_RESOLVED_URL" != "$CURR_RESOLVED_URL" ]; then
  hard_fail "RESOLVED_URL_MISMATCH"
fi

PREV_NORM_HASH="$(jq -r '.norm_hash' "$PREV_JSON")"
CURR_NORM_HASH="$(jq -r '.norm_hash' "$CURR_JSON")"
TIMESTAMP_PREV="$(jq -r '.timestamp_utc' "$PREV_JSON")"
TIMESTAMP_CURR="$(jq -r '.timestamp_utc' "$CURR_JSON")"

sha256_no_newline() {
  printf '%s' "$1" | sha256sum | awk '{print $1}'
}

PREV_ROOT_HASH="$(sha256_no_newline "$PREV_RESOLVED_URL")"
CURR_ROOT_HASH="$(sha256_no_newline "$CURR_RESOLVED_URL")"

SAME_WITNESS=false
SAME_ROOT=false

if [ "$PREV_NORM_HASH" = "$CURR_NORM_HASH" ]; then
  SAME_WITNESS=true
fi

if [ "$PREV_ROOT_HASH" = "$CURR_ROOT_HASH" ]; then
  SAME_ROOT=true
fi

if [ "$SAME_WITNESS" = true ] && [ "$SAME_ROOT" = true ]; then
  BREAK_STATUS="NO_BREAK"
elif [ "$SAME_WITNESS" = false ] && [ "$SAME_ROOT" = false ]; then
  BREAK_STATUS="DRIFT"
else
  BREAK_STATUS="BREAK"
fi

jq -n -cS \
  --arg break_status "$BREAK_STATUS" \
  --arg curr_norm_hash "$CURR_NORM_HASH" \
  --arg curr_root_hash "$CURR_ROOT_HASH" \
  --arg prev_norm_hash "$PREV_NORM_HASH" \
  --arg prev_root_hash "$PREV_ROOT_HASH" \
  --arg resolved_url "$CURR_RESOLVED_URL" \
  --arg timestamp_curr "$TIMESTAMP_CURR" \
  --arg timestamp_prev "$TIMESTAMP_PREV" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --argjson same_root "$SAME_ROOT" \
  --argjson same_witness "$SAME_WITNESS" \
  '{break_status:$break_status,curr_norm_hash:$curr_norm_hash,curr_root_hash:$curr_root_hash,prev_norm_hash:$prev_norm_hash,prev_root_hash:$prev_root_hash,resolved_url:$resolved_url,same_root:$same_root,same_witness:$same_witness,timestamp_curr:$timestamp_curr,timestamp_prev:$timestamp_prev,timestamp_utc:$timestamp_utc}'
