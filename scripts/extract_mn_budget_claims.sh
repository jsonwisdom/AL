#!/usr/bin/env bash
set -euo pipefail

EXTRACT="${EXTRACT:-_truth/sources/mmb-feb-2026-forecast.txt}"
OUT="${OUT:-_truth/snapshots/mn_budget_claim_candidates.tsv}"

command -v awk >/dev/null 2>&1 || { echo "EXTRACT_FAIL reason=missing_awk" >&2; exit 2; }

test -f "$EXTRACT" || { echo "EXTRACT_FAIL reason=missing_extract path=$EXTRACT" >&2; exit 1; }
mkdir -p "$(dirname "$OUT")"

# Extract high-signal budget category rows from the MMB text extract.
# Output TSV: line_hint, category, primary_value, canonical_claim_text
awk '
  function trim(s){gsub(/^[[:space:]]+|[[:space:]]+$/, "", s); return s}
  function first_money(s, arr){ if (match(s, /[-]?[0-9][0-9,]+/, arr)) return arr[0]; return "" }
  /^[[:space:]]*(E-12 Education|Higher Education|Health & Human Services|Public Safety & Judiciary|Transportation|Environment)/ {
    raw=$0
    line_no=FNR
    label=raw
    sub(/[-]?[0-9][0-9,]+.*/, "", label)
    label=trim(label)
    val=first_money(raw)
    if (label != "" && val != "") {
      # Pad label to 55 chars to preserve a stable claim_text form.
      printf "%s\t%s\t%s\t%-55s%s\n", line_no, label, val, label, val
    }
  }
' "$EXTRACT" | LC_ALL=C sort -n > "$OUT"

count=$(wc -l < "$OUT" | tr -d ' ')
echo "EXTRACT_OK out=$OUT candidates=$count"
cat "$OUT"
