#!/usr/bin/env bash
set -euo pipefail

RPC="${RPC:-https://mainnet.base.org}"
CHAIN="${CHAIN:-base-mainnet}"
CONTRACT="0x08e49F31Ab11b17f3a5BaA36e6744E9B532bC87B"

STATE="_truth/base/nitro_${CHAIN}.json"
LOG="_truth/logs/nitro_revoker.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

CURRENT_BLOCK="$(cast block-number --rpc-url "$RPC")"
CURRENT_REVOKER="$(cast call "$CONTRACT" "revoker()(address)" --rpc-url "$RPC" 2>/dev/null || echo "CALL_FAILED")"

if [ ! -f "$STATE" ]; then
  jq -n \
    --arg chain "$CHAIN" \
    --arg contract "$CONTRACT" \
    --arg revoker "$CURRENT_REVOKER" \
    --arg ts "$TS" \
    --argjson block "$CURRENT_BLOCK" \
    '{chain:$chain,contract:$contract,revoker:$revoker,last_checked_at:$ts,last_block:$block}' > "$STATE"

  echo "$TS INIT $CHAIN revoker=$CURRENT_REVOKER block=$CURRENT_BLOCK" >> "$LOG"
  exit 0
fi

OLD_REVOKER="$(jq -r '.revoker' "$STATE")"

jq \
  --arg revoker "$CURRENT_REVOKER" \
  --arg ts "$TS" \
  --argjson block "$CURRENT_BLOCK" \
  '.revoker=$revoker | .last_checked_at=$ts | .last_block=$block' \
  "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"

if [ "$CURRENT_REVOKER" != "$OLD_REVOKER" ]; then
  echo "$TS REVOKER_CHANGED $CHAIN old=$OLD_REVOKER new=$CURRENT_REVOKER block=$CURRENT_BLOCK" >> "$LOG"
fi
