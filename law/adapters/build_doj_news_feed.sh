#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/law/doj/doj_news_feed.json"
STATE="_truth/law/doj/doj_news_state.json"
LOG="_truth/logs/doj_news_adapter.log"
TS="$(date -u +%FT%TZ)"
mkdir -p _truth/law/doj _truth/logs

CANON="_truth/law/doj/doj_news_urls.canonical.txt"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

: > "$TMP"

for page in 1 2 3 4 5; do
  curl -fsSL "https://www.justice.gov/sitemap.xml?page=$page" \
    | grep -Eo '<loc>https://www.justice.gov/(opa/pr|usao-[^<]+)[^<]*</loc>' \
    | sed 's#<loc>##;s#</loc>##' >> "$TMP" || true
done

sort -u "$TMP" | head -n 100 > "$CANON"
COUNT="$(wc -l < "$CANON" | tr -d ' ')"
HASH="$(sha256sum "$CANON" | awk '{print $1}')"
PREV_HASH="INIT"
[ -f "$STATE" ] && PREV_HASH="$(jq -r '.hash // "INIT"' "$STATE")"

if [ "$COUNT" = "0" ]; then
  EVENT="EMPTY"; VISIBILITY="YELLOW"; REASON="sitemap fetched but no DOJ release URLs matched"
elif [ "$HASH" = "$PREV_HASH" ]; then
  EVENT="QUIET"; VISIBILITY="GREEN"; REASON="no_new_doj_release_urls_detected"
else
  EVENT="ALERT"; VISIBILITY="GREEN"; REASON="doj_release_url_set_changed"
fi

jq -n \
  --arg ts "$TS" --arg hash "$HASH" --arg prev "$PREV_HASH" \
  --arg event "$EVENT" --arg visibility "$VISIBILITY" --arg reason "$REASON" \
  --argjson count "$COUNT" --rawfile urls "$CANON" \
  '{
    observer:"doj_sitemap_adapter_v1",
    generated_at:$ts,
    source:"https://www.justice.gov/sitemap.xml?page=1..5",
    hash:$hash,
    previous_hash:$prev,
    status:{visibility:$visibility,event:$event,reason:$reason},
    count:$count,
    urls:($urls|split("\n")|map(select(length>0)))
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
jq -n --arg ts "$TS" --arg hash "$HASH" '{updated_at:$ts,hash:$hash}' > "$STATE.tmp"
mv "$STATE.tmp" "$STATE"

echo "$TS DOJ_SITEMAP_$EVENT visibility=$VISIBILITY count=$COUNT hash=$HASH" | tee -a "$LOG"
