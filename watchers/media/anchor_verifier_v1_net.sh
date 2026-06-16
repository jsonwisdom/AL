#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — ANCHOR VERIFIER V1 NET
# PURPOSE: Network harness that resolves ENS/EAS into anchored_batch.json, then calls offline verifier
# RULE: No Merkle logic, no aggregation logic, no signing, no mutation of verifier core

if [ "$#" -lt 4 ]; then
  echo "usage: $0 <merged_receipts_jsonl> <ens_name> <ens_text_key> <eas_schema_uid>" >&2
  exit 2
fi

MERGED_JSONL="$1"
ENS_NAME="$2"
ENS_TEXT_KEY="$3"
EAS_SCHEMA_UID="$4"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
OFFLINE_VERIFIER="$SCRIPT_DIR/anchor_verifier_v1.sh"
TMP_ANCHORED="$(mktemp)"
trap 'rm -f "$TMP_ANCHORED"' EXIT

hard_fail() {
  jq -n -cS \
    --arg ens_name "$ENS_NAME" \
    --arg ens_text_key "$ENS_TEXT_KEY" \
    --arg reason "$1" \
    --arg timestamp_utc "$TIMESTAMP_UTC" \
    '{ens_name:$ens_name,ens_text_key:$ens_text_key,reason:$reason,timestamp_utc:$timestamp_utc,verify_status:"HARD_FAIL"}'
  exit 1
}

[ -f "$MERGED_JSONL" ] || hard_fail "MERGED_JSONL_NOT_FOUND"
[ -s "$MERGED_JSONL" ] || hard_fail "MERGED_JSONL_EMPTY"
[ -x "$OFFLINE_VERIFIER" ] || hard_fail "OFFLINE_VERIFIER_NOT_EXECUTABLE"
[ -n "$ENS_NAME" ] || hard_fail "ENS_NAME_EMPTY"
[ -n "$ENS_TEXT_KEY" ] || hard_fail "ENS_TEXT_KEY_EMPTY"
[ -n "$EAS_SCHEMA_UID" ] || hard_fail "EAS_SCHEMA_UID_EMPTY"

# Network boundary.
# Caller must provide explicit commands:
#   MEDIA_MESH_RESOLVE_ENS_CMD: prints EAS attestation UID from ENS name + text key
#   MEDIA_MESH_FETCH_EAS_CMD: prints EAS attestation JSON from attestation UID
#
# Expected calls:
#   $MEDIA_MESH_RESOLVE_ENS_CMD "$ENS_NAME" "$ENS_TEXT_KEY"
#   $MEDIA_MESH_FETCH_EAS_CMD "$ATTESTATION_UID"

[ -n "${MEDIA_MESH_RESOLVE_ENS_CMD:-}" ] || hard_fail "ENS_RESOLVER_COMMAND_NOT_CONFIGURED"
[ -n "${MEDIA_MESH_FETCH_EAS_CMD:-}" ] || hard_fail "EAS_FETCH_COMMAND_NOT_CONFIGURED"

ATTESTATION_UID="$($MEDIA_MESH_RESOLVE_ENS_CMD "$ENS_NAME" "$ENS_TEXT_KEY")"
[ -n "$ATTESTATION_UID" ] || hard_fail "ENS_POINTER_EMPTY"

case "$ATTESTATION_UID" in
  0x[0-9a-fA-F]*) ;;
  *) hard_fail "ENS_POINTER_NOT_UID_SHAPED" ;;
esac

EAS_JSON="$($MEDIA_MESH_FETCH_EAS_CMD "$ATTESTATION_UID")"
[ -n "$EAS_JSON" ] || hard_fail "EAS_FETCH_EMPTY"
printf '%s' "$EAS_JSON" | jq -e . >/dev/null 2>&1 || hard_fail "EAS_JSON_MALFORMED"

ATTESTED_SCHEMA_UID="$(printf '%s' "$EAS_JSON" | jq -r '.schema_uid // .schemaUid // .schema // ""')"
[ "$ATTESTED_SCHEMA_UID" = "$EAS_SCHEMA_UID" ] || hard_fail "EAS_SCHEMA_UID_MISMATCH"

REVOKED="$(printf '%s' "$EAS_JSON" | jq -r '.revoked // false')"
[ "$REVOKED" = "false" ] || hard_fail "EAS_ATTESTATION_REVOKED"

BATCH_ID="$(printf '%s' "$EAS_JSON" | jq -r '.batch_id // .batchId // .data.batch_id // .data.batchId // ""')"
MERKLE_ROOT="$(printf '%s' "$EAS_JSON" | jq -r '.merkle_root // .merkleRoot // .data.merkle_root // .data.merkleRoot // ""')"
LEAF_COUNT="$(printf '%s' "$EAS_JSON" | jq -r '.leaf_count // .leafCount // .data.leaf_count // .data.leafCount // ""')"
BATCH_TIMESTAMP_UTC="$(printf '%s' "$EAS_JSON" | jq -r '.timestamp_utc // .timestampUtc // .data.timestamp_utc // .data.timestampUtc // ""')"

[ -n "$BATCH_ID" ] || hard_fail "EAS_BATCH_ID_MISSING"
[ -n "$MERKLE_ROOT" ] || hard_fail "EAS_MERKLE_ROOT_MISSING"
[ -n "$LEAF_COUNT" ] || hard_fail "EAS_LEAF_COUNT_MISSING"
[ -n "$BATCH_TIMESTAMP_UTC" ] || hard_fail "EAS_TIMESTAMP_MISSING"

jq -n -cS \
  --arg batch_id "$BATCH_ID" \
  --arg merkle_root "$MERKLE_ROOT" \
  --arg timestamp_utc "$BATCH_TIMESTAMP_UTC" \
  --argjson leaf_count "$LEAF_COUNT" \
  '{batch_id:$batch_id,leaf_count:$leaf_count,merkle_root:$merkle_root,timestamp_utc:$timestamp_utc}' > "$TMP_ANCHORED"

OFFLINE_RESULT="$($OFFLINE_VERIFIER "$MERGED_JSONL" "$TMP_ANCHORED")"
printf '%s' "$OFFLINE_RESULT" | jq -e . >/dev/null 2>&1 || hard_fail "OFFLINE_VERIFIER_OUTPUT_MALFORMED"

jq -n -cS \
  --arg attestation_uid "$ATTESTATION_UID" \
  --arg eas_schema_uid "$EAS_SCHEMA_UID" \
  --arg ens_name "$ENS_NAME" \
  --arg ens_text_key "$ENS_TEXT_KEY" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --argjson offline_result "$OFFLINE_RESULT" \
  '{attestation_uid:$attestation_uid,eas_schema_uid:$eas_schema_uid,ens_name:$ens_name,ens_text_key:$ens_text_key,offline_result:$offline_result,timestamp_utc:$timestamp_utc,verify_status:$offline_result.verify_status}'
