#!/usr/bin/env bash
# =============================================================================
# ALMS External Source Fetcher v1
# Fetches an external URL, hashes raw bytes, extracts text when possible, and
# emits deterministic metadata for source_integrity + source_match.
#
# Scope v1:
#   - curl URL fetch
#   - sha256 raw bytes
#   - sha256 extracted text
#   - PDF extraction via pdftotext when available
#   - text/html/plain fallback as raw UTF-8 text
# =============================================================================

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/alms_fetch_source.sh URL OUTPUT_DIR

Outputs:
  OUTPUT_DIR/source.bin
  OUTPUT_DIR/source.txt
  OUTPUT_DIR/source_manifest.json
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -ne 2 ]; then
  echo "ALMS_FETCH_SOURCE_ERROR expected_url_and_output_dir" >&2
  usage >&2
  exit 2
fi

URL="$1"
OUT_DIR="$2"
mkdir -p "$OUT_DIR"

RAW_PATH="$OUT_DIR/source.bin"
TEXT_PATH="$OUT_DIR/source.txt"
MANIFEST_PATH="$OUT_DIR/source_manifest.json"
HEADERS_PATH="$OUT_DIR/headers.txt"

FETCHED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if ! curl -L --fail --silent --show-error --max-time 30 -D "$HEADERS_PATH" "$URL" -o "$RAW_PATH"; then
  echo "ALMS_FETCH_SOURCE_FAIL source_fetch_failed url=$URL" >&2
  exit 1
fi

RAW_HASH="sha256:$(sha256sum "$RAW_PATH" | awk '{print $1}')"
CONTENT_TYPE=$(awk 'BEGIN{IGNORECASE=1} /^content-type:/ {print $0}' "$HEADERS_PATH" | tail -1 | sed 's/^[Cc]ontent-[Tt]ype:[[:space:]]*//' | tr -d '\r')

EXTRACT_STATUS="raw_text"
if printf '%s' "$CONTENT_TYPE" | grep -qi 'pdf'; then
  if command -v pdftotext >/dev/null 2>&1; then
    if pdftotext -layout -nopgbrk "$RAW_PATH" "$TEXT_PATH"; then
      EXTRACT_STATUS="pdf_text"
    else
      echo "ALMS_FETCH_SOURCE_FAIL source_extract_failed url=$URL" >&2
      exit 1
    fi
  else
    echo "ALMS_FETCH_SOURCE_FAIL pdftotext_missing url=$URL" >&2
    exit 1
  fi
else
  # v1 fallback: treat fetched bytes as text. Strip NUL bytes for text tools.
  tr -d '\000' < "$RAW_PATH" > "$TEXT_PATH"
fi

TEXT_HASH="sha256:$(sha256sum "$TEXT_PATH" | awk '{print $1}')"

jq -n \
  --arg url "$URL" \
  --arg fetched_at "$FETCHED_AT" \
  --arg raw_path "$RAW_PATH" \
  --arg text_path "$TEXT_PATH" \
  --arg raw_hash "$RAW_HASH" \
  --arg text_hash "$TEXT_HASH" \
  --arg content_type "$CONTENT_TYPE" \
  --arg extract_status "$EXTRACT_STATUS" \
  '{
    fetcher_version: "alms_fetch_source_v1",
    url: $url,
    fetched_at: $fetched_at,
    raw_path: $raw_path,
    text_path: $text_path,
    raw_hash: $raw_hash,
    extracted_text_hash: $text_hash,
    content_type: $content_type,
    extract_status: $extract_status,
    status: "FETCHED"
  }' > "$MANIFEST_PATH"

cat "$MANIFEST_PATH"
