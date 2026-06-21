#!/usr/bin/env bash
# MN_001_FORENSIC_WORKER_V0_1.sh
# Purpose: turn MN_001 normalized drift into sentence-level forensic artifacts.
# Doctrine: NO_FAKE_GREEN. Never promote PUBLIC_CONTENT_CLAIM from this script.

set -euo pipefail

ROOT="${1:-.}"
MN_DIR="$ROOT/projects/mn-fiscal-replay/live_fetch/MN_001"
OUT_DIFF="$MN_DIR/MN_001_sentence_level.diff"
OUT_REVIEW="$MN_DIR/MN_001_sentence_review.json"
OUT_MD="$MN_DIR/MN_001_delta_classification.md"
OUT_RECEIPT="$MN_DIR/MN_001_forensic_receipt.json"
WORK_DIR="$MN_DIR/.mn001_forensic_work"

mkdir -p "$MN_DIR" "$WORK_DIR"

utc_now() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}
json_escape() {
  sed 's/\\/\\\\/g; s/"/\\"/g'
}

write_blocked_receipt() {
  local reason="$1"
  cat > "$OUT_RECEIPT" <<EOF
{
  "artifact": "MN_001_forensic_receipt.json",
  "version": "0.1",
  "generated_utc": "$(utc_now)",
  "status": "BLOCKED",
  "blocked_reason": "$reason",
  "public_content_claim": "BLOCKED",
  "human_review_required": true,
  "no_fake_green": true
}
EOF
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

if [ -z "$BASELINE_FILE" ]; then
  BASELINE_FILE="$(find_one 'baseline.*normalized|normalized.*baseline|baseline')"
fi
if [ -z "$LIVE_FILE" ]; then
  LIVE_FILE="$(find_one 'live.*normalized|normalized.*live|current.*normalized|normalized.*current|current')"
fi
if [ -z "$HUMAN_DIFF_FILE" ]; then
  HUMAN_DIFF_FILE="$(find_one 'human_readable_diff|sectional.*diff|normalized_sectional\.diff')"
fi

# Fallback: derive rough baseline/live streams from an existing +/- diff if source texts are missing.
if { [ -z "$BASELINE_FILE" ] || [ -z "$LIVE_FILE" ]; } && [ -n "$HUMAN_DIFF_FILE" ] && [ -f "$HUMAN_DIFF_FILE" ]; then
  BASELINE_FILE="$WORK_DIR/baseline_from_diff.txt"
  LIVE_FILE="$WORK_DIR/live_from_diff.txt"
  grep '^-' "$HUMAN_DIFF_FILE" | grep -v '^---' | sed 's/^-//' > "$BASELINE_FILE" || true
  grep '^+' "$HUMAN_DIFF_FILE" | grep -v '^+++' | sed 's/^+//' > "$LIVE_FILE" || true
fi

if [ -z "$BASELINE_FILE" ] || [ -z "$LIVE_FILE" ] || [ ! -s "$BASELINE_FILE" ] || [ ! -s "$LIVE_FILE" ]; then
  write_blocked_receipt "FORENSIC_PAYLOAD_MISSING"
  exit 1
fi

BASE_SENT="$WORK_DIR/baseline.sentences.txt"
LIVE_SENT="$WORK_DIR/live.sentences.txt"

sentence_split() {
  tr '\r' '\n' < "$1" \
    | sed -E 's/[[:space:]]+/ /g' \
    | sed -E 's/([.!?])([[:space:]]+)/\1\
/g' \
    | sed 's/^ *//; s/ *$//' \
    | awk 'NF {print}'
}

sentence_split "$BASELINE_FILE" > "$BASE_SENT"
sentence_split "$LIVE_FILE" > "$LIVE_SENT"

diff -u "$BASE_SENT" "$LIVE_SENT" > "$OUT_DIFF" || true

BASE_HASH="$(sha_file "$BASELINE_FILE")"
LIVE_HASH="$(sha_file "$LIVE_FILE")"
DIFF_HASH="$(sha_file "$OUT_DIFF")"
BASE_COUNT="$(wc -l < "$BASE_SENT" | tr -d ' ')"
LIVE_COUNT="$(wc -l < "$LIVE_SENT" | tr -d ' ')"
DIFF_LINES="$(wc -l < "$OUT_DIFF" | tr -d ' ')"

classify_line() {
  local text="$1"

  # Order matters: suppress known extractor/PDF/OCR artifacts before the broad numeric rule.
  if echo "$text" | grep -Eiq '^(page[[:space:]]+)?[0-9]+[[:space:]]+Budget[[:space:]]*&[[:space:]]*Economic[[:space:]]+Forecast|Budget[[:space:]]*&[[:space:]]*Economic[[:space:]]+Forecast[[:space:]]+February[[:space:]]+2026[[:space:]]+[0-9]+|^[0-9]+[[:space:]]+Budget[[:space:]]*&[[:space:]]*Economic[[:space:]]+Forecast'; then
    echo "PAGE_HEADER_SHIFT"
  elif echo "$text" | grep -Eiq '[[:alpha:]]{1,4}[[:space:]]+[[:alpha:]]{1,4}[[:space:]]+[[:alpha:]]{2,}|[[:alpha:]][[:space:]]+-[[:space:]]*[[:alpha:]]|[[:alpha:]][[:space:]]+[[:alpha:]]{1,3}\b|[$][[:space:]]+[0-9]|[0-9][[:space:]]+[0-9][[:space:]]+percent|FY[[:space:]]+20[0-9][0-9][[:space:]]*-[[:space:]]*[0-9]{2}'; then
    echo "WORD_SPLIT_OCR"
  elif echo "$text" | grep -Eiq '[.][0-9]{1,3}[[:space:]]+[A-Z]|[0-9]{4}[.][0-9]{1,3}\b|[[:lower:]][.][0-9]{1,3}[[:space:]]'; then
    echo "FOOTNOTE_JOIN"
  elif echo "$text" | grep -Eiq '(Forecast|Actual|[$][[:space:]]*Change|%[[:space:]]*Change|Annual[[:space:]]+%|FY[[:space:]]*20[0-9]{2}|November[[:space:]]+20[0-9]{2}|February[[:space:]]+20[0-9]{2}).*(Forecast|Actual|[$][[:space:]]*Change|%[[:space:]]*Change|Annual[[:space:]]+%|FY[[:space:]]*20[0-9]{2})'; then
    echo "TABLE_LAYOUT_REFLOW"
  elif echo "$text" | grep -Eiq '\$[0-9]|[0-9][0-9,]*(\.[0-9]+)?[[:space:]]*(million|billion|thousand)|appropriat|obligation|expenditure|revenue|deficit|surplus|fund|agency|program|fiscal year|FY[0-9]|20[0-9][0-9]'; then
    echo "POSSIBLE_CONTENT_DELTA"
  elif echo "$text" | grep -Eiq '^[[:space:][:punct:]]*$|policy template|header|footer|copyright|generated|uuid|sha256|hash|id:'; then
    echo "EXTRACTOR_ARTIFACT"
  else
    echo "NORMALIZATION_ARTIFACT"
  fi
}

TMP_CLASS="$WORK_DIR/classifications.tsv"
: > "$TMP_CLASS"
awk '/^[+-][^+-]/ {print}' "$OUT_DIFF" | while IFS= read -r line; do
  sign="${line:0:1}"
  body="${line:1}"
  class="$(classify_line "$body")"
  printf '%s\t%s\t%s\n' "$sign" "$class" "$body" >> "$TMP_CLASS"
done

count_class() {
  grep -c $'\t'"$1"$'\t' "$TMP_CLASS" || true
}

POSSIBLE_COUNT="$(count_class POSSIBLE_CONTENT_DELTA)"
EXTRACTOR_COUNT="$(count_class EXTRACTOR_ARTIFACT)"
NORMALIZATION_COUNT="$(count_class NORMALIZATION_ARTIFACT)"
PAGE_HEADER_COUNT="$(count_class PAGE_HEADER_SHIFT)"
WORD_SPLIT_COUNT="$(count_class WORD_SPLIT_OCR)"
FOOTNOTE_JOIN_COUNT="$(count_class FOOTNOTE_JOIN)"
TABLE_REFLOW_COUNT="$(count_class TABLE_LAYOUT_REFLOW)"
TOTAL_CLASSIFIED="$(wc -l < "$TMP_CLASS" | tr -d ' ')"

{
  echo "# MN_001 Delta Classification v0.1"
  echo
  echo "Generated UTC: $(utc_now)"
  echo
  echo "## Standing Gate"
  echo
  echo '```text'
  echo "PUBLIC_CONTENT_CLAIM: BLOCKED"
  echo "HUMAN_REVIEW_REQUIRED: TRUE"
  echo "NO_FAKE_GREEN: ACTIVE"
  echo '```'
  echo
  echo "## Taxonomy Order"
  echo
  echo "1. PAGE_HEADER_SHIFT"
  echo "2. WORD_SPLIT_OCR"
  echo "3. FOOTNOTE_JOIN"
  echo "4. TABLE_LAYOUT_REFLOW"
  echo "5. POSSIBLE_CONTENT_DELTA"
  echo "6. EXTRACTOR_ARTIFACT"
  echo "7. NORMALIZATION_ARTIFACT"
  echo
  echo "## Source Files"
  echo
  echo "- Baseline: \`$BASELINE_FILE\`"
  echo "- Live: \`$LIVE_FILE\`"
  echo "- Baseline SHA256: \`$BASE_HASH\`"
  echo "- Live SHA256: \`$LIVE_HASH\`"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Value |"
  echo "|---|---:|"
  echo "| Baseline sentences | $BASE_COUNT |"
  echo "| Live sentences | $LIVE_COUNT |"
  echo "| Diff lines | $DIFF_LINES |"
  echo "| Classified +/- lines | $TOTAL_CLASSIFIED |"
  echo "| Page header shifts | $PAGE_HEADER_COUNT |"
  echo "| Word split / OCR artifacts | $WORD_SPLIT_COUNT |"
  echo "| Footnote joins | $FOOTNOTE_JOIN_COUNT |"
  echo "| Table layout reflows | $TABLE_REFLOW_COUNT |"
  echo "| Possible content deltas | $POSSIBLE_COUNT |"
  echo "| Extractor artifacts | $EXTRACTOR_COUNT |"
  echo "| Normalization artifacts | $NORMALIZATION_COUNT |"
  echo
  echo "## Classified Lines"
  echo
  echo "| Sign | Classification | Text |"
  echo "|---|---|---|"
  awk -F '\t' '{gsub(/\|/, "\\|", $3); if (length($3) > 240) $3=substr($3,1,237) "..."; printf("| `%s` | `%s` | %s |\n", $1, $2, $3)}' "$TMP_CLASS"
} > "$OUT_MD"

MD_HASH="$(sha_file "$OUT_MD")"

cat > "$OUT_REVIEW" <<EOF
{
  "artifact": "MN_001_sentence_review.json",
  "version": "0.1",
  "generated_utc": "$(utc_now)",
  "baseline_file": "$(printf '%s' "$BASELINE_FILE" | json_escape)",
  "live_file": "$(printf '%s' "$LIVE_FILE" | json_escape)",
  "baseline_sha256": "$BASE_HASH",
  "live_sha256": "$LIVE_HASH",
  "baseline_sentence_count": $BASE_COUNT,
  "live_sentence_count": $LIVE_COUNT,
  "diff_line_count": $DIFF_LINES,
  "classified_delta_count": $TOTAL_CLASSIFIED,
  "page_header_shift_count": $PAGE_HEADER_COUNT,
  "word_split_ocr_count": $WORD_SPLIT_COUNT,
  "footnote_join_count": $FOOTNOTE_JOIN_COUNT,
  "table_layout_reflow_count": $TABLE_REFLOW_COUNT,
  "possible_content_delta_count": $POSSIBLE_COUNT,
  "extractor_artifact_count": $EXTRACTOR_COUNT,
  "normalization_artifact_count": $NORMALIZATION_COUNT,
  "public_content_claim": "BLOCKED",
  "human_review_required": true,
  "no_fake_green": true
}
EOF

REVIEW_HASH="$(sha_file "$OUT_REVIEW")"

STATUS="FORENSIC_REVIEW_REQUIRED"
if [ "$POSSIBLE_COUNT" -eq 0 ]; then
  STATUS="NO_POSSIBLE_CONTENT_DELTA_DETECTED_BY_HEURISTIC_BUT_STILL_BLOCKED"
fi

cat > "$OUT_RECEIPT" <<EOF
{
  "artifact": "MN_001_forensic_receipt.json",
  "version": "0.1",
  "generated_utc": "$(utc_now)",
  "status": "$STATUS",
  "public_content_claim": "BLOCKED",
  "human_review_required": true,
  "no_fake_green": true,
  "inputs": {
    "baseline_file": "$(printf '%s' "$BASELINE_FILE" | json_escape)",
    "baseline_sha256": "$BASE_HASH",
    "live_file": "$(printf '%s' "$LIVE_FILE" | json_escape)",
    "live_sha256": "$LIVE_HASH"
  },
  "outputs": {
    "sentence_level_diff": "$OUT_DIFF",
    "sentence_level_diff_sha256": "$DIFF_HASH",
    "sentence_review_json": "$OUT_REVIEW",
    "sentence_review_json_sha256": "$REVIEW_HASH",
    "delta_classification_md": "$OUT_MD",
    "delta_classification_md_sha256": "$MD_HASH"
  },
  "counts": {
    "baseline_sentences": $BASE_COUNT,
    "live_sentences": $LIVE_COUNT,
    "diff_lines": $DIFF_LINES,
    "classified_delta_lines": $TOTAL_CLASSIFIED,
    "page_header_shifts": $PAGE_HEADER_COUNT,
    "word_split_ocr": $WORD_SPLIT_COUNT,
    "footnote_joins": $FOOTNOTE_JOIN_COUNT,
    "table_layout_reflows": $TABLE_REFLOW_COUNT,
    "possible_content_deltas": $POSSIBLE_COUNT,
    "extractor_artifacts": $EXTRACTOR_COUNT,
    "normalization_artifacts": $NORMALIZATION_COUNT
  }
}
EOF

echo "=== MN_001 forensic worker complete ==="
echo "Status: $STATUS"
echo "Public content claim: BLOCKED"
echo "Human review required: TRUE"
echo "Diff: $OUT_DIFF"
echo "Review JSON: $OUT_REVIEW"
echo "Classification MD: $OUT_MD"
echo "Receipt: $OUT_RECEIPT"
