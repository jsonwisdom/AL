#!/usr/bin/env bash
set -euo pipefail

RECEIPT_FILE="${1:-}"

fail() {
  echo "ALMS_RECEIPT_INVALID: $1"
  exit 1
}

[ -n "$RECEIPT_FILE" ] || fail "missing_argument"
[ -f "$RECEIPT_FILE" ] || fail "file_not_found"

jq empty "$RECEIPT_FILE" 2>/dev/null || fail "invalid_json"

EXPECTED_HASH="$(jq -r '.receipt_hash // .output.receipt_hash // empty' "$RECEIPT_FILE")"
[ -n "$EXPECTED_HASH" ] || fail "missing_receipt_hash"

printf '%s' "$EXPECTED_HASH" | grep -Eq '^0x[0-9a-fA-F]{64}$' || fail "invalid_receipt_hash_format"

STATE="$(jq -r '.state // .state_transition.current_state // empty' "$RECEIPT_FILE")"
[ "$STATE" = "FINALIZED" ] || [ "$STATE" = "GLOBAL_ROOT_FINALIZED" ] || fail "state_not_finalized"

GLOBAL_ROOT="$(jq -r '.global_root // .output.global_root // empty' "$RECEIPT_FILE")"
[ -n "$GLOBAL_ROOT" ] || fail "missing_global_root"

printf '%s' "$GLOBAL_ROOT" | grep -Eq '^0x[0-9a-fA-F]{64}$' || fail "invalid_global_root_format"

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

jq -cS '
  if has("receipt_hash") then
    .receipt_hash = null
    | del(.receipt_hash_status)
  elif has("output") and (.output | has("receipt_hash")) then
    .output.receipt_hash = null
    | .output |= del(.receipt_hash_status)
  else
    .
  end
' "$RECEIPT_FILE" > "$TMP"

COMPUTED_HASH="0x$(sha256sum "$TMP" | awk '{print $1}')"

if [ "$COMPUTED_HASH" != "$EXPECTED_HASH" ]; then
  echo "expected: $EXPECTED_HASH"
  echo "computed: $COMPUTED_HASH"
  fail "hash_mismatch"
fi

echo "ALMS_RECEIPT_VALID"
echo "receipt_hash: $EXPECTED_HASH"
echo "global_root: $GLOBAL_ROOT"
exit 0
