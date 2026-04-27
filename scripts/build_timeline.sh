#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/timeline/timeline.json"
TMP="$(mktemp)"

FILES=(
  "_truth/logs/root_events.jsonl"
  "_truth/logs/multirun_events.jsonl"
  "_truth/tombstones/tombstones.jsonl"
)

> "$TMP"

for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    cat "$f" >> "$TMP"
  fi
done

# Build sorted JSON timeline
jq -s 'sort_by(.ts)' "$TMP" > "$OUT"

COUNT=$(jq 'length' "$OUT")

echo "TIMELINE_BUILT events=$COUNT file=$OUT"

rm -f "$TMP"
