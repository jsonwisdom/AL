#!/usr/bin/env bash
#
# LIVE-SENDER TEMPLATE (NON-OPERATIONAL)
# --------------------------------------
# This file is a structural scaffold only.
# It cannot move funds, cannot sign, cannot broadcast.
# All sensitive values are placeholders.
#
# Boundary:
#   Browser signs.
#   Terminal verifies.
#   GitHub shows receipts.
#   ENS anchors identity.
#
# Until real browser-wallet registration exists, this script is inert by design.
#

set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

###############################################
# 0. ENV + PLACEHOLDERS (SAFE DEFAULTS)
###############################################
RPC_URL="${RPC_URL:-REDACTED_RPC}"
EAS_CONTRACT="${EAS_CONTRACT:-0xPLACEHOLDER_CONTRACT}"
SCHEMA_UID="${SCHEMA_UID:-0xPLACEHOLDER_SCHEMA_UID}"
SIGNING_INFRA="${SIGNING_INFRA:-EXTERNAL_ONLY}"
CHAIN_EXPECTED="8453"

###############################################
# 1. SAFETY GATE: BLOCK REAL EXECUTION
###############################################
if [[ "$RPC_URL" == "REDACTED_RPC" ]]; then
  echo "FAIL rpc_not_configured"
  echo "This script is inert until real RPC is provided."
  exit 1
fi

if [[ "$EAS_CONTRACT" == "0xPLACEHOLDER_CONTRACT" ]]; then
  echo "FAIL eas_contract_not_configured"
  exit 1
fi

if [[ "$SCHEMA_UID" == "0xPLACEHOLDER_SCHEMA_UID" ]]; then
  echo "FAIL schema_uid_not_configured"
  exit 1
fi

if [[ "$SIGNING_INFRA" != "EXTERNAL_ONLY" ]]; then
  echo "FAIL signer_must_remain_external"
  echo "This scaffold does not accept private keys or terminal signing."
  exit 1
fi

###############################################
# 2. CHAIN SANITY CHECK
###############################################
CHAIN_ID="$(cast chain-id --rpc-url "$RPC_URL" 2>/dev/null || echo "0")"

if [[ "$CHAIN_ID" != "$CHAIN_EXPECTED" ]]; then
  echo "FAIL wrong_chain_id=$CHAIN_ID expected=$CHAIN_EXPECTED"
  exit 1
fi

###############################################
# 3. CONTRACT BYTECODE CHECK
###############################################
CODE="$(cast code "$EAS_CONTRACT" --rpc-url "$RPC_URL" 2>/dev/null || echo "0x")"

if [[ "$CODE" == "0x" ]]; then
  echo "FAIL no_code_at_eas_contract=$EAS_CONTRACT"
  exit 1
fi

###############################################
# 4. LOAD PREVIEW WITNESS (REQUIRED)
###############################################
PREVIEW_FILE="${1:-}"

if [[ -z "$PREVIEW_FILE" ]]; then
  echo "FAIL no_preview_file_provided"
  echo "Usage: $0 _truth/attest/base_alms_attest_2026_04_v2_preview_*.txt"
  exit 1
fi

if [[ ! -f "$PREVIEW_FILE" ]]; then
  echo "FAIL preview_file_not_found=$PREVIEW_FILE"
  exit 1
fi

###############################################
# 5. EXTRACT REQUIRED FIELDS FROM PREVIEW
###############################################
extract() {
  grep -E "^$1=" "$PREVIEW_FILE" | sed "s/^$1=//"
}

MERKLE_ROOT="$(extract merkle_root)"
FUNC_SIG="$(extract func_sig)"
REQUEST="$(extract request)"
DATA="$(extract data)"

REQUIRED_NAMES=(merkle_root func_sig request data)
REQUIRED_VALUES=("$MERKLE_ROOT" "$FUNC_SIG" "$REQUEST" "$DATA")
for i in "${!REQUIRED_VALUES[@]}"; do
  if [[ -z "${REQUIRED_VALUES[$i]}" ]]; then
    echo "FAIL malformed_preview_missing_${REQUIRED_NAMES[$i]}"
    exit 1
  fi
done

###############################################
# 6. HUMAN-IN-THE-LOOP PREVIEW
###############################################
echo "--------------------------------------------"
echo " LIVE SENDER (NON-OPERATIONAL TEMPLATE)"
echo "--------------------------------------------"
echo "RPC_URL:       $RPC_URL"
echo "EAS_CONTRACT:  $EAS_CONTRACT"
echo "SCHEMA_UID:    $SCHEMA_UID"
echo "MERKLE_ROOT:   $MERKLE_ROOT"
echo "FUNC_SIG:      $FUNC_SIG"
echo "REQUEST:       $REQUEST"
echo "DATA:          $DATA"
echo "--------------------------------------------"
echo "This script is NOT sending a transaction."
echo "Signing and broadcasting are intentionally disabled."
echo "Private keys are not accepted by this scaffold."
echo "--------------------------------------------"
echo "To enable a live flow, use the browser-wallet tool:"
echo "  1. Browser signs"
echo "  2. Terminal verifies"
echo "  3. GitHub shows receipts"
echo "  4. ENS anchors identity"
echo "--------------------------------------------"
echo "EXITING (SAFE MODE)"
exit 0

###############################################
# 7. INTENTIONALLY DISABLED
#    NO SIGNING + NO BROADCAST SECTION
###############################################
# Terminal signing is retired.
# This file must not contain cast send, private-key flags,
# or any broadcast-capable command path.
###############################################
