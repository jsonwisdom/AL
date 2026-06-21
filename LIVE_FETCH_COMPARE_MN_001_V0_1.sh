#!/bin/bash
# LIVE_FETCH_COMPARE_MN_001_V0_1.sh
# Real live fetch + compare against sealed MN_001 enriched baseline.
# NO_FAKE_GREEN: requires real URL, exits on fetch/extract failure.

set -e

LIVE_URL="${1:-}"
BASELINE="projects/mn-fiscal-replay/enriched/MN_001.enriched.json"
LIVE_DIR="projects/mn-fiscal-replay/live_fetch/MN_001"

if [ -z "$LIVE_URL" ]; then
  echo "BLOCKED_REASON: Missing live PDF URL argument"
  exit 1
fi

if [[ "$LIVE_URL" == *"XXXXXX"* ]] || [[ "$LIVE_URL" != http* ]]; then
  echo "BLOCKED_REASON: Placeholder or invalid URL"
  exit 1
fi

if [ ! -f "$BASELINE" ]; then
  echo "BLOCKED_REASON: Missing sealed baseline: $BASELINE"
  exit 1
fi

mkdir -p "$LIVE_DIR"

PDF_FILE="$LIVE_DIR/MN_001_live.pdf"
HEADERS_FILE="$LIVE_DIR/MN_001_live_headers.txt"
TEXT_FILE="$LIVE_DIR/MN_001_live_source.txt"
CURRENT_JSON="$LIVE_DIR/MN_001.current.enriched.json"
COMPARE_RECEIPT="$LIVE_DIR/MN_001.live_compare.json"

echo "=== LIVE_FETCH_COMPARE_MN_001_V0_1 ==="
echo "URL: $LIVE_URL"

echo "Fetching live headers..."
curl -I -L "$LIVE_URL" > "$HEADERS_FILE" 2>&1 || {
  echo "BLOCKED_REASON: HEADERS_FETCH_FAILED"
  exit 1
}

echo "Fetching live PDF..."
curl -L -f -o "$PDF_FILE" "$LIVE_URL" || {
  echo "BLOCKED_REASON: PDF_FETCH_FAILED"
  exit 1
}

RAW_HASH=$(sha256sum "$PDF_FILE" | awk '{print $1}')
META_HASH=$(projects/mn-fiscal-replay/scripts/hash_text_bytes.py "$HEADERS_FILE")

echo "Extracting text..."
if command -v pdftotext >/dev/null 2>&1; then
  pdftotext "$PDF_FILE" "$TEXT_FILE"
  EXTRACTION_METHOD="pdftotext"
else
  python3 - "$PDF_FILE" "$TEXT_FILE" <<'PY'
import sys
from pypdf import PdfReader
pdf_path, out_path = sys.argv[1], sys.argv[2]
reader = PdfReader(pdf_path)
text = ""
for page in reader.pages:
    text += page.extract_text() or ""
with open(out_path, "w", encoding="utf-8") as f:
    f.write(text)
PY
  EXTRACTION_METHOD="pypdf"
fi

TEXT_HASH=$(projects/mn-fiscal-replay/scripts/hash_text_bytes.py "$TEXT_FILE")

jq \
  --arg raw "$RAW_HASH" \
  --arg text "$TEXT_HASH" \
  --arg meta "$META_HASH" \
  --arg source "$LIVE_URL" \
  --arg method "$EXTRACTION_METHOD" \
  '.raw_pdf_sha256 = $raw |
   .normalized_pdf_text_sha256 = $text |
   .http_metadata_sha256 = $meta |
   .source_path = $source |
   .live_extraction_method = $method |
   .baseline_status = "LIVE_FETCH_CURRENT_ENRICHED"' \
  "$BASELINE" > "$CURRENT_JSON"

RESULT=$(projects/mn-fiscal-replay/scripts/compare_receipts.py "$BASELINE" "$CURRENT_JSON")
echo "$RESULT"

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

jq -n \
  --arg id "MN_001" \
  --arg url "$LIVE_URL" \
  --arg baseline "$BASELINE" \
  --arg current "$CURRENT_JSON" \
  --arg result "$RESULT" \
  --arg raw_hash "$RAW_HASH" \
  --arg text_hash "$TEXT_HASH" \
  --arg meta_hash "$META_HASH" \
  --arg method "$EXTRACTION_METHOD" \
  --arg timestamp "$TS" \
  '{
    id: $id,
    url: $url,
    baseline: $baseline,
    current: $current,
    result: $result,
    raw_pdf_sha256: $raw_hash,
    normalized_pdf_text_sha256: $text_hash,
    http_metadata_sha256: $meta_hash,
    extraction_method: $method,
    timestamp: $timestamp,
    status: "LIVE_COMPARE_COMPLETE"
  }' > "$COMPARE_RECEIPT"

echo "Live compare receipt: $COMPARE_RECEIPT"
echo "NO_FAKE_GREEN maintained."
