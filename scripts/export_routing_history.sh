#!/usr/bin/env bash
set -euo pipefail

IN="${1:-_truth/routing/history.jsonl}"
OUT="${2:-docs/routing-history.json}"

command -v jq >/dev/null 2>&1 || { echo "EXPORT_FAIL reason=missing_jq" >&2; exit 2; }

if [ ! -f "$IN" ]; then
  mkdir -p "$(dirname "$OUT")"
  printf '[]\n' > "$OUT"
  echo "EXPORT_OK records=0 out=$OUT"
  exit 0
fi

mkdir -p "$(dirname "$OUT")"
jq -s '.' "$IN" > "$OUT"
COUNT="$(jq 'length' "$OUT")"
echo "EXPORT_OK records=$COUNT out=$OUT"
