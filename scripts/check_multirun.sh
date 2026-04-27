#!/usr/bin/env bash
set -euo pipefail

LOG="_truth/logs/execution.log"
OUT="_truth/logs/multirun_events.jsonl"

SCRIPT="${1:-auto_root.sh}"
WINDOW_SECONDS="${2:-300}"
THRESHOLD="${3:-3}"

if [ ! -f "$LOG" ]; then
  echo "NO_LOG_FOUND"
  exit 0
fi

NOW=$(date -u +%s)

COUNT=0

# === SCAN LOG ===
while IFS= read -r line; do
  TS=$(echo "$line" | awk '{print $1}')
  NAME=$(echo "$line" | awk '{print $3}')

  if [ "$NAME" != "$SCRIPT" ]; then
    continue
  fi

  TS_EPOCH=$(date -u -d "$TS" +%s 2>/dev/null || echo 0)

  if [ "$TS_EPOCH" -eq 0 ]; then
    continue
  fi

  AGE=$((NOW - TS_EPOCH))

  if [ "$AGE" -le "$WINDOW_SECONDS" ]; then
    COUNT=$((COUNT + 1))
  fi
done < "$LOG"

# === CLASSIFY ===
STATUS="MULTIRUN_OK"

if [ "$COUNT" -gt "$THRESHOLD" ]; then
  STATUS="MULTIRUN_ALERT"
fi

echo "$STATUS script=$SCRIPT count=$COUNT window=${WINDOW_SECONDS}s threshold=$THRESHOLD"

# === LOG EVENT ===
jq -n \
  --arg ts "$(date -u +%FT%TZ)" \
  --arg script "$SCRIPT" \
  --arg status "$STATUS" \
  --arg count "$COUNT" \
  --arg window "$WINDOW_SECONDS" \
  --arg threshold "$THRESHOLD" \
  '{
    ts:$ts,
    type:"MULTIRUN_CHECK",
    script:$script,
    status:$status,
    count:($count|tonumber),
    window_seconds:($window|tonumber),
    threshold:($threshold|tonumber)
  }' >> "$OUT"

