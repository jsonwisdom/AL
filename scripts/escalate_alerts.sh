#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/alerts/alerts.jsonl"
TMP="$(mktemp)"

FILES=(
  "_truth/logs/root_events.jsonl"
  "_truth/logs/multirun_events.jsonl"
  "_truth/tombstones/tombstones.jsonl"
)

> "$TMP"

# === SAFE LOAD + COMPACT ===
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    jq -c . "$f" 2>/dev/null >> "$TMP" || true
  fi
done

INFO=0
WATCH=0
ALERT=0

while IFS= read -r line; do
  # skip empty lines
  [ -z "$line" ] && continue

  TYPE=$(echo "$line" | jq -r '.type // ""')
  CHANGE=$(echo "$line" | jq -r '.change_type // ""')
  STATUS=$(echo "$line" | jq -r '.status // ""')

  SEVERITY="INFO"

  if [[ "$CHANGE" == "ROOT_MUTATION" || "$STATUS" == "MULTIRUN_ALERT" ]]; then
    SEVERITY="ALERT"
    ALERT=$((ALERT + 1))
  elif [[ "$CHANGE" == "FILESET_CHANGE" || "$TYPE" == "TOMBSTONE" ]]; then
    SEVERITY="WATCH"
    WATCH=$((WATCH + 1))
  else
    SEVERITY="INFO"
    INFO=$((INFO + 1))
  fi

  jq -n \
    --arg ts "$(echo "$line" | jq -r '.ts')" \
    --arg type "$TYPE" \
    --arg severity "$SEVERITY" \
    --argjson raw "$line" \
    '{
      ts:$ts,
      type:$type,
      severity:$severity,
      raw:$raw
    }' >> "$OUT"

done < "$TMP"

echo "ALERT_ESCALATION_DONE alert=$ALERT watch=$WATCH info=$INFO"

rm -f "$TMP"
