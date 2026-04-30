#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — PROOF VERIFIER V1
# PURPOSE: Verify one Merkle inclusion proof against an expected root
# RULE: No network, no anchoring, no content interpretation, no leaf recomputation

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <proof_json>" >&2
  exit 2
fi

PROOF_JSON="$1"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

hard_fail() {
  local reason="$1"
  local leaf_hash=""
  local expected_root=""

  if [ -f "$PROOF_JSON" ] && jq -e . "$PROOF_JSON" >/dev/null 2>&1; then
    leaf_hash="$(jq -r '.leaf_hash // ""' "$PROOF_JSON")"
    expected_root="$(jq -r '.expected_root // ""' "$PROOF_JSON")"
  fi

  jq -n -cS \
    --arg expected_root "$expected_root" \
    --arg leaf_hash "$leaf_hash" \
    --arg reason "$reason" \
    --arg timestamp_utc "$TIMESTAMP_UTC" \
    '{expected_root:$expected_root,leaf_hash:$leaf_hash,reason:$reason,timestamp_utc:$timestamp_utc,verify_status:"HARD_FAIL"}'
  exit 1
}

is_hex64() {
  case "$1" in
    [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) return 0 ;;
    *) return 1 ;;
  esac
}

[ -f "$PROOF_JSON" ] || hard_fail "PROOF_FILE_NOT_FOUND"
[ -s "$PROOF_JSON" ] || hard_fail "PROOF_FILE_EMPTY"
jq -e . "$PROOF_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_JSON"

jq -e '.leaf_hash and .expected_root and ((.siblings // .sibling_hashes) | type == "array") and (.positions | type == "array")' "$PROOF_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_INPUT"

LEAF_HASH="$(jq -r '.leaf_hash' "$PROOF_JSON")"
EXPECTED_ROOT="$(jq -r '.expected_root' "$PROOF_JSON")"
SIBLING_COUNT="$(jq '(.siblings // .sibling_hashes) | length' "$PROOF_JSON")"
POSITION_COUNT="$(jq '.positions | length' "$PROOF_JSON")"

is_hex64 "$LEAF_HASH" || hard_fail "LEAF_HASH_HEX_INVALID"
is_hex64 "$EXPECTED_ROOT" || hard_fail "EXPECTED_ROOT_HEX_INVALID"
[ "$SIBLING_COUNT" = "$POSITION_COUNT" ] || hard_fail "LENGTH_MISMATCH"

if ! jq -e 'all((.siblings // .sibling_hashes)[]; test("^[0-9a-f]{64}$"))' "$PROOF_JSON" >/dev/null 2>&1; then
  hard_fail "SIBLING_HEX_INVALID"
fi

if ! jq -e 'all(.positions[]; . == "L" or . == "R")' "$PROOF_JSON" >/dev/null 2>&1; then
  hard_fail "POSITION_INVALID"
fi

CURRENT="$LEAF_HASH"
index=0
while [ "$index" -lt "$SIBLING_COUNT" ]; do
  SIBLING="$(jq -r --argjson i "$index" '(.siblings // .sibling_hashes)[$i]' "$PROOF_JSON")"
  POSITION="$(jq -r --argjson i "$index" '.positions[$i]' "$PROOF_JSON")"

  if [ "$POSITION" = "L" ]; then
    CURRENT="$(printf '%s%s' "$SIBLING" "$CURRENT" | sha256sum | awk '{print $1}')"
  else
    CURRENT="$(printf '%s%s' "$CURRENT" "$SIBLING" | sha256sum | awk '{print $1}')"
  fi

  index=$((index + 1))
done

COMPUTED_ROOT="$CURRENT"
ROOT_MATCH=false
VERIFY_STATUS="PROOF_INVALID"

if [ "$COMPUTED_ROOT" = "$EXPECTED_ROOT" ]; then
  ROOT_MATCH=true
  VERIFY_STATUS="PROOF_VALID"
fi

jq -n -cS \
  --arg computed_root "$COMPUTED_ROOT" \
  --arg expected_root "$EXPECTED_ROOT" \
  --arg leaf_hash "$LEAF_HASH" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --arg verify_status "$VERIFY_STATUS" \
  --argjson root_match "$ROOT_MATCH" \
  '{computed_root:$computed_root,expected_root:$expected_root,leaf_hash:$leaf_hash,root_match:$root_match,timestamp_utc:$timestamp_utc,verify_status:$verify_status}'
