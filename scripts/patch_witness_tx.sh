#!/usr/bin/env bash
#
# WITNESS TX PATCHER (STRUCTURAL ONLY)
# -----------------------------------
# Mutates ONLY tx.* fields in a derivative witness JSON.
# No RPC, no signing, no chain contact, no network I/O.
#

set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

WITNESS_IN="${1:-}"
TX_HASH="${2:-}"

if [[ -z "$WITNESS_IN" || -z "$TX_HASH" ]]; then
  echo "USAGE: $0 path/to/witness.json 0xTX_HASH"
  exit 1
fi

if [[ ! -f "$WITNESS_IN" ]]; then
  echo "FAIL witness_file_not_found=$WITNESS_IN"
  exit 1
fi

if [[ ! "$TX_HASH" =~ ^0x[0-9a-fA-F]{64}$ ]]; then
  echo "FAIL invalid_tx_hash_format=$TX_HASH"
  exit 1
fi

command -v jq >/dev/null || {
  echo "FAIL missing_jq"
  exit 1
}

STATUS="$(jq -r '.tx.status // empty' "$WITNESS_IN")"
if [[ -z "$STATUS" ]]; then
  echo "FAIL witness_missing_tx_status"
  exit 1
fi

if [[ "$STATUS" != "NOT_SUBMITTED" ]]; then
  echo "FAIL tx_status_not_mutable status=$STATUS"
  exit 1
fi

CHAIN_ID="$(jq -r '.env.chain_id // empty' "$WITNESS_IN")"
if [[ -z "$CHAIN_ID" ]]; then
  echo "FAIL witness_missing_chain_id"
  exit 1
fi

if [[ "$CHAIN_ID" != "8453" ]]; then
  echo "FAIL unsupported_chain_id=$CHAIN_ID expected=8453"
  exit 1
fi

WITNESS_OUT="${WITNESS_IN%.json}.with_tx.json"
BASESCAN_URL="https://basescan.org/tx/$TX_HASH"

ORIGINAL_NON_TX_HASH="$(jq -cS 'del(.tx)' "$WITNESS_IN" | sha256sum | awk '{print $1}')"

jq \
  --arg tx_hash "$TX_HASH" \
  --arg status "SUBMITTED" \
  --arg url "$BASESCAN_URL" \
  '.tx.status = $status | .tx.tx_hash = $tx_hash | .tx.basescan_url = $url | .tx.block_number = null' \
  "$WITNESS_IN" \
  | jq -cS \
  > "$WITNESS_OUT"

PATCHED_NON_TX_HASH="$(jq -cS 'del(.tx)' "$WITNESS_OUT" | sha256sum | awk '{print $1}')"
if [[ "$ORIGINAL_NON_TX_HASH" != "$PATCHED_NON_TX_HASH" ]]; then
  echo "FAIL non_tx_fields_mutated"
  rm -f "$WITNESS_OUT"
  exit 1
fi

PATCHED_HASH="$(jq -cS . "$WITNESS_OUT" | sha256sum | awk '{print $1}')"
echo "WITNESS_TX_PATCHED input=$WITNESS_IN output=$WITNESS_OUT tx_hash=$TX_HASH hash=$PATCHED_HASH status=SUBMITTED"
