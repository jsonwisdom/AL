#!/usr/bin/env bash
set -euo pipefail

RPC="${RPC:-https://mainnet.base.org}"
CHAIN="${CHAIN:-base-mainnet}"
CONTRACT="0x08e49F31Ab11b17f3a5BaA36e6744E9B532bC87B"

STATE="_truth/base/nitro_sentinel_${CHAIN}.json"
ALERTS="_truth/logs/nitro_alerts.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

BLOCK="$(cast block-number --rpc-url "$RPC")"
CODE_HASH="$(cast code "$CONTRACT" --rpc-url "$RPC" | cast keccak)"

if [ ! -f "$STATE" ]; then
  jq -n \
    --arg chain "$CHAIN" \
    --arg contract "$CONTRACT" \
    --arg code_hash "$CODE_HASH" \
    --arg ts "$TS" \
    --argjson block "$BLOCK" \
    '{chain:$chain,contract:$contract,code_hash:$code_hash,last_checked_at:$ts,last_block:$block,alerts:0}' > "$STATE"

  echo "$TS INIT_SENTINEL $CHAIN code_hash=$CODE_HASH block=$BLOCK" >> "$ALERTS"
  exit 0
fi

OLD_HASH="$(jq -r '.code_hash' "$STATE")"
ALERTS_COUNT="$(jq -r '.alerts' "$STATE")"

if [ "$CODE_HASH" != "$OLD_HASH" ]; then
  ALERTS_COUNT=$((ALERTS_COUNT + 1))
  echo "$TS CONTRACT_CODEHASH_CHANGED $CHAIN old=$OLD_HASH new=$CODE_HASH block=$BLOCK" >> "$ALERTS"
./watchers/base/notify_telegram.sh "🔥 CODEHASH CHANGED on $CHAIN old=$OLD_HASH new=$CODE_HASH"
fi

jq \
  --arg code_hash "$CODE_HASH" \
  --arg ts "$TS" \
  --argjson block "$BLOCK" \
  --argjson alerts "$ALERTS_COUNT" \
  '.code_hash=$code_hash | .last_checked_at=$ts | .last_block=$block | .alerts=$alerts' \
  "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"
