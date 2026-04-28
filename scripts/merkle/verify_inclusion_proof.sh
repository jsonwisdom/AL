#!/usr/bin/env bash
set -euo pipefail

PROOF="${1:?usage: verify_inclusion_proof.sh PROOF_JSON}"
test -f "$PROOF"

jq -e '.algorithm == "sha256_pairwise_sorted_v1" and .verdict == "PROVABLE_AGAINST_BASE"' "$PROOF" >/dev/null

CLAIM_ID="$(jq -r '.claim_id' "$PROOF")"
RECEIPT_PATH="$(jq -r '.receipt_path' "$PROOF")"
EXPECTED_LEAF="$(jq -r '.leaf_hash' "$PROOF")"
EXPECTED_ROOT="$(jq -r '.merkle_root' "$PROOF")"
EAS_UID="$(jq -r '.eas_anchor_uid' "$PROOF")"

test -f "$RECEIPT_PATH"

ACTUAL_LEAF="$(sha256sum "$RECEIPT_PATH" | awk '{print $1}')"
if [ "$EXPECTED_LEAF" != "$ACTUAL_LEAF" ]; then
  echo "ALMS_INCLUSION_VERIFY_FAIL leaf_hash_mismatch claim_id=$CLAIM_ID expected=$EXPECTED_LEAF actual=$ACTUAL_LEAF"
  exit 1
fi

TARGET="$EXPECTED_LEAF"
COUNT="$(jq '.proof_path | length' "$PROOF")"

for i in $(seq 0 $((COUNT - 1))); do
  NODE="$(jq -r ".proof_path[$i].node" "$PROOF")"
  SIBLING="$(jq -r ".proof_path[$i].sibling" "$PROOF")"
  PARENT="$(jq -r ".proof_path[$i].parent" "$PROOF")"

  if [ "$NODE" != "$TARGET" ]; then
    echo "ALMS_INCLUSION_VERIFY_FAIL proof_node_mismatch step=$i expected_current=$TARGET proof_node=$NODE"
    exit 1
  fi

  ACTUAL_PARENT="$(printf '%s%s' "$TARGET" "$SIBLING" | sha256sum | awk '{print $1}')"
  if [ "$PARENT" != "$ACTUAL_PARENT" ]; then
    echo "ALMS_INCLUSION_VERIFY_FAIL parent_mismatch step=$i expected=$PARENT actual=$ACTUAL_PARENT"
    exit 1
  fi

  TARGET="$PARENT"
done

if [ "$TARGET" != "$EXPECTED_ROOT" ]; then
  echo "ALMS_INCLUSION_VERIFY_FAIL root_mismatch expected=$EXPECTED_ROOT actual=$TARGET"
  exit 1
fi

case "$EAS_UID" in
  0x*) ;;
  *) echo "ALMS_INCLUSION_VERIFY_FAIL eas_uid_missing_or_unprefixed eas_uid=$EAS_UID"; exit 1 ;;
esac

echo "ALMS_INCLUSION_VERIFY_OK claim_id=$CLAIM_ID merkle_root=$EXPECTED_ROOT eas_uid=$EAS_UID"
