#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/root/alms_root.json"
TMP="$(mktemp)"

mkdir -p _truth/root

# Build canonical root directly
jq -s -cS '{
  system:"ALMS",
  version:1,
  receipts: map({
    leaf_id,
    canonical_sha256,
    status,
    risk
  }) | sort_by(.leaf_id)
}' _truth/receipts/*.receipt.json > "$TMP"

# Hash the canonical root
HASH="$(sha256sum "$TMP" | awk '{print $1}')"

# Wrap with root hash
jq -cS --arg root_hash "$HASH" \
  '{root: ., root_sha256: $root_hash}' \
  "$TMP" > "$OUT"

COUNT="$(jq '.root.receipts | length' "$OUT")"

echo "ALMS_ROOT_OK leaves=$COUNT hash=$HASH file=$OUT"

rm -f "$TMP"
