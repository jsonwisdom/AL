#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — ANCHOR PUBLISHER V1
# PURPOSE: Validate canonical batch summary and emit wallet-safe EAS anchor payload
# RULE: No private keys, no terminal signing, no leaf recomputation, no Merkle recomputation

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <batch_summary_json> [--update-ens]" >&2
  exit 2
fi

BATCH_JSON="$1"
UPDATE_ENS="SKIPPED"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [ "${2:-}" = "--update-ens" ]; then
  UPDATE_ENS="REQUESTED"
fi

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$TIMESTAMP_UTC" '{anchor_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
}

[ -f "$BATCH_JSON" ] || hard_fail "BATCH_FILE_NOT_FOUND"
[ -s "$BATCH_JSON" ] || hard_fail "BATCH_FILE_EMPTY"

jq -e '.batch_id and .merkle_root and (.leaf_count != null) and .timestamp_utc' "$BATCH_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_BATCH_SUMMARY"

CANONICAL_BATCH="$(jq -cS . "$BATCH_JSON")"
INPUT_BYTES="$(cat "$BATCH_JSON")"
[ "$INPUT_BYTES" = "$CANONICAL_BATCH" ] || hard_fail "NON_CANONICAL_BATCH_SUMMARY"

BATCH_ID="$(jq -r '.batch_id' "$BATCH_JSON")"
MERKLE_ROOT="$(jq -r '.merkle_root' "$BATCH_JSON")"
LEAF_COUNT="$(jq -r '.leaf_count' "$BATCH_JSON")"
BATCH_TIMESTAMP_UTC="$(jq -r '.timestamp_utc' "$BATCH_JSON")"

BATCH_HASH="$(printf '%s' "$CANONICAL_BATCH" | sha256sum | awk '{print $1}')"

[ "$BATCH_HASH" = "$BATCH_ID" ] || hard_fail "BATCH_HASH_ID_MISMATCH"

case "$BATCH_HASH" in
  [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) ;;
  *) hard_fail "INVALID_BATCH_HASH_HEX" ;;
esac

case "$MERKLE_ROOT" in
  [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) ;;
  *) hard_fail "INVALID_MERKLE_ROOT_HEX" ;;
esac

EAS_PAYLOAD="$(jq -n -cS \
  --arg batchId "0x$BATCH_HASH" \
  --arg merkleRoot "0x$MERKLE_ROOT" \
  --arg timestampUtc "$BATCH_TIMESTAMP_UTC" \
  --argjson leafCount "$LEAF_COUNT" \
  '{batchId:$batchId,leafCount:$leafCount,merkleRoot:$merkleRoot,timestampUtc:$timestampUtc}')"

# Wallet-safe boundary: this script does not sign or send.
# Browser/wallet publisher consumes eas_payload and returns eas_attestation_uid.
EAS_ATTESTATION_UID="PENDING_WALLET_SIGNATURE"

jq -n -cS \
  --arg batch_hash "$BATCH_HASH" \
  --arg batch_id "$BATCH_ID" \
  --arg eas_attestation_uid "$EAS_ATTESTATION_UID" \
  --arg eas_payload "$EAS_PAYLOAD" \
  --arg ens_update "$UPDATE_ENS" \
  --arg merkle_root "$MERKLE_ROOT" \
  --arg timestamp_utc "$BATCH_TIMESTAMP_UTC" \
  --argjson leaf_count "$LEAF_COUNT" \
  '{batch_hash:$batch_hash,batch_id:$batch_id,eas_attestation_uid:$eas_attestation_uid,eas_payload:($eas_payload|fromjson),ens_update:$ens_update,leaf_count:$leaf_count,merkle_root:$merkle_root,timestamp_utc:$timestamp_utc}'
