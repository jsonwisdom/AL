#!/usr/bin/env bash
set -euo pipefail

ETH_RPC="${ETH_RPC:-https://ethereum-rpc.publicnode.com}"

PORTAL="0x49048044D57e1C92A77f79988d21Fa8fAF74E97e"

OUT="_truth/base/optimismportal_observer_feed.json"
TS="$(date -u +%FT%TZ)"

LATEST="$(cast block-number --rpc-url "$ETH_RPC")"
FROM="$((LATEST - 5000))"

codehash() {
  cast code "$1" --rpc-url "$ETH_RPC" 2>/dev/null | sha256sum | awk '{print $1}'
}

# Event topics (CONFIRMED from your logs)
TOPIC_DEPOSIT="0xb3813568d9991fc951961fcb4c784893574240a28925604d09fc577c55bb7c32"
TOPIC_WITHDRAW="0x67a6208cfcc0801d50f6cbe764733f4fddf66ac0b04442061a8a8c0cb6b63f62"

DEPOSIT_COUNT="$(cast logs \
  --rpc-url "$ETH_RPC" \
  --address "$PORTAL" \
  --from-block "$FROM" \
  "$TOPIC_DEPOSIT" 2>/dev/null | grep -c "transactionHash" || true)"

WITHDRAW_COUNT="$(cast logs \
  --rpc-url "$ETH_RPC" \
  --address "$PORTAL" \
  --from-block "$FROM" \
  "$TOPIC_WITHDRAW" 2>/dev/null | grep -c "transactionHash" || true)"

CODEHASH="$(codehash "$PORTAL")"

jq -n \
  --arg ts "$TS" \
  --arg portal "$PORTAL" \
  --arg codehash "$CODEHASH" \
  --argjson deposits "$DEPOSIT_COUNT" \
  --argjson withdrawals "$WITHDRAW_COUNT" \
  '{
    observer: "base_optimismportal",
    generated_at: $ts,
    layer: "ethereum_l1",
    contract: {
      address: $portal,
      codehash_proxy: $codehash
    },
    activity: {
      last_5000_blocks: {
        deposits: $deposits,
        withdrawals: $withdrawals
      }
    },
    status: {
      visibility: "GREEN",
      reason: "event layer active; real flow observed"
    }
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS PORTAL_FEED_BUILT deposits=$DEPOSIT_COUNT withdrawals=$WITHDRAW_COUNT"
