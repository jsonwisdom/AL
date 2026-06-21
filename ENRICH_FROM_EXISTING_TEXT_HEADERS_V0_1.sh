#!/bin/bash
set -e

ENRICH_DIR="projects/mn-fiscal-replay/enriched"
mkdir -p "$ENRICH_DIR"

echo "=== MN Text/Headers Enrichment v0.1 ==="

for id in MN_001 MN_002; do
  echo "Processing $id..."

  SOURCE_TXT="_sources/$id/source.txt"
  HEADERS_TXT="_sources/$id/headers.txt"
  RECEIPT="_truth/receipts/$id.json"
  ENRICHED="$ENRICH_DIR/$id.enriched.json"

  RAW_HASH="RAW_PDF_MISSING"
  TEXT_HASH="TEXT_SOURCE_MISSING"
  TABLE_HASH="NO_TABLE"
  META_HASH="NO_METADATA"
  STATUS="TEXT_AND_HEADERS_BASELINE_ENRICHED"
  SOURCE_PATH="$SOURCE_TXT"

  if [ -f "$SOURCE_TXT" ]; then
    TEXT_HASH=$(projects/mn-fiscal-replay/scripts/hash_text_bytes.py "$SOURCE_TXT")
    echo "  → Hashed source.txt"
  else
    STATUS="TEXT_SOURCE_MISSING"
    SOURCE_PATH="TEXT_SOURCE_MISSING"
  fi

  if [ -f "$HEADERS_TXT" ]; then
    META_HASH=$(projects/mn-fiscal-replay/scripts/hash_text_bytes.py "$HEADERS_TXT")
    echo "  → Hashed headers.txt"
  fi

  if [ -f "$RECEIPT" ]; then
    cp "$RECEIPT" "$ENRICHED"
    jq --arg raw "$RAW_HASH" \
       --arg text "$TEXT_HASH" \
       --arg table "$TABLE_HASH" \
       --arg meta "$META_HASH" \
       --arg status "$STATUS" \
       --arg source_path "$SOURCE_PATH" \
       '.raw_pdf_sha256 = $raw |
        .normalized_pdf_text_sha256 = $text |
        .extracted_table_sha256 = $table |
        .http_metadata_sha256 = $meta |
        .source_path = $source_path |
        .baseline_status = $status' \
       "$ENRICHED" > "${ENRICHED}.tmp" && mv "${ENRICHED}.tmp" "$ENRICHED"
    echo "  → Enriched receipt created"
  else
    echo "  → BLOCKED_REASON: No original receipt for $id"
  fi
done

echo ""
echo "=== Enrichment complete ==="
ls -la "$ENRICH_DIR"
