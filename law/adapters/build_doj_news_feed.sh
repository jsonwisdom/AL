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

# Extract likely DOJ news links.
grep -Eo 'href="[^"]+"' "$TMP_HTML" \
  | sed 's/^href="//;s/"$//' \
  | grep -E '^/opa/pr/|^/usao-|^https://www.justice.gov/opa/pr/' \
  | sed 's#^/#https://www.justice.gov/#' \
  | sort -u \
  | head -n 50 > "$TMP_LINES"

COUNT="$(wc -l < "$TMP_LINES" | tr -d ' ')"
CANON="_truth/law/doj/doj_news_urls.canonical.txt"
cp "$TMP_LINES" "$CANON"

HASH="$(sha256sum "$CANON" | awk '{print $1}')"

PREV_HASH="INIT"
if [ -f "$STATE" ]; then
  PREV_HASH="$(jq -r '.hash // "INIT"' "$STATE")"
fi

if [ "$HASH" = "$PREV_HASH" ]; then
  STATUS="QUIET"
  REASON="no_new_doj_news_urls_detected"
else
  STATUS="ALERT"
  REASON="doj_news_url_set_changed"
fi

jq -n \
  --arg ts "$TS" \
  --arg url "$URL" \
  --arg hash "$HASH" \
  --arg prev_hash "$PREV_HASH" \
  --arg status "$STATUS" \
  --arg reason "$REASON" \
  --argjson count "$COUNT" \
  --rawfile urls "$CANON" \
  '{
    observer: "doj_news_adapter_v1",
    generated_at: $ts,
    source: $url,
    hash: $hash,
    previous_hash: $prev_hash,
    status: {
      visibility: (if $status == "ALERT" then "GREEN" else "GREEN" end),
      event: $status,
      reason: $reason
    },
    count: $count,
    urls: ($urls | split("\n") | map(select(length > 0)))
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"

jq -n \
  --arg ts "$TS" \
  --arg hash "$HASH" \
  --arg source "$URL" \
  '{updated_at:$ts, hash:$hash, source:$source}' > "$STATE.tmp"

mv "$STATE.tmp" "$STATE"

echo "$TS DOJ_ADAPTER_$STATUS hash=$HASH count=$COUNT reason=$REASON" | tee -a "$LOG"
