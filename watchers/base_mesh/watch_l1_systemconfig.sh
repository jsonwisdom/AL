#!/usr/bin/env bash
set -euo pipefail

CHAIN="${CHAIN:-ethereum-mainnet}"
RPC="${RPC:-https://ethereum.publicnode.com}"
CONTRACT="${CONTRACT:-0x73a79Fab69143498Ed3712e519A88a918e1f4072}"

STATE="_truth/base_mesh/systemconfig_${CHAIN}.json"
LOG="_truth/logs/systemconfig_mesh.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base_mesh _truth/logs

BLOCK="$(cast block-number --rpc-url "$RPC")"
CODE="$(cast code "$CONTRACT" --rpc-url "$RPC" 2>/dev/null || echo "CODE_READ_ERROR")"

if [ "$CODE" = "0x" ] || [ "$CODE" = "CODE_READ_ERROR" ]; then
  jq -n \
    --arg chain "$CHAIN" \
    --arg contract "$CONTRACT" \
    --arg ts "$TS" \
    --argjson block "$BLOCK" \
    '{chain:$chain,contract:$contract,last_checked_at:$ts,last_block:$block,status:"YELLOW_CODE_UNAVAILABLE"}' > "$STATE"
  echo "$TS YELLOW_CODE_UNAVAILABLE $CHAIN contract=$CONTRACT block=$BLOCK" >> "$LOG"
  exit 0
fi

CODE_HASH="$(printf "%s" "$CODE" | cast keccak)"

OWNER="$(cast call "$CONTRACT" 0x8da5cb5b --rpc-url "$RPC" 2>/dev/null || echo "READ_ERROR")"
IMPL="$(cast call "$CONTRACT" 0x5c60da1b --rpc-url "$RPC" 2>/dev/null || echo "READ_ERROR")"

if [ ! -f "$STATE" ]; then
  jq -n \
    --arg chain "$CHAIN" \
    --arg contract "$CONTRACT" \
    --arg code_hash "$CODE_HASH" \
    --arg owner "$OWNER" \
    --arg impl "$IMPL" \
    --arg ts "$TS" \
    --argjson block "$BLOCK" \
    '{chain:$chain,contract:$contract,last_checked_at:$ts,last_block:$block,code_hash:$code_hash,owner_live:$owner,implementation_live:$impl,status:(($owner=="READ_ERROR" or $impl=="READ_ERROR")?"YELLOW_DEGRADED_VISIBILITY":"INIT")}' > "$STATE"

  echo "$TS INIT_SYSTEMCONFIG $CHAIN code_hash=$CODE_HASH owner=$OWNER impl=$IMPL block=$BLOCK" >> "$LOG"
  exit 0
fi

OLD_CODE="$(jq -r '.code_hash // "UNKNOWN"' "$STATE")"
OLD_OWNER="$(jq -r '.owner_live // "UNKNOWN"' "$STATE")"
OLD_IMPL="$(jq -r '.implementation_live // "UNKNOWN"' "$STATE")"

STATUS="GREEN"

if [ "$OWNER" = "READ_ERROR" ] || [ "$IMPL" = "READ_ERROR" ]; then
  STATUS="YELLOW_DEGRADED_VISIBILITY"
fi

if [ "$CODE_HASH" != "$OLD_CODE" ] || [ "$OWNER" != "$OLD_OWNER" ] || [ "$IMPL" != "$OLD_IMPL" ]; then
  STATUS="RED_MUTATION_DETECTED"
  echo "$TS RED_MUTATION_DETECTED $CHAIN old_code=$OLD_CODE new_code=$CODE_HASH old_owner=$OLD_OWNER new_owner=$OWNER old_impl=$OLD_IMPL new_impl=$IMPL block=$BLOCK" >> "$LOG"
fi

jq -n \
  --arg chain "$CHAIN" \
  --arg contract "$CONTRACT" \
  --arg code_hash "$CODE_HASH" \
  --arg owner "$OWNER" \
  --arg impl "$IMPL" \
  --arg status "$STATUS" \
  --arg ts "$TS" \
  --argjson block "$BLOCK" \
  '{chain:$chain,contract:$contract,last_checked_at:$ts,last_block:$block,code_hash:$code_hash,owner_live:$owner,implementation_live:$impl,status:$status}' > "$STATE.tmp"

mv "$STATE.tmp" "$STATE"
