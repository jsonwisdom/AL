#!/usr/bin/env bash
# MN_001_FORENSIC_WORKER_V0_1.sh
# Purpose: turn normalized drift into sentence-level forensic artifacts.
# Doctrine: NO_FAKE_GREEN. Never promote PUBLIC_CONTENT_CLAIM from this script.
# Boss Bre compatible: set JURISDICTION=MN027_HENNEPIN to reuse the same worker.

set -euo pipefail

ROOT="${1:-.}"
if git -C "$ROOT" rev-parse --show-toplevel >/dev/null 2>&1; then
  ROOT="$(git -C "$ROOT" rev-parse --show-toplevel)"
fi

JURISDICTION="${JURISDICTION:-MN_001}"
MN_DIR="$ROOT/projects/mn-fiscal-replay/live_fetch/$JURISDICTION"
OUT_DIFF="$MN_DIR/MN_001_sentence_level.diff"
OUT_REVIEW="$MN_DIR/MN_001_sentence_review.json"
OUT_MD="$MN_DIR/MN_001_delta_classification.md"
OUT_RECEIPT="$MN_DIR/MN_001_forensic_receipt.json"
WORK_DIR="$MN_DIR/.mn001_forensic_work"

mkdir -p "$MN_DIR" "$WORK_DIR"

utc_now() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
sha_file() { if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi; }

write_blocked_receipt() {
  local reason="$1"
  cat > "$OUT_DIFF" <<EOF
BLOCKED_REASON: $reason
EOF
  cat > "$OUT_MD" <<EOF
# $JURISDICTION Delta Classification

STATUS: BLOCKED
BLOCKED_REASON: $reason
PUBLIC_CONTENT_CLAIM: BLOCKED
HUMAN_REVIEW_REQUIRED: TRUE
NO_FAKE_GREEN: ACTIVE
EOF
  jq -n \
    --arg artifact "MN_001_sentence_review.json" \
    --arg jurisdiction "$JURISDICTION" \
    --arg utc "$(utc_now)" \
    --arg reason "$reason" \
    '{artifact:$artifact,jurisdiction:$jurisdiction,generated_utc:$utc,status:"BLOCKED",blocked_reason:$reason,public_content_claim:"BLOCKED",human_review_required:true,no_fake_green:true,items:[]}' \
    > "$OUT_REVIEW"
  jq -n \
    --arg artifact "MN_001_forensic_receipt.json" \
    --arg jurisdiction "$JURISDICTION" \
    --arg utc "$(utc_now)" \
    --arg reason "$reason" \
    --arg diff "$OUT_DIFF" \
    --arg review "$OUT_REVIEW" \
    --arg md "$OUT_MD" \
    --arg receipt "$OUT_RECEIPT" \
    '{artifact:$artifact,version:"0.1",jurisdiction:$jurisdiction,generated_utc:$utc,status:"FORENSIC_PAYLOAD_MISSING",blocked_reason:$reason,public_content_claim:"BLOCKED",human_review_required:true,no_fake_green:true,outputs:{sentence_level_diff:$diff,sentence_review_json:$review,delta_classification_md:$md,forensic_receipt_json:$receipt}}' \
    > "$OUT_RECEIPT"
  echo "BLOCKED_REASON: $reason"
  echo "Receipt: $OUT_RECEIPT"
}

find_one() {
  find "$MN_DIR" -maxdepth 4 -type f \
    \( -name "*.txt" -o -name "*.md" -o -name "*.diff" -o -name "*.json" \) \
    | grep -Ei "$1" \
    | grep -Ev 'sentence_level|sentence_review|delta_classification|forensic_receipt|\.mn001_forensic_work' \
    | head -n 1 || true
}

BASELINE_FILE="${BASELINE_FILE:-}"
LIVE_FILE="${LIVE_FILE:-}"
HUMAN_DIFF_FILE="${HUMAN_DIFF_FILE:-}"

[ -n "$BASELINE_FILE" ] || BASELINE_FILE="$(find_one 'baseline.*normalized|normalized.*baseline|baseline')"
[ -n "$LIVE_FILE" ] || LIVE_FILE="$(find_one 'live.*normalized|normalized.*live|current.*normalized|normalized.*current|current')"
[ -n "$HUMAN_DIFF_FILE" ] || HUMAN_DIFF_FILE="$(find_one 'human_readable_diff|sectional.*diff|normalized_sectional\.diff')"

# Fallback: derive rough baseline/live streams from an existing +/- diff if source texts are missing.
if { [ -z "$BASELINE_FILE" ] || [ -z "$LIVE_FILE" ]; } && [ -n "$HUMAN_DIFF_FILE" ] && [ -f "$HUMAN_DIFF_FILE" ]; then
  BASELINE_FILE="$WORK_DIR/baseline_from_diff.txt"
  LIVE_FILE="$WORK_DIR/live_from_diff.txt"
  grep '^-' "$HUMAN_DIFF_FILE" | grep -v '^---' | sed 's/^-//' > "$BASELINE_FILE" || true
  grep '^+' "$HUMAN_DIFF_FILE" | grep -v '^+++' | sed 's/^+//' > "$LIVE_FILE" || true
