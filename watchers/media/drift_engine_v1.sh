#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — DRIFT ENGINE V1
# PURPOSE: Compare previous and current extractor JSON using byte-surface hashes only
# RULE: No NLP, no heuristics, no semantic inference

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <previous_extractor_json> <current_extractor_json>" >&2
  exit 2
fi

PREV_JSON="$1"
CURR_JSON="$2"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# 0. Preconditions: valid JSON and required keys.
if ! jq -e '.claim_excerpt and .source_url' "$PREV_JSON" >/dev/null 2>&1; then
  jq -n -cS --arg reason "MALFORMED_PREVIOUS_INPUT" --arg ts "$TIMESTAMP_UTC" '{drift_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
fi

if ! jq -e '.claim_excerpt and .source_url' "$CURR_JSON" >/dev/null 2>&1; then
  jq -n -cS --arg reason "MALFORMED_CURRENT_INPUT" --arg ts "$TIMESTAMP_UTC" '{drift_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
fi

PREV_SOURCE_URL="$(jq -r '.source_url' "$PREV_JSON")"
CURR_SOURCE_URL="$(jq -r '.source_url' "$CURR_JSON")"
PREV_RAW="$(jq -r '.claim_excerpt' "$PREV_JSON")"
CURR_RAW="$(jq -r '.claim_excerpt' "$CURR_JSON")"

# 1. Normalize excerpt by deterministic surface transforms only.
normalize_excerpt() {
  printf '%s' "$1" \
    | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//; s/[[:space:]]+/ /g' \
    | cut -c 1-512
}

PREV_NORM="$(normalize_excerpt "$PREV_RAW")"
CURR_NORM="$(normalize_excerpt "$CURR_RAW")"

# 2. Compute stable SHA-256 hashes over exact bytes with no implicit newline.
sha256_no_newline() {
  printf '%s' "$1" | sha256sum | awk '{print $1}'
}

PREV_RAW_HASH="$(sha256_no_newline "$PREV_RAW")"
CURR_RAW_HASH="$(sha256_no_newline "$CURR_RAW")"
PREV_NORM_HASH="$(sha256_no_newline "$PREV_NORM")"
CURR_NORM_HASH="$(sha256_no_newline "$CURR_NORM")"

RAW_CHANGED=false
NORM_CHANGED=false

if [ "$PREV_RAW_HASH" != "$CURR_RAW_HASH" ]; then
  RAW_CHANGED=true
fi

if [ "$PREV_NORM_HASH" != "$CURR_NORM_HASH" ]; then
  NORM_CHANGED=true
fi

if [ "$RAW_CHANGED" = false ] && [ "$NORM_CHANGED" = false ]; then
  DRIFT_STATUS="NO_DRIFT"
elif [ "$RAW_CHANGED" = true ] && [ "$NORM_CHANGED" = false ]; then
  DRIFT_STATUS="RAW_DRIFT"
elif [ "$RAW_CHANGED" = false ] && [ "$NORM_CHANGED" = true ]; then
  DRIFT_STATUS="NORM_DRIFT"
else
  DRIFT_STATUS="BOTH"
fi

# 4. Emit canonical drift receipt.
jq -n -cS \
  --arg drift_status "$DRIFT_STATUS" \
  --arg norm_hash "$CURR_NORM_HASH" \
  --arg prev_norm_hash "$PREV_NORM_HASH" \
  --arg prev_raw_hash "$PREV_RAW_HASH" \
  --arg previous_source_url "$PREV_SOURCE_URL" \
  --arg raw_hash "$CURR_RAW_HASH" \
  --arg source_url "$CURR_SOURCE_URL" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --argjson norm_changed "$NORM_CHANGED" \
  --argjson raw_changed "$RAW_CHANGED" \
  '{drift_status:$drift_status,norm_changed:$norm_changed,norm_hash:$norm_hash,prev_norm_hash:$prev_norm_hash,prev_raw_hash:$prev_raw_hash,previous_source_url:$previous_source_url,raw_changed:$raw_changed,raw_hash:$raw_hash,source_url:$source_url,timestamp_utc:$timestamp_utc}'
