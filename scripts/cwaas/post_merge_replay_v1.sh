#!/usr/bin/env bash
set -euo pipefail

MERGE_COMMIT="a6ffdc2b8ec45e0141bf9a6a989a793316236ae5"
SPEC="projects/cwaas/gates/AUDIT_WORKFLOW_STOREFRONT_01_INTAKE_GATE_SPEC_V1.json"
DIR="receipts/cwaas"
RECEIPT="$DIR/POST_MERGE_REPLAY_RECEIPT_V1.json"
OUT="$DIR/post_merge_replay_output.txt"

mkdir -p "$DIR"

{
  echo "POST_MERGE_REPLAY_V1"
  echo "merge_commit=$MERGE_COMMIT"
  echo "spec=$SPEC"
  echo "branch=master"
} > "$OUT"

git rev-parse "$MERGE_COMMIT^{tree}" > "$DIR/tree_sha.txt"

test -f "$SPEC"

jq -e '
  .identity.root_identity == "jaywisdom.base.eth"
  and .identity.aliases_authority == "provenance_only"
  and .identity.authority_escalation == "DISABLED"
  and .locks.treasury_access == "DENIED"
  and .locks.payment_execution == false
  and .locks.token_claim == false
  and .locks.settlement_claim == false
  and .locks.family_layer_protected == true
  and .doctrine.no_fake_green == true
' "$SPEC" >> "$OUT"

HASH_TREE_SHA=$(sha256sum "$DIR/tree_sha.txt" | cut -d' ' -f1)
HASH_SPEC=$(sha256sum "$SPEC" | cut -d' ' -f1)
HASH_REPLAY_OUTPUT=$(sha256sum "$OUT" | cut -d' ' -f1)
HASH_RECEIPT_STABILITY=$(sha256sum "$RECEIPT" | cut -d' ' -f1)

{
  echo "HASH_TREE_SHA=$HASH_TREE_SHA"
  echo "HASH_SPEC=$HASH_SPEC"
  echo "HASH_REPLAY_OUTPUT=$HASH_REPLAY_OUTPUT"
  echo "HASH_RECEIPT_STABILITY=$HASH_RECEIPT_STABILITY"
} | tee "$DIR/post_merge_replay_hashes.env"

echo "POST_MERGE_REPLAY_HASHES_COMPUTED"
echo "NO_FAKE_HASHES"
