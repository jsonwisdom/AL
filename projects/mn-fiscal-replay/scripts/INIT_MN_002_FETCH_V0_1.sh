#!/bin/bash
# INIT_MN_002_FETCH_V0_1.sh
# Purpose: Initialize live fetch lane for MN_002.
# Doctrine: NO_FAKE_GREEN / no placeholder URL promotion.

set -euo pipefail

JURISDICTION="MN_002"
SOURCE_URL="${1:-}"

if [ -z "$SOURCE_URL" ]; then
  echo "BLOCKED_REASON: Missing official MN_002 source URL"
  echo "Usage: $0 https://official.gov/path/to/document.pdf"
  exit 1
fi

case "$SOURCE_URL" in
  https://mn.gov/*|https://www.mn.gov/*)
    ;;
  *)
    echo "BLOCKED_REASON: Source URL is not an official mn.gov URL"
    echo "SOURCE_URL=$SOURCE_URL"
    exit 1
    ;;
esac

TARGET_DIR="projects/mn-fiscal-replay/live_fetch/$JURISDICTION"
mkdir -p "$TARGET_DIR"

PDF_OUT="$TARGET_DIR/${JURISDICTION}_live.pdf"
TEXT_OUT="$TARGET_DIR/${JURISDICTION}_live_source.txt"
HEADERS_OUT="$TARGET_DIR/${JURISDICTION}_live_headers.txt"
RECEIPT_OUT="$TARGET_DIR/${JURISDICTION}_fetch_receipt.json"

echo "=== INITIALIZING $JURISDICTION FETCH ==="
echo "Source: $SOURCE_URL"
echo "Target: $TARGET_DIR"

curl -sS -L -D "$HEADERS_OUT" "$SOURCE_URL" -o "$PDF_OUT"

PDF_SHA=$(sha256sum "$PDF_OUT" | awk '{print $1}')
PDF_BYTES=$(wc -c < "$PDF_OUT" | tr -d ' ')
HEADER_SHA=$(sha256sum "$HEADERS_OUT" | awk '{print $1}')

python3 - "$PDF_OUT" "$TEXT_OUT" << 'PY'
import sys
from pathlib import Path
from pypdf import PdfReader

pdf = Path(sys.argv[1])
out = Path(sys.argv[2])

reader = PdfReader(str(pdf))
with out.open("w", encoding="utf-8") as f:
    for page in reader.pages:
        f.write((page.extract_text() or "") + "\n")
PY

TEXT_SHA=$(sha256sum "$TEXT_OUT" | awk '{print $1}')
TEXT_BYTES=$(wc -c < "$TEXT_OUT" | tr -d ' ')
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

jq -n \
  --arg id "$JURISDICTION" \
  --arg source_url "$SOURCE_URL" \
  --arg pdf "$PDF_OUT" \
  --arg text "$TEXT_OUT" \
  --arg headers "$HEADERS_OUT" \
  --arg pdf_sha "$PDF_SHA" \
  --arg text_sha "$TEXT_SHA" \
  --arg header_sha "$HEADER_SHA" \
  --arg pdf_bytes "$PDF_BYTES" \
  --arg text_bytes "$TEXT_BYTES" \
  --arg timestamp "$TS" \
  '{
    id: $id,
    source_url: $source_url,
    pdf_path: $pdf,
    text_path: $text,
    headers_path: $headers,
    pdf_sha256: $pdf_sha,
    extracted_text_sha256: $text_sha,
    headers_sha256: $header_sha,
    pdf_bytes: $pdf_bytes,
    extracted_text_bytes: $text_bytes,
    timestamp: $timestamp,
    status: "LIVE_FETCH_COMPLETE",
    next_step: "NORMALIZE_COMPARE_CHUNK_REVIEW",
    no_fake_green: true
  }' > "$RECEIPT_OUT"

cat "$RECEIPT_OUT" | jq .
echo "=== MN_002 fetch initialized ==="
