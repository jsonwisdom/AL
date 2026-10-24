#!/usr/bin/env bash
# ZTVS fetch stage — contained repair v0.1
# Missing source URL or config => HOLD. Never invents a URL. Never writes VERIFIED.
set -euo pipefail

CONFIG="${1:-}"
OUT_DIR="${2:-registry/MN_001}"
RECEIPT="$OUT_DIR/fetch_receipt.json"

mkdir -p "$OUT_DIR"

write_hold() {
  local reason="$1"
  jq -n --arg reason "$reason" --arg utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{stage:"fetch",status:"HOLD",reason:$reason,utc:$utc,verified:false,no_fake_green:true}' \
    > "$RECEIPT"
  echo "HOLD: $reason"
  echo "Receipt: $RECEIPT"
  exit 2
}

if [ -z "$CONFIG" ] || [ ! -f "$CONFIG" ]; then
  write_hold "MISSING_CONFIG"
fi

URL=$(jq -r '.url // empty' "$CONFIG" 2>/dev/null || true)
if [ -z "$URL" ] || [ "$URL" = "null" ] || [ "$URL" = "HOLD" ]; then
  write_hold "MISSING_SOURCE_URL"
fi

# Delegate to existing fetcher only when a real URL is present.
if [ ! -x scripts/alms_fetch_source.sh ] && [ ! -f scripts/alms_fetch_source.sh ]; then
  write_hold "FETCHER_MISSING"
fi

bash scripts/alms_fetch_source.sh "$URL" "$OUT_DIR" || write_hold "FETCH_FAILED"

# alms_fetch_source writes source.bin; ZTVS expects raw.pdf. Copy only if fetch succeeded.
if [ -f "$OUT_DIR/source.bin" ]; then
  cp "$OUT_DIR/source.bin" "$OUT_DIR/raw.pdf"
fi

jq -n --arg utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg url "$URL" \
  '{stage:"fetch",status:"FETCHED",url:$url,utc:$utc,verified:false,no_fake_green:true,note:"fetch succeeded; authenticity not yet established"}' \
  > "$RECEIPT"
echo "FETCHED (not verified): $RECEIPT"
