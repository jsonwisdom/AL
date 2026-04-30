#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — BATCH PROOF V1
# PURPOSE: Generate deterministic Merkle inclusion proof for one merged_receipt_v1 leaf
# RULE: No network, no anchoring, no inference, no reordering

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <merged_receipts_jsonl> <leaf_index> [batch_summary_json]" >&2
  exit 2
fi

INPUT_JSONL="$1"
TARGET_INDEX="$2"
BATCH_JSON="${3:-}"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$TIMESTAMP_UTC" '{proof_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
}

[ -f "$INPUT_JSONL" ] || hard_fail "INPUT_FILE_NOT_FOUND"
[ -s "$INPUT_JSONL" ] || hard_fail "INPUT_FILE_EMPTY"

case "$TARGET_INDEX" in
  ''|*[!0-9]*) hard_fail "INVALID_LEAF_INDEX" ;;
esac

TMP_LEAVES="$(mktemp)"
TMP_LEVEL="$(mktemp)"
TMP_NEXT="$(mktemp)"
TMP_SIBLINGS="$(mktemp)"
TMP_POSITIONS="$(mktemp)"
trap 'rm -f "$TMP_LEAVES" "$TMP_LEVEL" "$TMP_NEXT" "$TMP_SIBLINGS" "$TMP_POSITIONS"' EXIT

index=0
TARGET_LEAF_HASH=""
while IFS= read -r line || [ -n "$line" ]; do
  [ -n "$line" ] || hard_fail "EMPTY_LINE"
  printf '%s' "$line" | jq -e . >/dev/null 2>&1 || hard_fail "INVALID_JSON_LINE_$index"
  canonical="$(printf '%s' "$line" | jq -cS .)"
  [ "$line" = "$canonical" ] || hard_fail "NON_CANONICAL_JSON_LINE_$index"
  leaf_hash="$(printf '%s' "$line" | sha256sum | awk '{print $1}')"
  printf '%s\n' "$leaf_hash" >> "$TMP_LEAVES"
  if [ "$index" -eq "$TARGET_INDEX" ]; then
    TARGET_LEAF_HASH="$leaf_hash"
  fi
  index=$((index + 1))
done < "$INPUT_JSONL"

LEAF_COUNT="$index"
[ "$LEAF_COUNT" -gt 0 ] || hard_fail "NO_LEAVES"
[ "$TARGET_INDEX" -lt "$LEAF_COUNT" ] || hard_fail "LEAF_INDEX_OUT_OF_RANGE"
[ -n "$TARGET_LEAF_HASH" ] || hard_fail "TARGET_LEAF_NOT_FOUND"

cp "$TMP_LEAVES" "$TMP_LEVEL"
CURRENT_INDEX="$TARGET_INDEX"

while [ "$(wc -l < "$TMP_LEVEL" | tr -d ' ')" -gt 1 ]; do
  mapfile -t hashes < "$TMP_LEVEL"
  count="${#hashes[@]}"

  if [ $((CURRENT_INDEX % 2)) -eq 0 ]; then
    sibling_index=$((CURRENT_INDEX + 1))
    position="R"
    if [ "$sibling_index" -ge "$count" ]; then
      sibling_index="$CURRENT_INDEX"
    fi
  else
    sibling_index=$((CURRENT_INDEX - 1))
    position="L"
  fi

  printf '%s\n' "${hashes[$sibling_index]}" >> "$TMP_SIBLINGS"
  printf '%s\n' "$position" >> "$TMP_POSITIONS"

  : > "$TMP_NEXT"
  i=0
  while [ "$i" -lt "$count" ]; do
    left="${hashes[$i]}"
    if [ $((i + 1)) -lt "$count" ]; then
      right="${hashes[$((i + 1))]}"
    else
      right="$left"
    fi
    printf '%s%s' "$left" "$right" | sha256sum | awk '{print $1}' >> "$TMP_NEXT"
    i=$((i + 2))
  done

  CURRENT_INDEX=$((CURRENT_INDEX / 2))
  cp "$TMP_NEXT" "$TMP_LEVEL"
done

COMPUTED_ROOT="$(cat "$TMP_LEVEL")"
EXPECTED_ROOT=""
ROOT_MATCH=false

if [ -n "$BATCH_JSON" ]; then
  [ -f "$BATCH_JSON" ] || hard_fail "BATCH_FILE_NOT_FOUND"
  jq -e '.merkle_root and (.leaf_count != null)' "$BATCH_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_BATCH_SUMMARY"
  EXPECTED_ROOT="$(jq -r '.merkle_root' "$BATCH_JSON")"
  EXPECTED_LEAF_COUNT="$(jq -r '.leaf_count' "$BATCH_JSON")"
  [ "$EXPECTED_LEAF_COUNT" = "$LEAF_COUNT" ] || hard_fail "BATCH_LEAF_COUNT_MISMATCH"
  if [ "$EXPECTED_ROOT" = "$COMPUTED_ROOT" ]; then
    ROOT_MATCH=true
  fi
fi

SIBLINGS_JSON="$(jq -R -s -c 'split("\n") | map(select(length > 0))' "$TMP_SIBLINGS")"
POSITIONS_JSON="$(jq -R -s -c 'split("\n") | map(select(length > 0))' "$TMP_POSITIONS")"

jq -n -cS \
  --arg computed_root "$COMPUTED_ROOT" \
  --arg expected_root "$EXPECTED_ROOT" \
  --arg leaf_hash "$TARGET_LEAF_HASH" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --argjson leaf_count "$LEAF_COUNT" \
  --argjson leaf_index "$TARGET_INDEX" \
  --argjson positions "$POSITIONS_JSON" \
  --argjson root_match "$ROOT_MATCH" \
  --argjson sibling_hashes "$SIBLINGS_JSON" \
  '{computed_root:$computed_root,expected_root:$expected_root,leaf_count:$leaf_count,leaf_hash:$leaf_hash,leaf_index:$leaf_index,positions:$positions,proof_status:"OK",root_match:$root_match,sibling_hashes:$sibling_hashes,timestamp_utc:$timestamp_utc}'
