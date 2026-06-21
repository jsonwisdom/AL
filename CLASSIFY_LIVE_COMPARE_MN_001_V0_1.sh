#!/bin/bash
# CLASSIFY_LIVE_COMPARE_MN_001_V0_1.sh
# Safe verdict from live compare receipt. NO_FAKE_GREEN, no overclaims.

set -e

COMPARE_RECEIPT="projects/mn-fiscal-replay/live_fetch/MN_001/MN_001.live_compare.json"
VERDICT_FILE="projects/mn-fiscal-replay/live_fetch/MN_001/MN_001.verdict.json"

if [ ! -f "$COMPARE_RECEIPT" ]; then
  echo "BLOCKED_REASON: No live compare receipt found"
  exit 1
fi

echo "=== CLASSIFY_LIVE_COMPARE_MN_001_V0_1 ==="

RESULT=$(jq -r '.result' "$COMPARE_RECEIPT")

if [ "$RESULT" = "NO_ANOMALY" ]; then
  VERDICT="NO_CHANGE_DETECTED"
  NOTE="Live fetch matches sealed enriched baseline."
  RAW_DIFF="false"
  TEXT_DIFF="false"
  META_DIFF="false"
else
  VERDICT="PUBLIC_CONTENT_ANOMALY_UNPROVEN"
  NOTE="Hash differences detected, but safest classification is RAW_PDF_BASELINE_UPGRADED + HTTP_METADATA_DRIFT + TEXT_EXTRACTOR_OR_NORMALIZATION_DRIFT. No public content-change claim is made."

  RAW_DIFF=$(printf '%s\n' "$RESULT" | grep -q 'raw_pdf_sha256' && echo "true" || echo "false")
  TEXT_DIFF=$(printf '%s\n' "$RESULT" | grep -q 'normalized_pdf_text_sha256' && echo "true" || echo "false")
  META_DIFF=$(printf '%s\n' "$RESULT" | grep -q 'http_metadata_sha256' && echo "true" || echo "false")
fi

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

jq -n \
  --arg verdict "$VERDICT" \
  --arg note "$NOTE" \
  --arg timestamp "$TS" \
  --arg receipt "$COMPARE_RECEIPT" \
  --arg raw_diff "$RAW_DIFF" \
  --arg text_diff "$TEXT_DIFF" \
  --arg meta_diff "$META_DIFF" \
  '{
    id: "MN_001",
    verdict: $verdict,
    note: $note,
    timestamp: $timestamp,
    source_receipt: $receipt,
    raw_pdf_diff_detected: $raw_diff,
    text_hash_diff_detected: $text_diff,
    http_metadata_diff_detected: $meta_diff,
    classification: "SAFE_VERDICT"
  }' > "$VERDICT_FILE"

cat "$VERDICT_FILE" | jq .

echo ""
echo "=== Safe verdict complete ==="
echo "Verdict file: $VERDICT_FILE"
echo "No overclaims. PUBLIC_CONTENT_ANOMALY_UNPROVEN until proven."
