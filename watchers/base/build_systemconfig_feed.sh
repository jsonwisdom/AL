#!/usr/bin/env bash
set -euo pipefail

CONTRACT_MAIN="0x73a79Fab69143498Ed3712e519A88a918e1f4072"
CONTRACT_SEP="0xf272670eb55e895584501d564AfEB048bEd26194"

OUT="_truth/base/systemconfig_observer_feed.json"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

[ -f _truth/base/systemconfig_event_mainnet.json ] || echo '{"last_event":"UNKNOWN","events":0}' > _truth/base/systemconfig_event_mainnet.json
[ -f _truth/base/systemconfig_event_sepolia.json ] || echo '{"last_event":"UNKNOWN","events":0}' > _truth/base/systemconfig_event_sepolia.json

live_call() {
  local rpc="$1"
  local contract="$2"
  local selector="$3"
  cast call "$contract" "$selector" --rpc-url "$rpc" 2>/dev/null || echo "REVERT_OR_MISSING"
}

code_hash() {
  local rpc="$1"
  local contract="$2"
  cast code "$contract" --rpc-url "$rpc" 2>/dev/null | cast keccak 2>/dev/null || echo "CODE_READ_ERROR"
}

OWNER_MAIN="$(live_call https://mainnet.base.org "$CONTRACT_MAIN" 0x8da5cb5b)"
OWNER_SEP="$(live_call https://sepolia.base.org "$CONTRACT_SEP" 0x8da5cb5b)"

CODEHASH_MAIN="$(code_hash https://mainnet.base.org "$CONTRACT_MAIN")"
CODEHASH_SEP="$(code_hash https://sepolia.base.org "$CONTRACT_SEP")"

jq -n \
  --arg ts "$TS" \
  --arg cmain "$CONTRACT_MAIN" \
  --arg csep "$CONTRACT_SEP" \
  --arg owner_main "$OWNER_MAIN" \
  --arg owner_sep "$OWNER_SEP" \
  --arg codehash_main "$CODEHASH_MAIN" \
  --arg codehash_sep "$CODEHASH_SEP" \
  --slurpfile events_main "_truth/base/systemconfig_event_mainnet.json" \
  --slurpfile events_sep "_truth/base/systemconfig_event_sepolia.json" \
  '{
    observer:"base_systemconfig",
    generated_at:$ts,
    networks:{
      base_mainnet:{
        address:$cmain,
        owner_live:$owner_main,
        code_hash:$codehash_main,
        event_state:$events_main[0]
      },
      base_sepolia:{
        address:$csep,
        owner_live:$owner_sep,
        code_hash:$codehash_sep,
        event_state:$events_sep[0]
      }
    },
    status:{
      live_owner_visibility:($owner_main!="REVERT_OR_MISSING" and $owner_sep!="REVERT_OR_MISSING"),
      codehash_visibility:($codehash_main!="CODE_READ_ERROR" and $codehash_sep!="CODE_READ_ERROR"),
      alerting:false
    }
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS FEED_BUILT $OUT"
