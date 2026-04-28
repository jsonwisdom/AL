#!/usr/bin/env bash
set -euo pipefail

EXTRACT="${EXTRACT:-_truth/sources/mmb-feb-2026-forecast.txt}"
OUT="${OUT:-_truth/snapshots/mn_budget_claim_candidates.tsv}"

test -f "$EXTRACT" || { echo "EXTRACT_FAIL reason=missing_extract path=$EXTRACT" >&2; exit 1; }
mkdir -p "$(dirname "$OUT")"

awk '
  function trim(s){gsub(/^[[:space:]]+|[[:space:]]+$/, "", s); return s}
  /^[[:space:]]*(E-12 Education|Higher Education|Health & Human Services|Public Safety & Judiciary|Transportation|Environment)/ {
    raw=$0
    line_no=FNR
    label=raw
    sub(/[-]?[0-9][0-9,]+.*/, "", label)
    label=trim(label)

    rest=raw
    sub(label, "", rest)
    sub(/^[[:space:]]+/, "", rest)
    split(rest, parts, /[[:space:]]+/)
    val=parts[1]

    if (label != "" && val ~ /^-?[0-9][0-9,]+$/) {
      printf "%s\t%s\t%s\t%-55s%s\n", line_no, label, val, label, val
    }
  }
' "$EXTRACT" | LC_ALL=C sort -n > "$OUT"

count="$(wc -l < "$OUT" | tr -d " ")"
echo "EXTRACT_OK out=$OUT candidates=$count"
cat "$OUT"
