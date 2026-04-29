#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%Y%m%dT%H%M%SZ)"
BASE="_truth/infra_watch"
RUN="$BASE/runs/$TS"
ARCH="$BASE/archive"
SNAP_BASE="$BASE/snapshots"
LATEST="$BASE/latest.json"

mkdir -p "$RUN" "$ARCH" "$SNAP_BASE"

UA="ALMS-Infra-Watcher/0.4 (+jaywisdom.base.eth; audit monitor)"

URLS=(
  "https://aws.amazon.com/bedrock/pricing/"
  "https://aws.amazon.com/bedrock/sla/"
  "https://aws.amazon.com/bedrock/"
  "https://openai.com/pricing"
  "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/"
  "https://azure.microsoft.com/en-us/support/legal/sla/cognitive-services/"
)

RAW="$RUN/raw.jsonl"
CANON="$RUN/canonical.jsonl"
: > "$RAW"

PARENT_HASH="GENESIS"
[ -f "$LATEST" ] && PARENT_HASH="$(jq -r '.run_hash // "GENESIS"' "$LATEST")"

for URL in "${URLS[@]}"; do
  ID="$(printf "%s" "$URL" | sha256sum | cut -d' ' -f1)"
  BODY="$RUN/$ID.html"
  HDR="$RUN/$ID.headers"

  CODE="$(curl -sSL --compressed \
    -A "$UA" \
    -H "Cache-Control: no-cache" \
    -H "Pragma: no-cache" \
    -D "$HDR" \
    -o "$BODY" \
    -w "%{http_code}" \
    "$URL" || echo "000")"

  HASH="$(sha256sum "$BODY" | cut -d' ' -f1)"
  SIZE="$(wc -c < "$BODY" | tr -d ' ')"

  FETCH_OK="true"
  if [ "$CODE" != "200" ] || [ "$SIZE" -lt 5000 ]; then FETCH_OK="false"; fi
  if grep -qiE 'access denied|captcha|blocked|cloudfront error|request blocked|enable javascript' "$BODY"; then FETCH_OK="false"; fi

  jq -ncS \
    --arg url "$URL" \
    --arg http_code "$CODE" \
    --arg sha256 "$HASH" \
    --arg bytes "$SIZE" \
    --arg fetch_ok "$FETCH_OK" \
    --arg fetched_at "$TS" \
    '{url:$url,http_code:($http_code|tonumber),sha256:$sha256,bytes:($bytes|tonumber),fetch_ok:($fetch_ok=="true"),fetched_at:$fetched_at}' \
    >> "$RAW"
done

jq -cS . "$RAW" | LC_ALL=C sort > "$CANON"
RUN_HASH="$(sha256sum "$CANON" | cut -d' ' -f1)"
BAD_FETCHES="$(jq -s '[.[] | select(.fetch_ok==false)] | length' "$CANON")"

DIFF_STATUS="GENESIS"
DIFF_HASH="NONE"

if [ -f "$LATEST" ]; then
  PREV_RUN="$(jq -r '.run_id // empty' "$LATEST")"
  PREV="$BASE/runs/$PREV_RUN/canonical.jsonl"
  if [ -f "$PREV" ]; then
    if cmp -s "$PREV" "$CANON"; then
      DIFF_STATUS="UNCHANGED"
    else
      DIFF_STATUS="CHANGED"
      diff -u "$PREV" "$CANON" > "$RUN/diff.patch" || true
      DIFF_HASH="$(sha256sum "$RUN/diff.patch" | cut -d' ' -f1)"
      cp "$CANON" "$ARCH/${TS}_changed.jsonl"
      SNAP="$SNAP_BASE/$TS"
      mkdir -p "$SNAP"
      cp "$RUN"/*.html "$RUN"/*.headers "$SNAP/" 2>/dev/null || true
    fi
  fi
fi

jq -ncS \
  --arg leaf_id "OPENAI_AWS_001" \
  --arg type "INFRA_WATCH" \
  --arg watcher_version "0.4" \
  --arg run_id "$TS" \
  --arg run_hash "$RUN_HASH" \
  --arg parent_run_hash "$PARENT_HASH" \
  --arg diff_status "$DIFF_STATUS" \
  --arg diff_sha256 "$DIFF_HASH" \
  --arg bad_fetches "$BAD_FETCHES" \
  '{leaf_id:$leaf_id,type:$type,watcher_version:$watcher_version,run_id:$run_id,run_hash:$run_hash,parent_run_hash:$parent_run_hash,diff_status:$diff_status,diff_sha256:$diff_sha256,bad_fetches:($bad_fetches|tonumber)}' \
  > "$RUN/receipt.json"

cp "$RUN/receipt.json" "$BASE/latest.tmp"
mv "$BASE/latest.tmp" "$LATEST"

echo "ALMS_INFRA_WATCH_V0.4 run_id=$TS run_hash=$RUN_HASH diff_status=$DIFF_STATUS bad_fetches=$BAD_FETCHES"