fi

if [ -z "$BASELINE_FILE" ] || [ -z "$LIVE_FILE" ] || [ ! -s "$BASELINE_FILE" ] || [ ! -s "$LIVE_FILE" ]; then
  write_blocked_receipt "FORENSIC_PAYLOAD_MISSING"
  exit 0
fi

BASE_SENT="$WORK_DIR/baseline.sentences.txt"
LIVE_SENT="$WORK_DIR/live.sentences.txt"
RAW_DIFF="$WORK_DIR/raw_sentence.diff"
CLASS_TSV="$WORK_DIR/classification.tsv"

sentence_split() {
  # Bootstrap-safe sentence splitter: normalize whitespace, then place sentence endings on separate lines.
  tr '\r' '\n' < "$1" \
    | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//' \
    | sed 's/\. /\.\
/g; s/! /!\
/g; s/? /?\
/g' \
    | sed '/^$/d'
}

sentence_split "$BASELINE_FILE" > "$BASE_SENT"
sentence_split "$LIVE_FILE" > "$LIVE_SENT"

diff -u "$BASE_SENT" "$LIVE_SENT" > "$RAW_DIFF" || true
cp "$RAW_DIFF" "$OUT_DIFF"

classify_line() {
  local text="$1"
  if echo "$text" | grep -Eq '^(Budget & Economic Forecast February 2026 [0-9]+|[0-9]+ Budget & Economic Forecast February 2026)'; then
    echo "PAGE_HEADER_SHIFT"
  elif echo "$text" | grep -Eq '([A-Za-z]{1,3} -[A-Za-z]{2,}|[A-Za-z]{1,3} [A-Za-z]{2,}|\$ [0-9]|[0-9]{4} -[0-9]{2})'; then
    echo "WORD_SPLIT_OCR"
  elif echo "$text" | grep -Eq '[0-9]{4}\.[0-9]{1,3}|[a-zA-Z]\.[0-9]{1,3}|base\.[0-9]{1,3}'; then
    echo "FOOTNOTE_JOIN"
  elif echo "$text" | grep -Eiq '(Forecast|\$ Change|% Change|\(\$ in millions\)|Actual FY|Forecast FY|Annual % Change)' && echo "$text" | grep -Eq '[0-9,$%() -]{20,}'; then
    echo "TABLE_LAYOUT_REFLOW"
  elif echo "$text" | grep -Eq '\$[ ]?[0-9,]+|[0-9]+\.[0-9]+ percent|\bFY 202[0-9]|\bbillion\b|\bmillion\b|\bGDP\b|\bCPI\b'; then
    echo "POSSIBLE_CONTENT_DELTA"
  elif echo "$text" | grep -Eiq '(graph:|chart:|Source:|accessed|https?://|Homebuilding Activity|Wage and Salary Income)'; then
    echo "EXTRACTOR_ARTIFACT"
  else
    echo "NORMALIZATION_ARTIFACT"
  fi
}

: > "$CLASS_TSV"
while IFS= read -r line; do
  case "$line" in
    ---*|+++*|@@*) continue ;;
    -*) sign="-"; text="${line#-}" ;;
    +*) sign="+"; text="${line#+}" ;;
    *) continue ;;
  esac
  label="$(classify_line "$text")"
  printf '%s\t%s\t%s\n' "$label" "$sign" "$text" >> "$CLASS_TSV"
done < "$RAW_DIFF"

count_label() { grep -c "^$1" "$CLASS_TSV" 2>/dev/null || true; }
BASE_COUNT="$(wc -l < "$BASE_SENT" | tr -d ' ')"
LIVE_COUNT="$(wc -l < "$LIVE_SENT" | tr -d ' ')"
DIFF_COUNT="$(wc -l < "$RAW_DIFF" | tr -d ' ')"
CLASS_COUNT="$(wc -l < "$CLASS_TSV" | tr -d ' ')"
PAGE_COUNT="$(count_label PAGE_HEADER_SHIFT)"
WORD_COUNT="$(count_label WORD_SPLIT_OCR)"
FOOTNOTE_COUNT="$(count_label FOOTNOTE_JOIN)"
TABLE_COUNT="$(count_label TABLE_LAYOUT_REFLOW)"
POSSIBLE_COUNT="$(count_label POSSIBLE_CONTENT_DELTA)"
EXTRACTOR_COUNT="$(count_label EXTRACTOR_ARTIFACT)"
NORMALIZATION_COUNT="$(count_label NORMALIZATION_ARTIFACT)"

if cmp -s "$BASE_SENT" "$LIVE_SENT"; then
  STATUS="NO_DIFF_DETECTED"
else
  STATUS="FORENSIC_REVIEW_REQUIRED"
