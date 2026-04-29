#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/alms_fetch_source.sh URL OUTPUT_DIR [expected_raw_hash]

expected_raw_hash format:
  sha256:<64 lowercase hex chars>
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then usage; exit 0; fi
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then echo "ALMS_FETCH_SOURCE_ERROR expected_url_output_dir_optional_hash" >&2; usage >&2; exit 2; fi

URL="$1"
OUT_DIR="$2"
EXPECTED_RAW_HASH="${3:-}"
mkdir -p "$OUT_DIR"

RAW_PATH="$OUT_DIR/source.bin"
TEXT_PATH="$OUT_DIR/source.txt"
HEADERS_PATH="$OUT_DIR/headers.txt"
MANIFEST_PATH="$OUT_DIR/source_manifest.json"
FETCHED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ -n "$EXPECTED_RAW_HASH" ] && ! printf '%s' "$EXPECTED_RAW_HASH" | grep -Eq '^sha256:[a-f0-9]{64}$'; then
  echo "ALMS_FETCH_SOURCE_ERROR invalid_expected_raw_hash expected=$EXPECTED_RAW_HASH" >&2
  exit 2
fi

if ! curl -L --fail --silent --show-error --max-time 30 -D "$HEADERS_PATH" "$URL" -o "$RAW_PATH"; then
  echo "ALMS_FETCH_SOURCE_FAIL source_fetch_failed url=$URL" >&2
  exit 1
fi

RAW_HASH="sha256:$(sha256sum "$RAW_PATH" | awk '{print $1}')"
INTEGRITY_STATUS="NO_EXPECTED_HASH"
if [ -n "$EXPECTED_RAW_HASH" ]; then
  if [ "$RAW_HASH" = "$EXPECTED_RAW_HASH" ]; then
    INTEGRITY_STATUS="VERIFIED"
  else
    INTEGRITY_STATUS="MISMATCH"
  fi
fi

CONTENT_TYPE=$(awk 'BEGIN{IGNORECASE=1} /^content-type:/ {print $0}' "$HEADERS_PATH" | tail -1 | sed 's/^[Cc]ontent-[Tt]ype:[[:space:]]*//' | tr -d '\r')
EXTRACT_STATUS="raw_text"
if printf '%s' "$CONTENT_TYPE" | grep -qi 'pdf'; then
  if command -v pdftotext >/dev/null 2>&1; then
    pdftotext -layout -nopgbrk "$RAW_PATH" "$TEXT_PATH" || { echo "ALMS_FETCH_SOURCE_FAIL source_extract_failed url=$URL" >&2; exit 1; }
    EXTRACT_STATUS="pdf_text"
  else
    echo "ALMS_FETCH_SOURCE_FAIL pdftotext_missing url=$URL" >&2
    exit 1
  fi
else
  tr -d '\000' < "$RAW_PATH" > "$TEXT_PATH"
fi

TEXT_HASH="sha256:$(sha256sum "$TEXT_PATH" | awk '{print $1}')"

jq -n \
  --arg url "$URL" --arg fetched_at "$FETCHED_AT" \
  --arg raw_path "$RAW_PATH" --arg text_path "$TEXT_PATH" \
  --arg raw_hash "$RAW_HASH" --arg expected_raw_hash "$EXPECTED_RAW_HASH" \
  --arg integrity_status "$INTEGRITY_STATUS" \
  --arg text_hash "$TEXT_HASH" --arg content_type "$CONTENT_TYPE" \
  --arg extract_status "$EXTRACT_STATUS" \
  '{fetcher_version:"alms_fetch_source_v1",url:$url,fetched_at:$fetched_at,raw_path:$raw_path,text_path:$text_path,raw_hash:$raw_hash,expected_raw_hash:($expected_raw_hash//""),integrity_status:$integrity_status,extracted_text_hash:$text_hash,content_type:$content_type,extract_status:$extract_status,status:"FETCHED"}' > "$MANIFEST_PATH"

cat "$MANIFEST_PATH"
