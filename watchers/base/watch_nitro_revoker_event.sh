#!/usr/bin/env bash
set -euo pipefail

RPC="${RPC:-https://mainnet.base.org}"
CHAIN="${CHAIN:-base-mainnet}"
CONTRACT="0x08e49F31Ab11b17f3a5BaA36e6744E9B532bC87B"

STATE="_truth/base/nitro_event_${CHAIN}.json"
LOG="_truth/logs/nitro_revoker_event.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

# Event topic (RevokerUpdated(address,address))
TOPIC="0x99f8e0b3045f0b2f05192da79e25a5564759735adfee8dd3a642ba1093a7c936"

CURRENT_BLOCK="$(cast block-number --rpc-url "$RPC")"

# Init state
if [ ! -f "$STATE" ]; then
  jq -n \
    --arg chain "$CHAIN" \
    --arg contract "$CONTRACT" \
    --arg ts "$TS" \
    --argjson block "$CURRENT_BLOCK" \
    '{chain:$chain,contract:$contract,last_checked_at:$ts,last_block:$block,last_revoker:"UNKNOWN"}' > "$STATE"

  echo "$TS INIT $CHAIN block=$CURRENT_BLOCK" >> "$LOG"
  exit 0
fi

LAST_BLOCK="$(jq -r '.last_block' "$STATE")"

# Fetch logs
LOGS=$(cast logs \
  --from-block "$LAST_BLOCK" \
  --to-block "$CURRENT_BLOCK" \
  --address "$CONTRACT" \
  --topics "$TOPIC" \
  --rpc-url "$RPC" 2>/dev/null || echo "[]")

# Extract new revoker (last topic[2])
NEW_REV=$(echo "$LOGS" | jq -r '.[].topics[2]' | tail -n1)

# Update state
jq \
  --arg ts "$TS" \
  --argjson block "$CURRENT_BLOCK" \
  '.last_checked_at=$ts | .last_block=$block' \
  "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"

# If change detected
if [ "$NEW_REV" != "null" ] && [ -n "$NEW_REV" ]; then
  jq \
    --arg rev "$NEW_REV" \
    '.last_revoker=$rev' \
    "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"

  echo "$TS REVOKER_UPDATED $CHAIN new=$NEW_REV block=$CURRENT_BLOCK" >> "$LOG"
./watchers/base/notify_telegram.sh "⚠️ REVOKER UPDATED on $CHAIN: $NEW_REV"
fi
