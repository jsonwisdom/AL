#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — BUNDLE VERIFIER V1
# PURPOSE: Verify portable_proof_bundle_v1 offline as a self-contained artifact
# RULE: No network, no signing, no mutation, no inference

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <portable_proof_bundle_json>" >&2
  exit 2
fi

BUNDLE_JSON="$1"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$TIMESTAMP_UTC" '{reason:$reason,timestamp_utc:$ts,verify_status:"HARD_FAIL"}'
  exit 1
}

is_hex64() {
  case "$1" in
    [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) return 0 ;;
    *) return 1 ;;
  esac
}

[ -f "$BUNDLE_JSON" ] || hard_fail "BUNDLE_FILE_NOT_FOUND"
[ -s "$BUNDLE_JSON" ] || hard_fail "BUNDLE_FILE_EMPTY"
jq -e . "$BUNDLE_JSON" >/dev/null 2>&1 || hard_fail "BUNDLE_JSON_MALFORMED"

BUNDLE_CANONICAL="$(jq -cS . "$BUNDLE_JSON")"
[ "$(cat "$BUNDLE_JSON")" = "$BUNDLE_CANONICAL" ] || hard_fail "BUNDLE_NOT_CANONICAL"

jq -e '.bundle_version == "portable_proof_bundle_v1" and .bundle_id and .leaf_hash and (.leaf|type=="object") and (.merkle_proof|type=="object") and (.batch_summary|type=="object") and (.anchor_metadata|type=="object")' "$BUNDLE_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_BUNDLE"

BUNDLE_ID="$(jq -r '.bundle_id' "$BUNDLE_JSON")"
BUNDLE_LEAF_HASH="$(jq -r '.leaf_hash' "$BUNDLE_JSON")"
LEAF_CANONICAL="$(jq -cS '.leaf' "$BUNDLE_JSON")"
PROOF_LEAF_HASH="$(jq -r '.merkle_proof.leaf_hash // ""' "$BUNDLE_JSON")"
PROOF_ROOT="$(jq -r '.merkle_proof.computed_root // .merkle_proof.expected_root // ""' "$BUNDLE_JSON")"
BATCH_ROOT="$(jq -r '.batch_summary.merkle_root // ""' "$BUNDLE_JSON")"
BATCH_LEAF_COUNT="$(jq -r '.batch_summary.leaf_count // ""' "$BUNDLE_JSON")"
ANCHOR_ROOT="$(jq -r '.anchor_metadata.merkle_root // .anchor_metadata.offline_result.anchored_merkle_root // .anchor_metadata.offline_result.local_merkle_root // ""' "$BUNDLE_JSON")"

is_hex64 "$BUNDLE_ID" || hard_fail "BUNDLE_ID_HEX_INVALID"
is_hex64 "$BUNDLE_LEAF_HASH" || hard_fail "BUNDLE_LEAF_HASH_INVALID"
is_hex64 "$PROOF_LEAF_HASH" || hard_fail "PROOF_LEAF_HASH_INVALID"
is_hex64 "$PROOF_ROOT" || hard_fail "PROOF_ROOT_INVALID"
is_hex64 "$BATCH_ROOT" || hard_fail "BATCH_ROOT_INVALID"

LEAF_HASH_RECOMPUTED="$(printf '%s' "$LEAF_CANONICAL" | sha256sum | awk '{print $1}')"
[ "$LEAF_HASH_RECOMPUTED" = "$BUNDLE_LEAF_HASH" ] || hard_fail "LEAF_HASH_RECOMPUTE_MISMATCH"
[ "$PROOF_LEAF_HASH" = "$BUNDLE_LEAF_HASH" ] || hard_fail "PROOF_LEAF_HASH_MISMATCH"
[ "$PROOF_ROOT" = "$BATCH_ROOT" ] || hard_fail "PROOF_BATCH_ROOT_MISMATCH"

if [ -n "$ANCHOR_ROOT" ] && [ "$ANCHOR_ROOT" != "null" ]; then
  is_hex64 "$ANCHOR_ROOT" || hard_fail "ANCHOR_ROOT_INVALID"
  [ "$ANCHOR_ROOT" = "$BATCH_ROOT" ] || hard_fail "ANCHOR_BATCH_ROOT_MISMATCH"
fi

SIBLING_COUNT="$(jq '.merkle_proof.sibling_hashes // .merkle_proof.siblings // [] | length' "$BUNDLE_JSON")"
POSITION_COUNT="$(jq '.merkle_proof.positions // [] | length' "$BUNDLE_JSON")"
[ "$SIBLING_COUNT" = "$POSITION_COUNT" ] || hard_fail "PROOF_LENGTH_MISMATCH"

if ! jq -e 'all((.merkle_proof.sibling_hashes // .merkle_proof.siblings // [])[]; test("^[0-9a-f]{64}$"))' "$BUNDLE_JSON" >/dev/null 2>&1; then
  hard_fail "PROOF_SIBLING_HEX_INVALID"
fi

if ! jq -e 'all((.merkle_proof.positions // [])[]; . == "L" or . == "R")' "$BUNDLE_JSON" >/dev/null 2>&1; then
  hard_fail "PROOF_POSITION_INVALID"
fi

CURRENT="$BUNDLE_LEAF_HASH"
index=0
while [ "$index" -lt "$SIBLING_COUNT" ]; do
  SIBLING="$(jq -r --argjson i "$index" '(.merkle_proof.sibling_hashes // .merkle_proof.siblings)[$i]' "$BUNDLE_JSON")"
  POSITION="$(jq -r --argjson i "$index" '.merkle_proof.positions[$i]' "$BUNDLE_JSON")"

  if [ "$POSITION" = "L" ]; then
    CURRENT="$(printf '%s%s' "$SIBLING" "$CURRENT" | sha256sum | awk '{print $1}')"
  else
    CURRENT="$(printf '%s%s' "$CURRENT" "$SIBLING" | sha256sum | awk '{print $1}')"
  fi

  index=$((index + 1))
done

COMPUTED_ROOT="$CURRENT"
[ "$COMPUTED_ROOT" = "$BATCH_ROOT" ] || hard_fail "MERKLE_PROOF_ROOT_MISMATCH"

ROOT_MATCH=true
VERIFY_STATUS="BUNDLE_VALID"

jq -n -cS \
  --arg batch_root "$BATCH_ROOT" \
  --arg bundle_id "$BUNDLE_ID" \
  --arg computed_root "$COMPUTED_ROOT" \
  --arg leaf_hash "$BUNDLE_LEAF_HASH" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --arg verify_status "$VERIFY_STATUS" \
  --argjson leaf_count "$BATCH_LEAF_COUNT" \
  --argjson root_match "$ROOT_MATCH" \
  '{batch_root:$batch_root,bundle_id:$bundle_id,computed_root:$computed_root,leaf_count:$leaf_count,leaf_hash:$leaf_hash,root_match:$root_match,timestamp_utc:$timestamp_utc,verify_status:$verify_status}'
