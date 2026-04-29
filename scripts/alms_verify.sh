#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NORMALIZER="$PROJECT_ROOT/scripts/alms_normalize.sh"
EXTRACTOR="$PROJECT_ROOT/scripts/alms_extract_numbers.sh"
SOURCE_MATCHER="$PROJECT_ROOT/scripts/alms_source_match.sh"
FETCHER="$PROJECT_ROOT/scripts/alms_fetch_source.sh"

MODE="raw"
RECEIPT_FILE=""

if [ "$#" -eq 0 ]; then
  ORIGINAL_CLAIM=$(cat)
else
  MODE="replay"
  RECEIPT_FILE="$1"
  ORIGINAL_CLAIM=$(jq -r '.original_claim' "$RECEIPT_FILE")
fi

NORMALIZE_OUTPUT=$(printf '%s' "$ORIGINAL_CLAIM" | "$NORMALIZER")
INPUT_HASH=$(echo "$NORMALIZE_OUTPUT" | jq -r '.input_hash')
NORMALIZED_HASH=$(echo "$NORMALIZE_OUTPUT" | jq -r '.normalized_hash')
NORMALIZED_TEXT=$(echo "$NORMALIZE_OUTPUT" | jq -r '.normalized_text')

NUMERIC_OUTPUT=$(printf '%s' "$NORMALIZED_TEXT" | "$EXTRACTOR")
NUMBERS_HASH=$(echo "$NUMERIC_OUTPUT" | jq -r '.numbers_hash')
NUMBERS=$(echo "$NUMERIC_OUTPUT" | jq '.numbers')

# --- numeric drift ---
if [ "$MODE" = "replay" ]; then
  REC_HASH=$(jq -r '.numeric_extract.numbers_hash // empty' "$RECEIPT_FILE")
  if [ -n "$REC_HASH" ] && [ "$NUMBERS_HASH" != "$REC_HASH" ]; then
    echo "ALMS_VERIFY_FAIL numeric_drift_detected" >&2
    exit 1
  fi
fi

# --- anchor presence ---
MISSING=$(echo "$NUMBERS" | jq '[.[] | select(.source_anchor == null)] | length')
if [ "$MISSING" -gt 0 ]; then
  echo "ALMS_VERIFY_FAIL numeric_anchor_missing" >&2
  exit 1
fi

SOURCE_DOCS="[]"

# --- external grounding ---
if [ -n "${ALMS_SOURCE_URL:-}" ]; then
  TMP_DIR=$(mktemp -d)
  FETCH_OUTPUT=$("$FETCHER" "$ALMS_SOURCE_URL" "$TMP_DIR") || exit 1

  TEXT_PATH=$(echo "$FETCH_OUTPUT" | jq -r '.text_path')
  RAW_HASH=$(echo "$FETCH_OUTPUT" | jq -r '.raw_hash')

  # integrity check stub: always passes unless fetch failed
  SOURCE_DOCS=$(echo "$FETCH_OUTPUT" | jq '[.]')

  # run source match on extracted text
  TMP_CLAIM=$(mktemp)
  printf '%s' "$NORMALIZED_TEXT" > "$TMP_CLAIM"

  MATCH_OUTPUT=$("$SOURCE_MATCHER" "$TMP_CLAIM" "$TEXT_PATH")
  PASSED=$(echo "$MATCH_OUTPUT" | jq -r '.passed')

  if [ "$PASSED" != "true" ]; then
    FAILED_INDEXES=$(echo "$MATCH_OUTPUT" | jq '[.results[] | select(.matched==false) | .index]')
    echo "ALMS_VERIFY_FAIL source_match_failed indexes=$FAILED_INDEXES" >&2
    exit 1
  fi
fi

INVARIANT_RESULTS=$(jq -n \
  --arg nh "$NUMBERS_HASH" \
  '[
    {"id":"numerical_consistency","passed":true,"details":"numbers_hash stable"},
    {"id":"source_presence","passed":true,"details":"all numbers anchored"}
  ]'
)

RECEIPT_ID="ALMS-MS-$(date -u +%Y%m%d%H%M%S)"
VALID_AS_OF=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

BASE=$(jq -n \
  --arg id "$RECEIPT_ID" \
  --arg ih "$INPUT_HASH" \
  --arg nh "$NORMALIZED_HASH" \
  --arg txt "$NORMALIZED_TEXT" \
  --arg numh "$NUMBERS_HASH" \
  --argjson nums "$NUMBERS" \
  --argjson src "$SOURCE_DOCS" \
  '{receipt_id:$id,input_hash:$ih,normalized_hash:$nh,normalized_text:$txt,numeric_extract:{extractor_version:"alms_numeric_extractor_v1",numbers_hash:$numh,numbers:$nums},source_documents:$src,verdict:"NEEDS_MORE_EVIDENCE",valid_as_of:""}')

HASH="sha256:$(echo "$BASE" | jq -cS . | sha256sum | awk '{print $1}')"
FINAL=$(echo "$BASE" | jq --arg h "$HASH" '. + {receipt_hash:$h}')

echo "$FINAL" | jq .
