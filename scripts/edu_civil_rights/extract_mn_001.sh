#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 INPUT.pdf OUTPUT.json" >&2
  exit 64
fi

PDF="$1"
OUT="$2"

TMP_TXT=$(mktemp)
TMP_ROWS=$(mktemp)

cleanup() {
  rm -f "$TMP_TXT" "$TMP_ROWS"
}
trap cleanup EXIT

"$(dirname "$0")/pdf_to_text.sh" "$PDF" "$TMP_TXT"
python3 "$(dirname "$0")/table_extract.py" "$TMP_TXT" > "$TMP_ROWS"
python3 "$(dirname "$0")/normalize_json.py" < "$TMP_ROWS" | jq -S . > "$OUT"
