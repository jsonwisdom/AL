#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — EXTRACTOR V1
# PURPOSE: Deterministically extract minimal claim text from HTML
# RULE: No NLP, no heuristics, no inference

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <input_url>" >&2
  exit 2
fi

INPUT_URL="$1"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# 1. Fetch raw HTML. No JS, cookies, or rendering.
HTML_CONTENT="$(curl -Ls "$INPUT_URL")"

# 2. Extract <title>.
TITLE="$(printf '%s' "$HTML_CONTENT" \
  | tr '\n' ' ' \
  | grep -oiP '<title[^>]*>.*?</title>' \
  | head -n 1 \
  | sed -E 's/<\/?title[^>]*>//Ig' \
  | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"

# 3. Extract <meta name="description">.
META_DESC="$(printf '%s' "$HTML_CONTENT" \
  | tr '\n' ' ' \
  | grep -oiP '<meta[^>]+name=["'"'"']description["'"'"'][^>]*>' \
  | head -n 1 \
  | sed -nE 's/.*content=["'"'"']([^"'"'"']*)["'"'"'].*/\1/Ip' \
  | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"

# 4. Extract first <p> fallback.
FIRST_P="$(printf '%s' "$HTML_CONTENT" \
  | tr '\n' ' ' \
  | grep -oiP '<p[^>]*>.*?</p>' \
  | head -n 1 \
  | sed -E 's/<[^>]+>//g' \
  | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"

# 5. Select claim_excerpt by fixed priority: title → meta description → first paragraph.
if [ -n "$TITLE" ]; then
  CLAIM_EXCERPT="$TITLE"
elif [ -n "$META_DESC" ]; then
  CLAIM_EXCERPT="$META_DESC"
else
  CLAIM_EXCERPT="$FIRST_P"
fi

# 6. Emit canonical JSON.
jq -n -cS \
  --arg claim_excerpt "$CLAIM_EXCERPT" \
  --arg source_url "$INPUT_URL" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  '{claim_excerpt:$claim_excerpt,source_url:$source_url,timestamp_utc:$timestamp_utc}'
