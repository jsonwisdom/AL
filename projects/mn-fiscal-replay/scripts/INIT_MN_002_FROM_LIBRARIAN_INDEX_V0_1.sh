#!/bin/bash
# INIT_MN_002_FROM_LIBRARIAN_INDEX_V0_1.sh
# Purpose: initialize MN_002 from Librarian Index, not manual URL.
# Doctrine: DISCOVERY_BEFORE_DELEGATION / NO_FAKE_GREEN.

set -euo pipefail

INDEX="projects/mn-fiscal-replay/librarian/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_2.json"
JURISDICTION="MN_002"
TARGET_DIR="projects/mn-fiscal-replay/live_fetch/$JURISDICTION"

echo "=== INIT $JURISDICTION FROM LIBRARIAN INDEX ==="

if [ ! -f "$INDEX" ]; then
  echo "BLOCKED_REASON: Missing Librarian index: $INDEX"
  exit 1
fi

SOURCE_URL=$(jq -r --arg id "$JURISDICTION" '.components[$id].source_url // empty' "$INDEX")
SOURCE_MANIFEST=$(jq -r --arg id "$JURISDICTION" '.components[$id].source_manifest // empty' "$INDEX")
REPLAY_RECEIPT=$(jq -r --arg id "$JURISDICTION" '.components[$id].replay_receipt // empty' "$INDEX")
ENRICHED_BASELINE=$(jq -r --arg id "$JURISDICTION" '.components[$id].enriched_baseline // empty' "$INDEX")

if [ -z "$SOURCE_URL" ]; then
  echo "BLOCKED_REASON: Librarian index missing source_url for $JURISDICTION"
  exit 1
fi

if [ -z "$SOURCE_MANIFEST" ] || [ ! -f "$SOURCE_MANIFEST" ]; then
  echo "BLOCKED_REASON: Librarian index points to missing source manifest"
  echo "SOURCE_MANIFEST=$SOURCE_MANIFEST"
  exit 1
fi

case "$SOURCE_URL" in
  https://mn.gov/*|https://www.mn.gov/*)
    ;;
  *)
    echo "BLOCKED_REASON: Source URL is not official mn.gov"
    echo "SOURCE_URL=$SOURCE_URL"
    exit 1
    ;;
esac

mkdir -p "$TARGET_DIR"

PDF_OUT="$TARGET_DIR/${JURISDICTION}_live.pdf"
HEADERS_OUT="$TARGET_DIR/${JURISDICTION}_live_headers.txt"
TEXT_OUT="$TARGET_DIR/${JURISDICTION}_live_source.txt"
NORMALIZED_OUT="$TARGET_DIR/${JURISDICTION}_live_normalized.txt"
RECEIPT_OUT="$TARGET_DIR/${JURISDICTION}_librarian_fetch_normalize_receipt.json"

echo "Source URL: $SOURCE_URL"
echo "Source manifest: $SOURCE_MANIFEST"
echo "Replay receipt: $REPLAY_RECEIPT"
echo "Enriched baseline: $ENRICHED_BASELINE"

curl -sS -L -D "$HEADERS_OUT" "$SOURCE_URL" -o "$PDF_OUT"

PDF_BYTES=$(wc -c < "$PDF_OUT" | tr -d ' ')
if [ "$PDF_BYTES" -lt 1000 ]; then
  echo "BLOCKED_REASON: Fetched file too small to be trusted as target PDF"
  echo "PDF_BYTES=$PDF_BYTES"
  exit 1
fi

PDF_SHA=$(sha256sum "$PDF_OUT" | awk '{print $1}')
HEADERS_SHA=$(sha256sum "$HEADERS_OUT" | awk '{print $1}')

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

python3 - "$TEXT_OUT" "$NORMALIZED_OUT" << 'PY'
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])

text = src.read_text(encoding="utf-8", errors="replace")
text = re.sub(r"\s+", " ", text).strip()
dst.write_text(text + "\n", encoding="utf-8")
PY

TEXT_SHA=$(sha256sum "$TEXT_OUT" | awk '{print $1}')
NORMALIZED_SHA=$(sha256sum "$NORMALIZED_OUT" | awk '{print $1}')
TEXT_BYTES=$(wc -c < "$TEXT_OUT" | tr -d ' ')
NORMALIZED_BYTES=$(wc -c < "$NORMALIZED_OUT" | tr -d ' ')
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

jq -n \
  --arg id "$JURISDICTION" \
  --arg timestamp "$TS" \
  --arg source_url "$SOURCE_URL" \
  --arg source_manifest "$SOURCE_MANIFEST" \
  --arg replay_receipt "$REPLAY_RECEIPT" \
  --arg enriched_baseline "$ENRICHED_BASELINE" \
  --arg pdf_path "$PDF_OUT" \
  --arg headers_path "$HEADERS_OUT" \
  --arg text_path "$TEXT_OUT" \
  --arg normalized_path "$NORMALIZED_OUT" \
  --arg pdf_sha256 "$PDF_SHA" \
  --arg headers_sha256 "$HEADERS_SHA" \
  --arg text_sha256 "$TEXT_SHA" \
  --arg normalized_sha256 "$NORMALIZED_SHA" \
  --arg pdf_bytes "$PDF_BYTES" \
  --arg text_bytes "$TEXT_BYTES" \
  --arg normalized_bytes "$NORMALIZED_BYTES" \
  '{
    id: $id,
    timestamp: $timestamp,
    status: "LIBRARIAN_INDEX_FETCH_NORMALIZE_COMPLETE",
    source: {
      source_url: $source_url,
      source_manifest: $source_manifest,
      replay_receipt: $replay_receipt,
      enriched_baseline: $enriched_baseline
    },
    outputs: {
      pdf_path: $pdf_path,
      headers_path: $headers_path,
      text_path: $text_path,
      normalized_path: $normalized_path
    },
    hashes: {
      pdf_sha256: $pdf_sha256,
      headers_sha256: $headers_sha256,
      extracted_text_sha256: $text_sha256,
      normalized_text_sha256: $normalized_sha256
    },
    byte_counts: {
      pdf_bytes: $pdf_bytes,
      extracted_text_bytes: $text_bytes,
      normalized_text_bytes: $normalized_bytes
    },
    public_content_claim: "BLOCKED",
    next_step: "MN_002_CHUNK_DIFF_AND_CLASSIFY",
    manual_operator_file_search_required: false,
    no_fake_green: true
  }' > "$RECEIPT_OUT"

cat "$RECEIPT_OUT" | jq .
echo "=== COMPLETE: $JURISDICTION librarian fetch + normalize ==="
