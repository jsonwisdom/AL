#!/usr/bin/env bash
set -euo pipefail

RPC="${RPC:-https://mainnet.base.org}"
CHAIN="${CHAIN:-base-mainnet}"
CONTRACT="0x08e49F31Ab11b17f3a5BaA36e6744E9B532bC87B"

STATE="_truth/base/nitro_calls_${CHAIN}.json"
LOG="_truth/logs/nitro_revoke_calls.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

# revokeCert selector (CONFIRMED)
SELECTOR="0x8cb50c44"

CURRENT_BLOCK="$(cast block-number --rpc-url "$RPC")"

# Init state
if [ ! -f "$STATE" ]; then
  jq -n \
    --arg chain "$CHAIN" \
    --arg contract "$CONTRACT" \
    --arg ts "$TS" \
    --argjson block "$CURRENT_BLOCK" \
    '{chain:$chain,contract:$contract,last_checked_at:$ts,last_block:$block,total_revoke_calls:0}' > "$STATE"

  echo "$TS INIT $CHAIN block=$CURRENT_BLOCK" >> "$LOG"
  exit 0
fi

LAST_BLOCK="$(jq -r '.last_block' "$STATE")"

# Pull tx list (light scan via cast)
TXS=$(cast rpc eth_getLogs '{
  "fromBlock": "'$(printf "0x%x" $LAST_BLOCK)'",
  "toBlock": "'$(printf "0x%x" $CURRENT_BLOCK)'",
  "address": "'$CONTRACT'"
}' 2>/dev/null || echo "[]")

# Extract tx hashes
HASHES=$(echo "$TXS" | jq -r '.[].transactionHash' | sort -u)

NEW_COUNT=0

for TX in $HASHES; do
  INPUT=$(cast tx $TX --rpc-url "$RPC" 2>/dev/null | grep input | awk '{print $2}' || echo "")

  if [[ "$INPUT" == "$SELECTOR"* ]]; then
    CERT_HASH="0x${INPUT:10}"   # strip selector (4 bytes = 8 hex chars + 0x)

    echo "$TS REVOKE_CALL $CHAIN tx=$TX certHash=$CERT_HASH" >> "$LOG"
./watchers/base/notify_telegram.sh "🚨 REVOKE CERT on $CHAIN tx=$TX certHash=$CERT_HASH"
    NEW_COUNT=$((NEW_COUNT + 1))
  fi
done

# Update state
TOTAL=$(jq -r '.total_revoke_calls' "$STATE")

jq \
  --arg ts "$TS" \
  --argjson block "$CURRENT_BLOCK" \
  --argjson total $((TOTAL + NEW_COUNT)) \
  '.last_checked_at=$ts | .last_block=$block | .total_revoke_calls=$total' \
  "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"

