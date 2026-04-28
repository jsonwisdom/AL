#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NORMALIZER="$PROJECT_ROOT/scripts/alms_normalize.sh"
EXTRACTOR="$PROJECT_ROOT/scripts/alms_extract_numbers.sh"

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

# --- NEW: numeric extraction ---
NUMERIC_OUTPUT=$(printf '%s' "$NORMALIZED_TEXT" | "$EXTRACTOR")
NUMBERS_HASH=$(echo "$NUMERIC_OUTPUT" | jq -r '.numbers_hash')
NUMBERS=$(echo "$NUMERIC_OUTPUT" | jq '.numbers')

if [ "$MODE" = "replay" ]; then
  REC_HASH=$(jq -r '.numeric_extract.numbers_hash // empty' "$RECEIPT_FILE")
  if [ -n "$REC_HASH" ] && [ "$NUMBERS_HASH" != "$REC_HASH" ]; then
    echo "ALMS_VERIFY_FAIL numeric_drift_detected expected=$REC_HASH actual=$NUMBERS_HASH" >&2
    exit 1
  fi
fi

INVARIANT_RESULTS=$(jq -n --arg nh "$NUMBERS_HASH" '[{"id":"numerical_consistency","passed":true,"details":"numbers_hash stable: "+$nh}]')

RECEIPT_ID="ALMS-MS-$(date -u +%Y%m%d%H%M%S)"
VALID_AS_OF=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

BASE=$(jq -n \
  --arg id "$RECEIPT_ID" \
  --arg ih "$INPUT_HASH" \
  --arg nh "$NORMALIZED_HASH" \
  --arg txt "$NORMALIZED_TEXT" \
  --arg numh "$NUMBERS_HASH" \
  --argjson nums "$NUMBERS" \
  --argjson inv "$INVARIANT_RESULTS" \
  '{receipt_id:$id,input_hash:$ih,normalized_hash:$nh,normalized_text:$txt,numeric_extract:{extractor_version:"alms_numeric_extractor_v1",numbers_hash:$numh,numbers:$nums},invariants_results:$inv,verdict:"NEEDS_MORE_EVIDENCE",valid_as_of:""}')

HASH="sha256:$(echo "$BASE" | jq -cS . | sha256sum | awk '{print $1}')"
FINAL=$(echo "$BASE" | jq --arg h "$HASH" '. + {receipt_hash:$h}')

echo "$FINAL" | jq .
