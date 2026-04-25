#!/usr/bin/env bash
set -euo pipefail

IN="law/manual/doj_receipts.jsonl"
OUT="_truth/law/doj/manual_doj_receipts_feed.json"
CANON="_truth/law/doj/manual_doj_receipts.canonical.jsonl"
LOG="_truth/logs/manual_doj_receipts.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/law/doj _truth/logs
touch "$IN"

jq -cS . "$IN" > "$CANON"

COUNT="$(wc -l < "$CANON" | tr -d ' ')"
HASH="$(sha256sum "$CANON" | awk '{print $1}')"

jq -n \
  --arg ts "$TS" \
  --arg hash "$HASH" \
  --argjson count "$COUNT" \
  --slurpfile receipts "$CANON" \
  '{
    observer:"manual_doj_receipts_v1",
    generated_at:$ts,
    source:"law/manual/doj_receipts.jsonl",
    count:$count,
    hash:$hash,
    status:{
      visibility:(if $count > 0 then "GREEN" else "YELLOW" end),
      reason:(if $count > 0 then "manual DOJ receipts normalized and hashed" else "manual receipt file exists but is empty" end)
    },
    receipts:$receipts
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS MANUAL_DOJ_RECEIPTS_BUILT count=$COUNT hash=$HASH" | tee -a "$LOG"
