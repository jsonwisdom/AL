#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — PORTABLE PROOF BUNDLE V1
# PURPOSE: Package one leaf + Merkle proof + batch summary + optional anchor metadata into one portable JSON artifact
# RULE: No network, no signing, no recomputation beyond integrity checks, no inference

if [ "$#" -lt 4 ]; then
  echo "usage: $0 <leaf_json> <proof_json> <batch_summary_json> <anchor_metadata_json>" >&2
  exit 2
fi

LEAF_JSON="$1"
PROOF_JSON="$2"
BATCH_JSON="$3"
ANCHOR_JSON="$4"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$TIMESTAMP_UTC" '{bundle_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
}

[ -f "$LEAF_JSON" ] || hard_fail "LEAF_FILE_NOT_FOUND"
[ -s "$LEAF_JSON" ] || hard_fail "LEAF_FILE_EMPTY"
[ -f "$PROOF_JSON" ] || hard_fail "PROOF_FILE_NOT_FOUND"
[ -s "$PROOF_JSON" ] || hard_fail "PROOF_FILE_EMPTY"
[ -f "$BATCH_JSON" ] || hard_fail "BATCH_FILE_NOT_FOUND"
[ -s "$BATCH_JSON" ] || hard_fail "BATCH_FILE_EMPTY"
[ -f "$ANCHOR_JSON" ] || hard_fail "ANCHOR_FILE_NOT_FOUND"
[ -s "$ANCHOR_JSON" ] || hard_fail "ANCHOR_FILE_EMPTY"

jq -e . "$LEAF_JSON" >/dev/null 2>&1 || hard_fail "LEAF_JSON_MALFORMED"
jq -e . "$PROOF_JSON" >/dev/null 2>&1 || hard_fail "PROOF_JSON_MALFORMED"
jq -e . "$BATCH_JSON" >/dev/null 2>&1 || hard_fail "BATCH_JSON_MALFORMED"
jq -e . "$ANCHOR_JSON" >/dev/null 2>&1 || hard_fail "ANCHOR_JSON_MALFORMED"

LEAF_CANONICAL="$(jq -cS . "$LEAF_JSON")"
PROOF_CANONICAL="$(jq -cS . "$PROOF_JSON")"
BATCH_CANONICAL="$(jq -cS . "$BATCH_JSON")"
ANCHOR_CANONICAL="$(jq -cS . "$ANCHOR_JSON")"

[ "$(cat "$LEAF_JSON")" = "$LEAF_CANONICAL" ] || hard_fail "LEAF_NOT_CANONICAL"
[ "$(cat "$PROOF_JSON")" = "$PROOF_CANONICAL" ] || hard_fail "PROOF_NOT_CANONICAL"
[ "$(cat "$BATCH_JSON")" = "$BATCH_CANONICAL" ] || hard_fail "BATCH_NOT_CANONICAL"
[ "$(cat "$ANCHOR_JSON")" = "$ANCHOR_CANONICAL" ] || hard_fail "ANCHOR_NOT_CANONICAL"

LEAF_HASH="$(printf '%s' "$LEAF_CANONICAL" | sha256sum | awk '{print $1}')"
PROOF_LEAF_HASH="$(jq -r '.leaf_hash // ""' "$PROOF_JSON")"
BATCH_ROOT="$(jq -r '.merkle_root // ""' "$BATCH_JSON")"
PROOF_ROOT="$(jq -r '.computed_root // .expected_root // ""' "$PROOF_JSON")"
ANCHOR_ROOT="$(jq -r '.merkle_root // .offline_result.anchored_merkle_root // .offline_result.local_merkle_root // ""' "$ANCHOR_JSON")"

[ -n "$PROOF_LEAF_HASH" ] || hard_fail "PROOF_LEAF_HASH_MISSING"
[ "$LEAF_HASH" = "$PROOF_LEAF_HASH" ] || hard_fail "LEAF_HASH_PROOF_MISMATCH"
[ -n "$BATCH_ROOT" ] || hard_fail "BATCH_ROOT_MISSING"
[ -n "$PROOF_ROOT" ] || hard_fail "PROOF_ROOT_MISSING"
[ "$BATCH_ROOT" = "$PROOF_ROOT" ] || hard_fail "PROOF_BATCH_ROOT_MISMATCH"

if [ -n "$ANCHOR_ROOT" ] && [ "$ANCHOR_ROOT" != "null" ]; then
  [ "$BATCH_ROOT" = "$ANCHOR_ROOT" ] || hard_fail "ANCHOR_BATCH_ROOT_MISMATCH"
fi

BUNDLE_ID="$(printf '%s:%s:%s' "$LEAF_HASH" "$BATCH_ROOT" "$TIMESTAMP_UTC" | sha256sum | awk '{print $1}')"

jq -n -cS \
  --arg bundle_id "$BUNDLE_ID" \
  --arg bundle_version "portable_proof_bundle_v1" \
  --arg generated_at_utc "$TIMESTAMP_UTC" \
  --arg leaf_hash "$LEAF_HASH" \
  --argjson anchor_metadata "$ANCHOR_CANONICAL" \
  --argjson batch_summary "$BATCH_CANONICAL" \
  --argjson leaf "$LEAF_CANONICAL" \
  --argjson merkle_proof "$PROOF_CANONICAL" \
  '{anchor_metadata:$anchor_metadata,batch_summary:$batch_summary,bundle_id:$bundle_id,bundle_status:"OK",bundle_version:$bundle_version,generated_at_utc:$generated_at_utc,leaf:$leaf,leaf_hash:$leaf_hash,merkle_proof:$merkle_proof}'
