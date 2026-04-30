#!/usr/bin/env bash
set -euo pipefail

MANIFEST="${1:-}"

fail() {
  echo "ALMS_SEGMENT_INVALID: $1"
  exit 1
}

[ -n "$MANIFEST" ] || fail "missing_manifest_argument"
[ -f "$MANIFEST" ] || fail "manifest_not_found"

jq empty "$MANIFEST" 2>/dev/null || fail "invalid_manifest_json"

REQUIRED_FIELDS=("segment_id" "state" "leaf_order" "global_root" "receipts")
for f in "${REQUIRED_FIELDS[@]}"; do
  jq -e "has(\"$f\")" "$MANIFEST" >/dev/null || fail "missing_manifest_field_$f"
done

TOP_LEVEL_COUNT=$(jq 'keys | length' "$MANIFEST")
if [ "$TOP_LEVEL_COUNT" -ne "${#REQUIRED_FIELDS[@]}" ]; then
  fail "unknown_manifest_fields"
fi

STATE=$(jq -r '.state' "$MANIFEST")
[ "$STATE" = "SEGMENT_SEALED" ] || fail "invalid_segment_state"

LEAF_ORDER=$(jq -r '.leaf_order' "$MANIFEST")
[ "$LEAF_ORDER" = "locked_manifest_order" ] || fail "invalid_leaf_order"

GLOBAL_ROOT=$(jq -r '.global_root' "$MANIFEST")
printf '%s' "$GLOBAL_ROOT" | grep -Eq '^0x[0-9a-fA-F]{64}$' || fail "invalid_global_root_format"

RECEIPT_COUNT=$(jq '.receipts | length' "$MANIFEST")
[ "$RECEIPT_COUNT" -gt 0 ] || fail "empty_receipts_array"

LEAVES=()

for i in $(seq 0 $((RECEIPT_COUNT - 1))); do
  RECEIPT_PATH=$(jq -r ".receipts[$i].receipt_path // empty" "$MANIFEST")
  RECEIPT_HASH=$(jq -r ".receipts[$i].receipt_hash // empty" "$MANIFEST")
  LEAF_ID=$(jq -r ".receipts[$i].leaf_id // empty" "$MANIFEST")

  [ -n "$RECEIPT_PATH" ] || fail "invalid_receipt_entry_missing_path"
  [ -n "$RECEIPT_HASH" ] || fail "invalid_receipt_entry_missing_hash"
  [ -n "$LEAF_ID" ] || fail "invalid_receipt_entry_missing_leaf_id"

  [ -f "$RECEIPT_PATH" ] || fail "receipt_file_not_found"

  printf '%s' "$RECEIPT_HASH" | grep -Eq '^0x[0-9a-fA-F]{64}$' || fail "invalid_receipt_hash_format"

  if ! ./scripts/verify_receipt.sh "$RECEIPT_PATH" >/dev/null; then
    fail "receipt_verification_failed"
  fi

  ACTUAL_HASH=$(jq -r '.receipt_hash // .output.receipt_hash // empty' "$RECEIPT_PATH")
  [ "$ACTUAL_HASH" = "$RECEIPT_HASH" ] || fail "receipt_hash_mismatch"

  RAW=$(printf "%s" "$RECEIPT_HASH" | sed 's/^0x//')
  LEAVES+=("$RAW")
done

compute_parent() {
  local left="$1"
  local right="$2"
  printf "%s" "$left$right" | xxd -r -p | sha256sum | awk '{print $1}'
}

LEVEL=("${LEAVES[@]}")

while [ "${#LEVEL[@]}" -gt 1 ]; do
  NEXT=()
  COUNT="${#LEVEL[@]}"

  for ((i=0; i<COUNT; i+=2)); do
    LEFT="${LEVEL[$i]}"
    if [ $((i+1)) -lt "$COUNT" ]; then
      RIGHT="${LEVEL[$((i+1))]}"
    else
      RIGHT="$LEFT"
    fi

    PARENT=$(compute_parent "$LEFT" "$RIGHT")
    NEXT+=("$PARENT")
  done

  LEVEL=("${NEXT[@]}")
done

COMPUTED_ROOT="0x${LEVEL[0]}"

[ "$COMPUTED_ROOT" = "$GLOBAL_ROOT" ] || fail "root_mismatch"

echo "ALMS_SEGMENT_VALID"
echo "global_root: $GLOBAL_ROOT"
echo "leaf_count: $RECEIPT_COUNT"
exit 0
