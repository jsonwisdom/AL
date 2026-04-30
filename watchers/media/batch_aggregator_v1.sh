#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — BATCH AGGREGATOR V1
# PURPOSE: Build deterministic Merkle batch root over merged_receipt_v1 JSONL leaves
# RULE: No inference, no filtering, no reordering

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <merged_receipts_jsonl> [leaf_output_jsonl]" >&2
  exit 2
fi

INPUT_JSONL="$1"
LEAF_OUTPUT_JSONL="${2:-}"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$TIMESTAMP_UTC" '{batch_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
}

[ -f "$INPUT_JSONL" ] || hard_fail "INPUT_FILE_NOT_FOUND"
[ -s "$INPUT_JSONL" ] || hard_fail "INPUT_FILE_EMPTY"

TMP_LEAVES="$(mktemp)"
TMP_LEVEL="$(mktemp)"
TMP_NEXT="$(mktemp)"
trap 'rm -f "$TMP_LEAVES" "$TMP_LEVEL" "$TMP_NEXT"' EXIT

index=0
while IFS= read -r line || [ -n "$line" ]; do
  [ -n "$line" ] || hard_fail "EMPTY_LINE"
  printf '%s' "$line" | jq -e . >/dev/null 2>&1 || hard_fail "INVALID_JSON_LINE_$index"

  canonical="$(printf '%s' "$line" | jq -cS .)"
  [ "$line" = "$canonical" ] || hard_fail "NON_CANONICAL_JSON_LINE_$index"

  leaf_hash="$(printf '%s' "$line" | sha256sum | awk '{print $1}')"
  printf '%s\n' "$leaf_hash" >> "$TMP_LEAVES"
  index=$((index + 1))
done < "$INPUT_JSONL"

LEAF_COUNT="$index"
[ "$LEAF_COUNT" -gt 0 ] || hard_fail "NO_LEAVES"

cp "$TMP_LEAVES" "$TMP_LEVEL"

while [ "$(wc -l < "$TMP_LEVEL" | tr -d ' ')" -gt 1 ]; do
  : > "$TMP_NEXT"
  mapfile -t hashes < "$TMP_LEVEL"
  count="${#hashes[@]}"
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
  cp "$TMP_NEXT" "$TMP_LEVEL"
done

MERKLE_ROOT="$(cat "$TMP_LEVEL")"
BATCH_ID="$(printf '%s:%s:%s' "$MERKLE_ROOT" "$LEAF_COUNT" "$TIMESTAMP_UTC" | sha256sum | awk '{print $1}')"

if [ -n "$LEAF_OUTPUT_JSONL" ]; then
  : > "$LEAF_OUTPUT_JSONL"
  leaf_index=0
  while IFS= read -r leaf_hash || [ -n "$leaf_hash" ]; do
    jq -n -cS \
      --arg batch_id "$BATCH_ID" \
      --arg leaf_hash "$leaf_hash" \
      --argjson leaf_index "$leaf_index" \
      '{batch_id:$batch_id,leaf_hash:$leaf_hash,leaf_index:$leaf_index}' >> "$LEAF_OUTPUT_JSONL"
    leaf_index=$((leaf_index + 1))
  done < "$TMP_LEAVES"
fi

jq -n -cS \
  --arg batch_id "$BATCH_ID" \
  --arg merkle_root "$MERKLE_ROOT" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --argjson leaf_count "$LEAF_COUNT" \
  '{batch_id:$batch_id,leaf_count:$leaf_count,merkle_root:$merkle_root,timestamp_utc:$timestamp_utc}'