fi

cat > "$OUT_MD" <<EOF
# $JURISDICTION Delta Classification

Generated UTC: $(utc_now)

## Gate

- PUBLIC_CONTENT_CLAIM: BLOCKED
- HUMAN_REVIEW_REQUIRED: TRUE
- NO_FAKE_GREEN: ACTIVE
- STATUS: $STATUS
- CONFIRMED_CONTENT_DELTA: NONE_BY_WORKER

## Counts

| Label | Count |
|---|---:|
| PAGE_HEADER_SHIFT | $PAGE_COUNT |
| WORD_SPLIT_OCR | $WORD_COUNT |
| FOOTNOTE_JOIN | $FOOTNOTE_COUNT |
| TABLE_LAYOUT_REFLOW | $TABLE_COUNT |
| POSSIBLE_CONTENT_DELTA | $POSSIBLE_COUNT |
| EXTRACTOR_ARTIFACT | $EXTRACTOR_COUNT |
| NORMALIZATION_ARTIFACT | $NORMALIZATION_COUNT |

## Classified Lines

| Label | Side | Text |
|---|---:|---|
EOF

awk -F '\t' 'BEGIN{max=500} NR<=max {gsub(/\|/, "\\|", $3); print "| " $1 " | `" $2 "` | " $3 " |"}' "$CLASS_TSV" >> "$OUT_MD"

jq -Rn \
  --arg jurisdiction "$JURISDICTION" \
  --arg utc "$(utc_now)" \
  --arg status "$STATUS" \
  --argjson max 500 \
  'def parse: split("\t") | {label:.[0],side:.[1],text:.[2]}; [inputs | parse] | .[0:$max] | {artifact:"MN_001_sentence_review.json",jurisdiction:$jurisdiction,generated_utc:$utc,status:$status,public_content_claim:"BLOCKED",human_review_required:true,no_fake_green:true,confirmed_content_delta:"NONE_BY_WORKER",items:.}' \
  < "$CLASS_TSV" > "$OUT_REVIEW"

jq -n \
  --arg jurisdiction "$JURISDICTION" \
  --arg utc "$(utc_now)" \
  --arg status "$STATUS" \
  --arg baseline_file "$BASELINE_FILE" \
  --arg baseline_sha "$(sha_file "$BASELINE_FILE")" \
  --arg live_file "$LIVE_FILE" \
  --arg live_sha "$(sha_file "$LIVE_FILE")" \
  --arg human_diff_file "$HUMAN_DIFF_FILE" \
  --arg human_diff_sha "$(sha_file "$HUMAN_DIFF_FILE")" \
  --arg diff "$OUT_DIFF" \
  --arg review "$OUT_REVIEW" \
  --arg md "$OUT_MD" \
  --arg receipt "$OUT_RECEIPT" \
  --argjson base_count "$BASE_COUNT" \
  --argjson live_count "$LIVE_COUNT" \
  --argjson diff_count "$DIFF_COUNT" \
  --argjson class_count "$CLASS_COUNT" \
  --argjson page_count "$PAGE_COUNT" \
  --argjson word_count "$WORD_COUNT" \
  --argjson footnote_count "$FOOTNOTE_COUNT" \
  --argjson table_count "$TABLE_COUNT" \
  --argjson possible_count "$POSSIBLE_COUNT" \
  --argjson extractor_count "$EXTRACTOR_COUNT" \
  --argjson normalization_count "$NORMALIZATION_COUNT" \
  '{artifact:"MN_001_forensic_receipt.json",version:"0.1",jurisdiction:$jurisdiction,generated_utc:$utc,status:$status,public_content_claim:"BLOCKED",human_review_required:true,no_fake_green:true,confirmed_content_delta:"NONE_BY_WORKER",inputs:{baseline_file:$baseline_file,baseline_sha256:$baseline_sha,live_file:$live_file,live_sha256:$live_sha,human_diff_file:$human_diff_file,human_diff_sha256:$human_diff_sha},counts:{baseline_sentences:$base_count,live_sentences:$live_count,diff_lines:$diff_count,classified_delta_lines:$class_count,page_header_shift:$page_count,word_split_ocr:$word_count,footnote_join:$footnote_count,table_layout_reflow:$table_count,possible_content_deltas:$possible_count,extractor_artifacts:$extractor_count,normalization_artifacts:$normalization_count},outputs:{sentence_level_diff:$diff,sentence_review_json:$review,delta_classification_md:$md,forensic_receipt_json:$receipt}}' \
  > "$OUT_RECEIPT"

echo "=== MN_001 forensic worker complete ==="
echo "Jurisdiction: $JURISDICTION"
echo "Status: $STATUS"
echo "Public content claim: BLOCKED"
echo "Human review required: TRUE"
echo "Diff: $OUT_DIFF"
echo "Review JSON: $OUT_REVIEW"
echo "Classification MD: $OUT_MD"
echo "Receipt: $OUT_RECEIPT"
