#!/usr/bin/env bash
set -euo pipefail

RULE_ID="ALMS_GLOBAL_MERKLE_RULE_V1"
LEAF_ID="MEDIA_MESH_V1"
LEAF_HASH="0x5aa1dd96735e02ba2d7a9cc41b4a4ed4cb0c11ed5366303eeb00262a4a9773ed"

OUT="_truth/merkle/global_root_v1.txt"
RECEIPT="receipts/media_mesh_v1/global_root_receipt.pending.json"

# Validate 0x-prefixed 32-byte hex
if ! printf '%s' "$LEAF_HASH" | grep -Eq '^0x[0-9a-fA-F]{64}$'; then
  echo "INVALID_LEAF_HASH"
  exit 1
fi

# ALMS_GLOBAL_MERKLE_RULE_V1:
# if leaf_count == 1: global_root = leaf_hash
LEAF_COUNT=1
GLOBAL_ROOT="$LEAF_HASH"

cat > "$OUT" <<ROOT
SUPPLY_GLOBAL_ROOT
global_root: $GLOBAL_ROOT
leaf_count: $LEAF_COUNT
merkle_rule: $RULE_ID
leaf_order: locked_manifest_order
single_leaf_rule: global_root = leaf_hash
source: terminal_bash
ROOT

cat > "$RECEIPT" <<JSON
{
  "receipt_type": "ALMS_GLOBAL_ROOT_RECEIPT",
  "version": "v1",
  "state": "AWAITING_OPERATOR_SUPPLIED_GLOBAL_ROOT",
  "next_gate": "SUPPLY_GLOBAL_ROOT",
  "merkle_rule": "$RULE_ID",
  "leaf_order": "locked_manifest_order",
  "single_leaf_rule": "global_root = leaf_hash",
  "leaf_count": $LEAF_COUNT,
  "included_leaf": {
    "leaf_id": "$LEAF_ID",
    "leaf_hash": "$LEAF_HASH"
  },
  "global_root": "$GLOBAL_ROOT",
  "global_root_status": "OPERATOR_COMPUTED_TERMINAL_BASH",
  "receipt_hash": null
}
JSON

sha256sum "$OUT" "$RECEIPT"

echo
cat "$OUT"
