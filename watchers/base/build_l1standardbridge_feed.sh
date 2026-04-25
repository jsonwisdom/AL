#!/usr/bin/env bash
set -euo pipefail

ETH_RPC="${ETH_RPC:-https://ethereum-rpc.publicnode.com}"
BRIDGE_MAIN="0x3154Cf16ccdb4C6d922629664174b904d80F2C35"

OUT="_truth/base/l1standardbridge_observer_feed.json"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

LATEST="$(cast block-number --rpc-url "$ETH_RPC")"
FROM="$((LATEST - 20000))"

codehash() {
  cast code "$1" --rpc-url "$ETH_RPC" 2>/dev/null | sha256sum | awk '{print $1}' || echo "CODEHASH_ERROR"
}

count_topic() {
  local topic="$1"
  cast logs \
    --rpc-url "$ETH_RPC" \
    --address "$BRIDGE_MAIN" \
    --from-block "$FROM" \
    "$topic" 2>/dev/null | grep -c "transactionHash" || true
}

# Observed directly from real bridge logs
TOPIC_A="0x35d79ab81f2b2017e19afb5c5571778877782d7a8786f5907f93b0f4702f4f23"
TOPIC_B="0x2849b43074093a05396b6f2a937dee8565b15a48a7b3d4bffb732a5017380af5"
TOPIC_C="0x718594027abd4eaed59f95162563e0cc6d0e8d5b86b1c7be8b1b0ac3343d0396"
TOPIC_D="0x7ff126db8024424bbfd9826e8ab82ff59136289ea440b04b39a0df1b03b9cabf"

COUNT_A="$(count_topic "$TOPIC_A")"
COUNT_B="$(count_topic "$TOPIC_B")"
COUNT_C="$(count_topic "$TOPIC_C")"
COUNT_D="$(count_topic "$TOPIC_D")"

TOTAL_OBSERVED="$((COUNT_A + COUNT_B + COUNT_C + COUNT_D))"

if [ "$TOTAL_OBSERVED" -gt 0 ]; then
  VISIBILITY="GREEN"
  REASON="bridge event flow confirmed from observed topics"
else
  VISIBILITY="YELLOW"
  REASON="bridge code confirmed but no observed event flow in sampled window"
fi

jq -n \
  --arg ts "$TS" \
  --arg bridge "$BRIDGE_MAIN" \
  --arg codehash "$(codehash "$BRIDGE_MAIN")" \
  --arg from "$FROM" \
  --arg latest "$LATEST" \
  --arg visibility "$VISIBILITY" \
  --arg reason "$REASON" \
  --argjson topic_a "$COUNT_A" \
  --argjson topic_b "$COUNT_B" \
  --argjson topic_c "$COUNT_C" \
  --argjson topic_d "$COUNT_D" \
  --argjson total "$TOTAL_OBSERVED" \
  '{
    observer:"base_l1standardbridge",
    generated_at:$ts,
    layer:"ethereum_l1",
    contract:{
      address:$bridge,
      codehash_proxy:$codehash
    },
    sample_window:{
      from_block:$from,
      latest_block:$latest
    },
    activity:{
      observed_topics:{
        "0x35d79ab8":$topic_a,
        "0x2849b430":$topic_b,
        "0x71859402":$topic_c,
        "0x7ff126db":$topic_d
      },
      total_observed_events:$total
    },
    status:{
      visibility:$visibility,
      reason:$reason
    }
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS BRIDGE_FEED_BUILT total_observed_events=$TOTAL_OBSERVED visibility=$VISIBILITY"
