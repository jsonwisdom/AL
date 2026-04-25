#!/usr/bin/env bash
set -euo pipefail

FEED="_truth/base/optimismportal_observer_feed.json"
STATE="_truth/base/optimismportal_alert_state.json"
LOG="_truth/logs/optimismportal_alerts.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/base _truth/logs

if [ ! -f "$FEED" ]; then
  echo "$TS ERROR missing feed: $FEED" | tee -a "$LOG"
  exit 1
fi

CURRENT_VISIBILITY="$(jq -r '.status.visibility // "UNKNOWN"' "$FEED")"
CURRENT_REASON="$(jq -r '.status.reason // "no reason"' "$FEED")"
CURRENT_DEPOSITS="$(jq -r '.activity.last_5000_blocks.deposits // 0' "$FEED")"
CURRENT_WITHDRAWALS="$(jq -r '.activity.last_5000_blocks.withdrawals // 0' "$FEED")"
CURRENT_CODEHASH="$(jq -r '.contract.codehash_proxy // "UNKNOWN"' "$FEED")"

if [ -f "$STATE" ]; then
  PREV_VISIBILITY="$(jq -r '.visibility // "UNKNOWN"' "$STATE")"
  PREV_CODEHASH="$(jq -r '.codehash_proxy // "UNKNOWN"' "$STATE")"
else
  PREV_VISIBILITY="INIT"
  PREV_CODEHASH="INIT"
fi

ALERT="false"
WHY=""

if [ "$CURRENT_VISIBILITY" != "$PREV_VISIBILITY" ]; then
  ALERT="true"
  WHY="visibility_change:$PREV_VISIBILITY->$CURRENT_VISIBILITY"
fi

if [ "$CURRENT_CODEHASH" != "$PREV_CODEHASH" ]; then
  ALERT="true"
  WHY="${WHY:+$WHY;}codehash_change"
fi

jq -n \
  --arg ts "$TS" \
  --arg visibility "$CURRENT_VISIBILITY" \
  --arg reason "$CURRENT_REASON" \
  --argjson deposits "$CURRENT_DEPOSITS" \
  --argjson withdrawals "$CURRENT_WITHDRAWALS" \
  --arg codehash "$CURRENT_CODEHASH" \
  '{
    updated_at: $ts,
    visibility: $visibility,
    reason: $reason,
    deposits_last_5000_blocks: $deposits,
    withdrawals_last_5000_blocks: $withdrawals,
    codehash_proxy: $codehash
  }' > "$STATE.tmp"

mv "$STATE.tmp" "$STATE"

if [ "$ALERT" = "true" ]; then
  echo "$TS ALERT optimismportal $WHY visibility=$CURRENT_VISIBILITY deposits=$CURRENT_DEPOSITS withdrawals=$CURRENT_WITHDRAWALS" | tee -a "$LOG"
else
  echo "$TS QUIET optimismportal unchanged visibility=$CURRENT_VISIBILITY deposits=$CURRENT_DEPOSITS withdrawals=$CURRENT_WITHDRAWALS" | tee -a "$LOG"
fi
