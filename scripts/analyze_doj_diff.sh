#!/usr/bin/env bash
# Detect delta between current and previous DOJ dataset receipt indexes
# Part of jsonwisdom/AL DOJ data_json lane

set -euo pipefail

INDEX_DIR="_truth/doj_data_json/indexes"
REPORT_DIR="_truth/doj_data_json/diff_reports"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
SAFE_TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
REPORT_FILE="$REPORT_DIR/diff_report_${SAFE_TIMESTAMP}.json"

mkdir -p "$REPORT_DIR"

echo "[ANALYSIS] Running DOJ data.json differential analysis"

mapfile -t INDEXES < <(find "$INDEX_DIR" -maxdepth 1 -type f -name 'dataset_index_*.jsonl' 2>/dev/null | sort)

if [[ "${#INDEXES[@]}" -lt 2 ]]; then
  jq -n \
    --arg generated_at "$TIMESTAMP" \
    --arg status "insufficient_history" \
    --arg message "Need at least two dataset indexes to compute a diff" \
    '{
      generated_at: $generated_at,
      status: $status,
      message: $message,
      authority: false,
      verification_state: "DIFF_NOT_INTERPRETED",
      added: [],
      removed: [],
      modified: []
    }' > "$REPORT_FILE"

  echo "[WARN] Insufficient history for diff"
  echo "REPORT_FILE=$REPORT_FILE"
  exit 0
fi

PREVIOUS_INDEX="${INDEXES[$((${#INDEXES[@]} - 2))]}"
CURRENT_INDEX="${INDEXES[$((${#INDEXES[@]} - 1))]}"

jq empty "$PREVIOUS_INDEX"
jq empty "$CURRENT_INDEX"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

PREV_SORTED="$TMP_DIR/previous.sorted.jsonl"
CURR_SORTED="$TMP_DIR/current.sorted.jsonl"
ADDED_FILE="$TMP_DIR/added.json"
REMOVED_FILE="$TMP_DIR/removed.json"
MODIFIED_FILE="$TMP_DIR/modified.json"

jq -s 'sort_by(.raw_identifier)' "$PREVIOUS_INDEX" > "$PREV_SORTED"
jq -s 'sort_by(.raw_identifier)' "$CURRENT_INDEX" > "$CURR_SORTED"

jq --slurpfile previous "$PREV_SORTED" '
  . as $current |
  $previous[0] as $prev |
  [
    $current[] as $c |
    select(($prev | map(.raw_identifier) | index($c.raw_identifier)) | not)
  ]
' "$CURR_SORTED" > "$ADDED_FILE"

jq --slurpfile current "$CURR_SORTED" '
  . as $previous |
  $current[0] as $cur |
  [
    $previous[] as $p |
    select(($cur | map(.raw_identifier) | index($p.raw_identifier)) | not)
  ]
' "$PREV_SORTED" > "$REMOVED_FILE"

jq --slurpfile previous "$PREV_SORTED" '
  . as $current |
  $previous[0] as $prev |
  [
    $current[] as $c |
    ($prev[] | select(.raw_identifier == $c.raw_identifier)) as $p |
    select($p.hash_sha256 != $c.hash_sha256) |
    {
      raw_identifier: $c.raw_identifier,
      previous_hash_sha256: $p.hash_sha256,
      current_hash_sha256: $c.hash_sha256,
      previous_receipt_id: $p.receipt_id,
      current_receipt_id: $c.receipt_id,
      previous_receipt_file: $p.receipt_file,
      current_receipt_file: $c.receipt_file
    }
  ]
' "$CURR_SORTED" > "$MODIFIED_FILE"

ADDED_COUNT="$(jq 'length' "$ADDED_FILE")"
REMOVED_COUNT="$(jq 'length' "$REMOVED_FILE")"
MODIFIED_COUNT="$(jq 'length' "$MODIFIED_FILE")"

if [[ "$ADDED_COUNT" -gt 0 || "$REMOVED_COUNT" -gt 0 || "$MODIFIED_COUNT" -gt 0 ]]; then
  STATUS="delta_detected"
else
  STATUS="no_delta"
fi

jq -n \
  --arg generated_at "$TIMESTAMP" \
  --arg previous_index "$PREVIOUS_INDEX" \
  --arg current_index "$CURRENT_INDEX" \
  --arg status "$STATUS" \
  --argjson added_count "$ADDED_COUNT" \
  --argjson removed_count "$REMOVED_COUNT" \
  --argjson modified_count "$MODIFIED_COUNT" \
  --slurpfile added "$ADDED_FILE" \
  --slurpfile removed "$REMOVED_FILE" \
  --slurpfile modified "$MODIFIED_FILE" \
  '{
    generated_at: $generated_at,
    status: $status,
    previous_index: $previous_index,
    current_index: $current_index,
    added_count: $added_count,
    removed_count: $removed_count,
    modified_count: $modified_count,
    authority: false,
    verification_state: "DIFF_NOT_INTERPRETED",
    added: $added[0],
    removed: $removed[0],
    modified: $modified[0]
  }' > "$REPORT_FILE"

echo "[SUCCESS] Differential analysis complete"
echo "STATUS=$STATUS"
echo "ADDED_COUNT=$ADDED_COUNT"
echo "REMOVED_COUNT=$REMOVED_COUNT"
echo "MODIFIED_COUNT=$MODIFIED_COUNT"
echo "REPORT_FILE=$REPORT_FILE"
