#!/usr/bin/env bash
set -euo pipefail

CONTRACT="0x08e49F31Ab11b17f3a5BaA36e6744E9B532bC87B"
OUT="_truth/base/nitro_observer_feed.json"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

live_revoker() {
  local rpc="$1"
  local raw
  raw="$(cast call "$CONTRACT" 0x35dec5d1 --rpc-url "$rpc" 2>/dev/null || echo "READ_ERROR")"

  if [[ "$raw" == 0x* && ${#raw} -ge 42 ]]; then
    echo "0x${raw: -40}"
  else
    echo "$raw"
  fi
}

REV_MAIN="$(live_revoker https://mainnet.base.org)"
REV_SEP="$(live_revoker https://sepolia.base.org)"

jq -n \
  --arg ts "$TS" \
  --arg contract "$CONTRACT" \
  --arg rev_main "$REV_MAIN" \
  --arg rev_sep "$REV_SEP" \
  --slurpfile me "_truth/base/nitro_event_base-mainnet.json" \
  --slurpfile se "_truth/base/nitro_event_base-sepolia.json" \
  --slurpfile mc "_truth/base/nitro_calls_base-mainnet.json" \
  --slurpfile sc "_truth/base/nitro_calls_base-sepolia.json" \
  '{
    observer:"base_nitro_enclave_verifier",
    generated_at:$ts,
    contract:$contract,
    networks:{
      base_mainnet:{
        revoker_event_state:$me[0],
        revoker_live:$rev_main,
        revoke_call_state:$mc[0]
      },
      base_sepolia:{
        revoker_event_state:$se[0],
        revoker_live:$rev_sep,
        revoke_call_state:$sc[0]
      }
    },
    status:{
      role_visibility:true,
      live_revoker_visibility:true,
      action_visibility:true,
      alerting:true
    }
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS FEED_BUILT $OUT"
