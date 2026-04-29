#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
source ./env_base.sh
mkdir -p _truth/attest

: "${MERKLE_ROOT:?MERKLE_ROOT required}"
[[ "$MERKLE_ROOT" =~ ^0x[0-9a-fA-F]{64}$ ]] || { echo "FAIL invalid_merkle_root_bytes32=$MERKLE_ROOT"; exit 1; }

: "${ALMS_SCHEMA_UID:?ALMS_SCHEMA_UID required}"
: "${EAS_CONTRACT:?EAS_CONTRACT required}"

EPOCH="2026-04-v2"
MODE="GENESIS"
WITNESS_COUNT="${WITNESS_COUNT:-1}"
RECIPIENT="${RECIPIENT:-0x0000000000000000000000000000000000000000}"
EXPIRATION_TIME="${EXPIRATION_TIME:-0}"
ATTESTATION_REVOCABLE="${ATTESTATION_REVOCABLE:-true}"
REF_UID="${REF_UID:-0x0000000000000000000000000000000000000000000000000000000000000000}"
VALUE="${VALUE:-0}"

command -v cast >/dev/null || { echo "FAIL missing_cast"; exit 1; }

CHAIN_ID="$(cast chain-id --rpc-url "$BASE_RPC")"
[ "$CHAIN_ID" = "8453" ] || { echo "FAIL wrong_chain_id=$CHAIN_ID expected=8453"; exit 1; }

RAW_SCHEMA="$(cast call "$SCHEMA_REGISTRY" \
  "getSchema(bytes32)((bytes32,address,bool,string))" \
  "$ALMS_SCHEMA_UID" \
  --rpc-url "$BASE_RPC")"

# Check if schema is live, but only warn for preview
case "$RAW_SCHEMA" in
  *"bytes32 merkleRoot,string epoch,string mode,uint8 witnessCount"*)
    SCHEMA_STATUS="LIVE"
    ;;
  *)
    echo "WARNING: schema_uid_not_live_or_mismatch - PROCEEDING WITH PREVIEW ONLY"
    echo "DEBUG_RAW_SCHEMA: $RAW_SCHEMA"
    SCHEMA_STATUS="PREVIEW_ONLY_MOCK"
    ;;
esac

DATA="$(cast abi-encode \
  "f(bytes32,string,string,uint8)" \
  "$MERKLE_ROOT" "$EPOCH" "$MODE" "$WITNESS_COUNT")"

[[ "$DATA" =~ ^0x[0-9a-fA-F]+$ ]] || { echo "FAIL data_not_hex=$DATA"; exit 1; }

FUNC_SIG="attest((bytes32,(address,uint64,bool,bytes32,bytes,uint256)))"
REQUEST="($ALMS_SCHEMA_UID,($RECIPIENT,$EXPIRATION_TIME,$ATTESTATION_REVOCABLE,$REF_UID,$DATA,$VALUE))"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="_truth/attest/base_alms_attest_2026_04_v2_preview_$TS.txt"

{
  echo "ALMS_BASE_ATTEST_PREVIEW_V3"
  echo "time=$TS"
  echo "chain_id=$CHAIN_ID"
  echo "eas_contract=$EAS_CONTRACT"
  echo "schema_uid=$ALMS_SCHEMA_UID"
  echo "schema_status=$SCHEMA_STATUS"
  echo "merkle_root=$MERKLE_ROOT"
  echo "epoch=$EPOCH"
  echo "mode=$MODE"
  echo "witness_count=$WITNESS_COUNT"
  echo "recipient=$RECIPIENT"
  echo "expiration_time=$EXPIRATION_TIME"
  echo "revocable=$ATTESTATION_REVOCABLE"
  echo "ref_uid=$REF_UID"
  echo "value=$VALUE"
  echo "raw_schema=$RAW_SCHEMA"
  echo "func_sig=$FUNC_SIG"
  echo "request=$REQUEST"
  echo "data=$DATA"
  echo "NO_SIGNER_USED"
  echo "NO_TX_SENT"
  echo "ATTEST_PREVIEW_REPORT=$OUT"
} | tee "$OUT"
