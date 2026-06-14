#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/alerts/alerts.jsonl"
SUMMARY="_truth/alerts/alerts_summary.json"
TMP="$(mktemp)"
OUT_TMP="$(mktemp)"
mkdir -p _truth/alerts

FILES=(
  "_truth/logs/root_events.jsonl"
  "_truth/logs/multirun_events.jsonl"
  "_truth/tombstones/tombstones.jsonl"
)

> "$TMP"
> "$OUT_TMP"

# === SAFE LOAD + COMPACT ===
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    jq -c . "$f" 2>/dev/null >> "$TMP" || true
  fi
done

INFO=0
WATCH=0
ALERT=0
TOTAL=0

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

  TOTAL=$((TOTAL + 1))

  jq -c -n \
    --arg ts "$(echo "$line" | jq -r '.ts // ""')" \
    --arg type "$TYPE" \
    --arg severity "$SEVERITY" \
    --argjson raw "$line" \
    '{
      ts:$ts,
      type:$type,
      severity:$severity,
      raw:$raw
    }' >> "$OUT_TMP"

done < "$TMP"

# Important: rewrite, do not append forever. The old behavior grew alerts.jsonl past GitHub's 100MB limit.
mv "$OUT_TMP" "$OUT"

jq -n -cS \
  --arg ts "$(date -u +%FT%TZ)" \
  --arg status "ALERT_ESCALATION_SUMMARY" \
  --arg source "$OUT" \
  --arg policy "alerts_jsonl_runtime_only_not_committed" \
  --argjson total "$TOTAL" \
  --argjson alert "$ALERT" \
  --argjson watch "$WATCH" \
  --argjson info "$INFO" \
  '{ts:$ts,status:$status,source:$source,policy:$policy,total:$total,alert:$alert,watch:$watch,info:$info}' > "$SUMMARY"

echo "ALERT_ESCALATION_DONE alert=$ALERT watch=$WATCH info=$INFO total=$TOTAL"

rm -f "$TMP"