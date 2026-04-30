#!/usr/bin/env bash
set -euo pipefail

RECEIPT="receipts/media_mesh_v1/global_root_receipt.pending.json"
FINAL="receipts/media_mesh_v1/global_root_receipt.final.json"

test -f "$RECEIPT" || { echo "MISSING_PENDING_RECEIPT"; exit 1; }

GLOBAL_ROOT="$(jq -r '.global_root' "$RECEIPT")"

if ! printf '%s' "$GLOBAL_ROOT" | grep -Eq '^0x[0-9a-fA-F]{64}$'; then
  echo "INVALID_GLOBAL_ROOT"
  exit 1
fi

TMP="$(mktemp)"

jq -cS '
  .state = "GLOBAL_ROOT_FINALIZED"
  | .next_gate = "NEW_CHAIN_BOOTSTRAP"
  | .receipt_hash = null
' "$RECEIPT" > "$TMP"

RECEIPT_HASH="0x$(sha256sum "$TMP" | awk "{print \$1}")"

jq -cS --arg h "$RECEIPT_HASH" '
  .receipt_hash = $h
  | .receipt_hash_status = "CANONICAL_SHA256_JQ_CS"
' "$TMP" > "$FINAL"

rm "$TMP"

echo "GLOBAL_ROOT_FINALIZED"
echo "global_root: $GLOBAL_ROOT"
echo "receipt_hash: $RECEIPT_HASH"
echo "final_receipt: $FINAL"
sha256sum "$FINAL"
