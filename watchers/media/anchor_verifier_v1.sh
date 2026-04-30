#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — ANCHOR VERIFIER V1
# PURPOSE: Replay local batch and compare against an anchored batch record
# RULE: No signing, no mutation, no heuristics, no hidden network calls

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <merged_receipts_jsonl> <anchored_batch_json>" >&2
  exit 2
fi

MERGED_JSONL="$1"
ANCHORED_JSON="$2"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BATCH_AGGREGATOR="$SCRIPT_DIR/batch_aggregator_v1.sh"

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$TIMESTAMP_UTC" '{reason:$reason,timestamp_utc:$ts,verify_status:"HARD_FAIL"}'
  exit 1
}

[ -f "$MERGED_JSONL" ] || hard_fail "MERGED_JSONL_NOT_FOUND"
[ -s "$MERGED_JSONL" ] || hard_fail "MERGED_JSONL_EMPTY"
[ -f "$ANCHORED_JSON" ] || hard_fail "ANCHORED_JSON_NOT_FOUND"
[ -s "$ANCHORED_JSON" ] || hard_fail "ANCHORED_JSON_EMPTY"
[ -x "$BATCH_AGGREGATOR" ] || hard_fail "BATCH_AGGREGATOR_NOT_EXECUTABLE"

jq -e '.batch_id and .merkle_root and (.leaf_count != null) and .timestamp_utc' "$ANCHORED_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_ANCHORED_JSON"

ANCHORED_CANONICAL="$(jq -cS . "$ANCHORED_JSON")"
ANCHORED_BYTES="$(cat "$ANCHORED_JSON")"
[ "$ANCHORED_BYTES" = "$ANCHORED_CANONICAL" ] || hard_fail "NON_CANONICAL_ANCHORED_JSON"

LOCAL_BATCH="$($BATCH_AGGREGATOR "$MERGED_JSONL")"
LOCAL_CANONICAL="$(printf '%s' "$LOCAL_BATCH" | jq -cS .)"
[ "$LOCAL_BATCH" = "$LOCAL_CANONICAL" ] || hard_fail "NON_CANONICAL_LOCAL_BATCH"

LOCAL_BATCH_ID="$(printf '%s' "$LOCAL_BATCH" | jq -r '.batch_id')"
LOCAL_MERKLE_ROOT="$(printf '%s' "$LOCAL_BATCH" | jq -r '.merkle_root')"
LOCAL_LEAF_COUNT="$(printf '%s' "$LOCAL_BATCH" | jq -r '.leaf_count')"
LOCAL_TIMESTAMP_UTC="$(printf '%s' "$LOCAL_BATCH" | jq -r '.timestamp_utc')"
LOCAL_BATCH_HASH="$(printf '%s' "$LOCAL_CANONICAL" | sha256sum | awk '{print $1}')"

ANCHORED_BATCH_ID="$(jq -r '.batch_id' "$ANCHORED_JSON")"
ANCHORED_MERKLE_ROOT="$(jq -r '.merkle_root' "$ANCHORED_JSON")"
ANCHORED_LEAF_COUNT="$(jq -r '.leaf_count' "$ANCHORED_JSON")"
ANCHORED_TIMESTAMP_UTC="$(jq -r '.timestamp_utc' "$ANCHORED_JSON")"
ANCHORED_BATCH_HASH="$(printf '%s' "$ANCHORED_CANONICAL" | sha256sum | awk '{print $1}')"

MISMATCHES="$(jq -n -c \
  --arg local_batch_hash "$LOCAL_BATCH_HASH" \
  --arg anchored_batch_hash "$ANCHORED_BATCH_HASH" \
  --arg local_batch_id "$LOCAL_BATCH_ID" \
  --arg anchored_batch_id "$ANCHORED_BATCH_ID" \
  --arg local_merkle_root "$LOCAL_MERKLE_ROOT" \
  --arg anchored_merkle_root "$ANCHORED_MERKLE_ROOT" \
  --arg local_leaf_count "$LOCAL_LEAF_COUNT" \
  --arg anchored_leaf_count "$ANCHORED_LEAF_COUNT" \
  --arg local_timestamp_utc "$LOCAL_TIMESTAMP_UTC" \
  --arg anchored_timestamp_utc "$ANCHORED_TIMESTAMP_UTC" \
  '[
    if $local_batch_hash != $anchored_batch_hash then "batch_hash" else empty end,
    if $local_batch_id != $anchored_batch_id then "batch_id" else empty end,
    if $local_merkle_root != $anchored_merkle_root then "merkle_root" else empty end,
    if $local_leaf_count != $anchored_leaf_count then "leaf_count" else empty end,
    if $local_timestamp_utc != $anchored_timestamp_utc then "timestamp_utc" else empty end
  ]')"

MISMATCH_COUNT="$(printf '%s' "$MISMATCHES" | jq 'length')"
VERIFY_STATUS="MATCH"
if [ "$MISMATCH_COUNT" -ne 0 ]; then
  VERIFY_STATUS="MISMATCH"
fi

jq -n -cS \
  --arg anchored_batch_hash "$ANCHORED_BATCH_HASH" \
  --arg anchored_batch_id "$ANCHORED_BATCH_ID" \
  --arg anchored_merkle_root "$ANCHORED_MERKLE_ROOT" \
  --arg anchored_timestamp_utc "$ANCHORED_TIMESTAMP_UTC" \
  --arg local_batch_hash "$LOCAL_BATCH_HASH" \
  --arg local_batch_id "$LOCAL_BATCH_ID" \
  --arg local_merkle_root "$LOCAL_MERKLE_ROOT" \
  --arg local_timestamp_utc "$LOCAL_TIMESTAMP_UTC" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --arg verify_status "$VERIFY_STATUS" \
  --argjson anchored_leaf_count "$ANCHORED_LEAF_COUNT" \
  --argjson local_leaf_count "$LOCAL_LEAF_COUNT" \
  --argjson mismatches "$MISMATCHES" \
  '{anchored_batch_hash:$anchored_batch_hash,anchored_batch_id:$anchored_batch_id,anchored_leaf_count:$anchored_leaf_count,anchored_merkle_root:$anchored_merkle_root,anchored_timestamp_utc:$anchored_timestamp_utc,local_batch_hash:$local_batch_hash,local_batch_id:$local_batch_id,local_leaf_count:$local_leaf_count,local_merkle_root:$local_merkle_root,local_timestamp_utc:$local_timestamp_utc,mismatches:$mismatches,timestamp_utc:$timestamp_utc,verify_status:$verify_status}'
