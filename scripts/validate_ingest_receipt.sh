#!/usr/bin/env bash
set -euo pipefail

# Validate ingest artifact against recorded SHA and meta
# Usage: validate_ingest_receipt.sh <html_file> <expected_sha>

FILE="${1:-}"
EXPECTED_SHA="${2:-}"

if [ -z "$FILE" ] || [ -z "$EXPECTED_SHA" ]; then
  echo "Usage: $0 <html_file> <expected_sha>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "FILE_NOT_FOUND"
  exit 1
fi

ACTUAL_SHA=$(sha256sum "$FILE" | awk '{print $1}')

if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then
  echo "INGEST_SHA_MISMATCH"
  echo "EXPECTED=$EXPECTED_SHA"
  echo "ACTUAL=$ACTUAL_SHA"
  exit 1
fi

SIZE=$(wc -c < "$FILE" | tr -d ' ')

echo "INGEST_VALID"
echo "FILE=$FILE"
echo "SIZE_BYTES=$SIZE"
echo "SHA256=$ACTUAL_SHA"
echo "NOTE=Quarantined ingest validated. Not promoted."
