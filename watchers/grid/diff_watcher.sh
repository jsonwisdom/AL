#!/usr/bin/env bash
set -euo pipefail

URL='https://www.whitehouse.gov/presidential-actions/2026/04/presidential-determination-pursuant-to-section-303-of-the-defense-production-act-of-1950-as-amended-on-grid-infrastructure-equipment-and-supply-chain-capacity/'
STATE_DIR="_truth/grid"
mkdir -p "$STATE_DIR"

NOW="$(date -u +%FT%TZ)"
CURRENT="$STATE_DIR/current.txt"
PREV="$STATE_DIR/previous.txt"
OUT="$STATE_DIR/diff_$(date -u +%Y%m%dT%H%M%SZ).json"

curl -Ls "$URL" \
  | sed 's/<script[^>]*>.*<\/script>//gI' \
  | sed 's/<style[^>]*>.*<\/style>//gI' \
  | sed 's/<[^>]*>/ /g' \
  | tr '\n\t' '  ' \
  | tr -s ' ' \
  | sed 's/^ *//;s/ *$//' > "$CURRENT"

CUR_HASH="$(sha256sum "$CURRENT" | cut -d' ' -f1)"
PREV_HASH=""
CHANGED=false

if [[ -f "$PREV" ]]; then
  PREV_HASH="$(sha256sum "$PREV" | cut -d' ' -f1)"
  [[ "$CUR_HASH" != "$PREV_HASH" ]] && CHANGED=true
fi

jq -n \
  --arg watcher "grid_diff" \
  --arg url "$URL" \
  --arg checked_at "$NOW" \
  --arg current_hash "$CUR_HASH" \
  --arg previous_hash "$PREV_HASH" \
  --arg changed "$CHANGED" \
  '{
    watcher: $watcher,
    source_url: $url,
    checked_at: $checked_at,
    current_hash: $current_hash,
    previous_hash: $previous_hash,
    changed: ($changed == "true")
  }' > "$OUT"

cp "$CURRENT" "$PREV"
cat "$OUT"
