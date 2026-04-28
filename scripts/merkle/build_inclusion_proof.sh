#!/usr/bin/env bash
set -euo pipefail

MONTH="${1:?usage: build_inclusion_proof.sh YYYY-MM CLAIM_ID}"
CLAIM_ID="${2:?usage: build_inclusion_proof.sh YYYY-MM CLAIM_ID}"
LEDGER="_truth/ledger/$MONTH.jsonl"
ROOT_JSON="_truth/merkle/root.json"
OUT_DIR="_truth/merkle/proofs"
DOCS_DIR="docs/merkle/proofs"
OUT="$OUT_DIR/$CLAIM_ID.json"
DOCS_OUT="$DOCS_DIR/$CLAIM_ID.json"

mkdir -p "$OUT_DIR" "$DOCS_DIR"
test -f "$LEDGER"
test -f "$ROOT_JSON"

ROOT_MONTH="$(jq -r '.month' "$ROOT_JSON")"
if [ "$ROOT_MONTH" != "$MONTH" ]; then
  echo "ALMS_INCLUSION_BUILD_FAIL month_mismatch expected=$MONTH actual=$ROOT_MONTH"
  exit 1
fi

MERKLE_ROOT="$(jq -r '.merkle_root' "$ROOT_JSON")"
EAS_UID="$(jq -r '.attestation_uid // "PENDING"' "_truth/eas/merkle_anchor_$MONTH.json" 2>/dev/null || echo PENDING)"
TX_HASH="$(jq -r '.tx_hash // "PENDING"' "_truth/eas/merkle_anchor_$MONTH.json" 2>/dev/null || echo PENDING)"

LEAF_HASH="$(jq -r --arg claim_id "$CLAIM_ID" 'select(.claim_id == $claim_id) | .sha256' "$LEDGER")"
RECEIPT_PATH="$(jq -r --arg claim_id "$CLAIM_ID" 'select(.claim_id == $claim_id) | .path' "$LEDGER")"

if [ -z "$LEAF_HASH" ] || [ "$LEAF_HASH" = "null" ]; then
  echo "ALMS_INCLUSION_BUILD_FAIL claim_not_found claim_id=$CLAIM_ID ledger=$LEDGER"
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

jq -r '.sha256' "$LEDGER" | LC_ALL=C sort > "$TMP/current.txt"
TARGET="$LEAF_HASH"
LEVEL=0
PROOF_JSONL="$TMP/proof.jsonl"
: > "$PROOF_JSONL"

while [ "$(wc -l < "$TMP/current.txt" | tr -d ' ')" -gt 1 ]; do
  mapfile -t nodes < "$TMP/current.txt"
  INDEX=-1
  for i in "${!nodes[@]}"; do
    if [ "${nodes[$i]}" = "$TARGET" ]; then
      INDEX="$i"
      break
    fi
  done

  if [ "$INDEX" = "-1" ]; then
    echo "ALMS_INCLUSION_BUILD_FAIL target_missing_at_level level=$LEVEL target=$TARGET"
    exit 1
  fi

  if [ $((INDEX % 2)) -eq 0 ]; then
    SIBLING_INDEX=$((INDEX + 1))
  else
    SIBLING_INDEX=$((INDEX - 1))
  fi

  if [ "$SIBLING_INDEX" -ge "${#nodes[@]}" ]; then
    SIBLING="${nodes[$INDEX]}"
    DUPLICATED=true
  else
    SIBLING="${nodes[$SIBLING_INDEX]}"
    DUPLICATED=false
  fi

  PARENT="$(printf '%s%s' "$TARGET" "$SIBLING" | sha256sum | awk '{print $1}')"

  jq -cn \
    --argjson level "$LEVEL" \
    --arg node "$TARGET" \
    --arg sibling "$SIBLING" \
    --arg parent "$PARENT" \
    --argjson node_index "$INDEX" \
    --argjson sibling_index "$SIBLING_INDEX" \
    --argjson duplicated "$DUPLICATED" \
    '{level:$level,node:$node,sibling:$sibling,parent:$parent,node_index:$node_index,sibling_index:$sibling_index,duplicated:$duplicated}' >> "$PROOF_JSONL"

  : > "$TMP/next.txt"
  i=0
  while [ "$i" -lt "${#nodes[@]}" ]; do
    left="${nodes[$i]}"
    right="${nodes[$((i+1))]:-${nodes[$i]}}"
    printf '%s%s' "$left" "$right" | sha256sum | awk '{print $1}' >> "$TMP/next.txt"
    i=$((i+2))
  done

  LEVEL=$((LEVEL + 1))
  LC_ALL=C sort "$TMP/next.txt" > "$TMP/current.txt"
  TARGET="$PARENT"
done

RECOMPUTED_ROOT="$(cat "$TMP/current.txt")"
if [ "$RECOMPUTED_ROOT" != "$MERKLE_ROOT" ]; then
  echo "ALMS_INCLUSION_BUILD_FAIL root_mismatch expected=$MERKLE_ROOT actual=$RECOMPUTED_ROOT"
  exit 1
fi

BUILT_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -cn \
  --arg proof_id "ALMS_INCLUSION_${CLAIM_ID}" \
  --arg month "$MONTH" \
  --arg claim_id "$CLAIM_ID" \
  --arg receipt_path "$RECEIPT_PATH" \
  --arg leaf_hash "$LEAF_HASH" \
  --arg merkle_root "$MERKLE_ROOT" \
  --arg eas_anchor_uid "$EAS_UID" \
  --arg tx_hash "$TX_HASH" \
  --arg algorithm "sha256_pairwise_sorted_v1" \
  --arg verdict "PROVABLE_AGAINST_BASE" \
  --arg built_at_utc "$BUILT_AT" \
  --slurpfile proof_path "$PROOF_JSONL" \
  '{proof_id:$proof_id,month:$month,claim_id:$claim_id,receipt_path:$receipt_path,leaf_hash:$leaf_hash,merkle_root:$merkle_root,eas_anchor_uid:$eas_anchor_uid,tx_hash:$tx_hash,algorithm:$algorithm,proof_path:$proof_path,verdict:$verdict,built_at_utc:$built_at_utc}' > "$OUT"

cp "$OUT" "$DOCS_OUT"
echo "ALMS_INCLUSION_BUILD_OK claim_id=$CLAIM_ID proof=$OUT merkle_root=$MERKLE_ROOT eas_uid=$EAS_UID"
