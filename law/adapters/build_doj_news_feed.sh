#!/usr/bin/env bash
set -euo pipefail

URL="${DOJ_NEWS_URL:-https://www.justice.gov/news}"
OUT="_truth/law/doj/doj_news_feed.json"
STATE="_truth/law/doj/doj_news_state.json"
LOG="_truth/logs/doj_news_adapter.log"
TS="$(date -u +%FT%TZ)"

mkdir -p _truth/law/doj _truth/logs

TMP_HTML="$(mktemp)"
TMP_LINES="$(mktemp)"
trap 'rm -f "$TMP_HTML" "$TMP_LINES"' EXIT

curl -fsSL "$URL" -o "$TMP_HTML"

grep -Eo 'href="[^"]+"' "$TMP_HTML" \
  | sed 's/^href="//;s/"$//' \
  | grep -E '/opa/pr/|/usao-' || true \
  | sed 's#^/#https://www.justice.gov/#' \
  | sort -u \
  | head -n 50 > "$TMP_LINES"

COUNT="$(wc -l < "$TMP_LINES" | tr -d ' ')"
CANON="_truth/law/doj/doj_news_urls.canonical.txt"
cp "$TMP_LINES" "$CANON"

HASH="$(sha256sum "$CANON" | awk '{print $1}')"
PREV_HASH="INIT"
[ -f "$STATE" ] && PREV_HASH="$(jq -r '.hash // "INIT"' "$STATE")"

if [ "$COUNT" = "0" ]; then
  EVENT="EMPTY"
  VISIBILITY="YELLOW"
  REASON="source fetched but no DOJ news URLs matched extractor"
elif [ "$HASH" = "$PREV_HASH" ]; then
  EVENT="QUIET"
  VISIBILITY="GREEN"
  REASON="no_new_doj_news_urls_detected"
else
  EVENT="ALERT"
  VISIBILITY="GREEN"
  REASON="doj_news_url_set_changed"
fi

jq -n \
  --arg ts "$TS" \
  --arg source "$URL" \
  --arg hash "$HASH" \
  --arg prev_hash "$PREV_HASH" \
  --arg event "$EVENT" \
  --arg visibility "$VISIBILITY" \
  --arg reason "$REASON" \
  --argjson count "$COUNT" \
  --rawfile urls "$CANON" \
  '{
    observer:"doj_news_adapter_v1",
    generated_at:$ts,
    source:$source,
    hash:$hash,
    previous_hash:$prev_hash,
    status:{visibility:$visibility,event:$event,reason:$reason},
    count:$count,
    urls:($urls | split("\n") | map(select(length > 0)))
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"

jq -n --arg ts "$TS" --arg hash "$HASH" --arg source "$URL" \
  '{updated_at:$ts, hash:$hash, source:$source}' > "$STATE.tmp"
mv "$STATE.tmp" "$STATE"

echo "$TS DOJ_ADAPTER_$EVENT visibility=$VISIBILITY hash=$HASH count=$COUNT reason=$REASON" | tee -a "$LOG"
