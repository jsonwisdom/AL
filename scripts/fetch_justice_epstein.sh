#!/usr/bin/env bash
set -euo pipefail

URL="https://www.justice.gov/epstein"
OUT_DIR="_truth/ingest/justice_epstein"
TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "$OUT_DIR"

RAW_HTML="$OUT_DIR/${TS}.html"
HASH_FILE="$OUT_DIR/${TS}.sha256"
META_FILE="$OUT_DIR/${TS}.meta.json"

# Fetch bytes (no transformation)
curl -sS "$URL" -o "$RAW_HTML"

# Compute hash over raw bytes
SHA256=$(sha256sum "$RAW_HTML" | awk '{print $1}')
echo "$SHA256  $(basename "$RAW_HTML")" > "$HASH_FILE"

# Write minimal metadata (no promotion, no claims)
cat > "$META_FILE" <<JSON
{
  "source": "justice_epstein",
  "url": "$URL",
  "fetched_at_utc": "${TS}",
  "file": "$(basename "$RAW_HTML")",
  "sha256": "${SHA256}",
  "note": "Raw fetch only. Not canonical. Not promoted."
}
JSON

echo "FETCH_OK"
echo "FILE=$RAW_HTML"
echo "SHA256=$SHA256"
echo "META=$META_FILE"
