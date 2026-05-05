#!/usr/bin/env bash
set -euo pipefail

URL="https://www.justice.gov/epstein"
OUT_DIR="_truth/ingest/justice_epstein"
TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "$OUT_DIR"

RAW_HTML="$OUT_DIR/${TS}.html"
HASH_FILE="$OUT_DIR/${TS}.sha256"
META_FILE="$OUT_DIR/${TS}.meta.json"
HEADER_FILE="$OUT_DIR/${TS}.headers.txt"

# Fetch raw response body plus headers. No parsing, no promotion, no claims.
HTTP_STATUS=$(curl -sS -L \
  -D "$HEADER_FILE" \
  -o "$RAW_HTML" \
  -w '%{http_code}' \
  "$URL")

FINAL_URL=$(curl -sS -L -o /dev/null -w '%{url_effective}' "$URL")

# Compute hash over raw response body bytes.
SHA256=$(sha256sum "$RAW_HTML" | awk '{print $1}')
SIZE_BYTES=$(wc -c < "$RAW_HTML" | tr -d ' ')
echo "$SHA256  $(basename "$RAW_HTML")" > "$HASH_FILE"

# Write metadata only. This is quarantined ingest, not canonical promotion.
cat > "$META_FILE" <<JSON
{
  "source": "justice_epstein",
  "url": "$URL",
  "final_url": "$FINAL_URL",
  "http_status": "$HTTP_STATUS",
  "fetched_at_utc": "${TS}",
  "file": "$(basename "$RAW_HTML")",
  "headers_file": "$(basename "$HEADER_FILE")",
  "size_bytes": ${SIZE_BYTES},
  "sha256": "${SHA256}",
  "custody_stage": "INGEST_ONLY_QUARANTINED",
  "promotion_status": "NOT_PROMOTED",
  "note": "Raw fetch only. Not canonical. Does not create WRITE_RUN_0002_packet.json."
}
JSON

echo "FETCH_OK"
echo "HTTP_STATUS=$HTTP_STATUS"
echo "FINAL_URL=$FINAL_URL"
echo "FILE=$RAW_HTML"
echo "SIZE_BYTES=$SIZE_BYTES"
echo "SHA256=$SHA256"
echo "META=$META_FILE"
