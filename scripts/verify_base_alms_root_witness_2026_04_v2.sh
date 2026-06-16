#!/usr/bin/env bash
#
# STATIC VERIFIER (NO NETWORK)
# ---------------------------
# Verifies preview -> witness consistency.
# No RPC, no signing, no network I/O.
#

set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

PREVIEW_FILE="${1:-}"
WITNESS_FILE="${2:-}"

if [[ -z "$PREVIEW_FILE" || -z "$WITNESS_FILE" ]]; then
  echo "USAGE: $0 preview.txt witness.json"
  exit 1
fi

if [[ ! -f "$PREVIEW_FILE" ]]; then
  echo "FAIL preview_file_not_found=$PREVIEW_FILE"
  exit 1
fi

if [[ ! -f "$WITNESS_FILE" ]]; then
  echo "FAIL witness_file_not_found=$WITNESS_FILE"
  exit 1
fi

command -v jq >/dev/null || { echo "FAIL missing_jq"; exit 1; }

require_line() {
  local key="$1"
  grep -qE "^${key}(=|$)" "$PREVIEW_FILE" || { echo "FAIL missing_required_line=$key"; exit 1; }
}

extract() {
  local key="$1"
  grep -E "^${key}=" "$PREVIEW_FILE" | head -n 1 | sed "s/^${key}=//"
}

# Required preview lines
for k in schema_uid merkle_root func_sig request data NO_SIGNER_USED NO_TX_SENT; do
  require_line "$k"
done

P_SCHEMA_UID="$(extract schema_uid)"
P_MERKLE_ROOT="$(extract merkle_root)"
P_FUNC_SIG="$(extract func_sig)"
P_REQUEST="$(extract request)"
P_DATA="$(extract data)"

W_CHAIN_ID="$(jq -r '.env.chain_id // empty' "$WITNESS_FILE")"
[[ -n "$W_CHAIN_ID" ]] || { echo "FAIL witness_missing_chain_id"; exit 1; }
[[ "$W_CHAIN_ID" == "8453" ]] || { echo "FAIL unsupported_chain_id=$W_CHAIN_ID"; exit 1; }

W_SCHEMA_UID="$(jq -r '.contracts.schema_uid // empty' "$WITNESS_FILE")"
[[ -n "$W_SCHEMA_UID" ]] || { echo "FAIL witness_missing_schema_uid"; exit 1; }
[[ "$P_SCHEMA_UID" == "$W_SCHEMA_UID" ]] || { echo "FAIL schema_uid_mismatch"; exit 1; }

W_MERKLE_ROOT="$(jq -r '.alms.merkle_root // empty' "$WITNESS_FILE")"
[[ -n "$W_MERKLE_ROOT" ]] || { echo "FAIL witness_missing_merkle_root"; exit 1; }
[[ "$P_MERKLE_ROOT" == "$W_MERKLE_ROOT" ]] || { echo "FAIL merkle_root_mismatch"; exit 1; }

W_FUNC_SIG="$(jq -r '.attestation.func_sig // empty' "$WITNESS_FILE")"
[[ -n "$W_FUNC_SIG" ]] || { echo "FAIL witness_missing_func_sig"; exit 1; }
[[ "$P_FUNC_SIG" == "$W_FUNC_SIG" ]] || { echo "FAIL func_sig_mismatch"; exit 1; }

W_REQUEST="$(jq -r '.attestation.request // empty' "$WITNESS_FILE")"
[[ -n "$W_REQUEST" ]] || { echo "FAIL witness_missing_request"; exit 1; }
[[ "$P_REQUEST" == "$W_REQUEST" ]] || { echo "FAIL request_mismatch"; exit 1; }

W_DATA="$(jq -r '.attestation.data // empty' "$WITNESS_FILE")"
[[ -n "$W_DATA" ]] || { echo "FAIL witness_missing_data"; exit 1; }
[[ "$P_DATA" == "$W_DATA" ]] || { echo "FAIL data_mismatch"; exit 1; }

STATUS="$(jq -r '.tx.status // empty' "$WITNESS_FILE")"
[[ -n "$STATUS" ]] || { echo "FAIL witness_missing_tx_status"; exit 1; }

case "$STATUS" in
  NOT_SUBMITTED|SUBMITTED) ;;
  *) echo "FAIL unsupported_tx_status=$STATUS"; exit 1 ;;
esac

if [[ "$STATUS" == "SUBMITTED" ]]; then
  TX_HASH="$(jq -r '.tx.tx_hash // empty' "$WITNESS_FILE")"
  [[ "$TX_HASH" =~ ^0x[0-9a-fA-F]{64}$ ]] || { echo "FAIL invalid_tx_hash_format=$TX_HASH"; exit 1; }
fi

HASH="$(jq -cS . "$WITNESS_FILE" | sha256sum | awk '{print $1}')"
echo "VERIFIER_OK witness=$WITNESS_FILE hash=$HASH status=$STATUS"
