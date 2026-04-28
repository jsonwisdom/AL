#!/usr/bin/env bash
set -euo pipefail

EXTRACT="${EXTRACT:-_truth/sources/mmb-feb-2026-forecast.txt}"
OUT="${OUT:-_truth/snapshots/mn_budget_claim_candidates.tsv}"

test -f "$EXTRACT" || { echo "EXTRACT_FAIL reason=missing_extract path=$EXTRACT" >&2; exit 1; }
mkdir -p "$(dirname "$OUT")"

awk '
  function trim(s){gsub(/^[[:space:]]+|[[:space:]]+$/, "", s); return s}
  function emit(label, raw, line_no) {
    rest=raw
    sub("^[[:space:]]*" label, "", rest)
    sub(/^[[:space:]]+/, "", rest)
    split(rest, parts, /[[:space:]]+/)
    val=parts[1]
    if (val ~ /^[0-9][0-9,]+$/) {
      printf "%s\t%s\t%s\t%-55s%s\n", line_no, label, val, label, val
    }
  }
  /^[[:space:]]*E-12 Education[[:space:]]+[0-9]/ { emit("E-12 Education", $0, FNR) }
  /^[[:space:]]*Higher Education[[:space:]]+[0-9]/ { emit("Higher Education", $0, FNR) }
  /^[[:space:]]*Health & Human Services[[:space:]]+[0-9]/ { emit("Health & Human Services", $0, FNR) }
  /^[[:space:]]*Public Safety & Judiciary[[:space:]]+[0-9]/ { emit("Public Safety & Judiciary", $0, FNR) }
  /^[[:space:]]*Transportation[[:space:]]+[0-9]/ { emit("Transportation", $0, FNR) }
  /^[[:space:]]*Environment and Energy[[:space:]]+[0-9]/ { emit("Environment and Energy", $0, FNR) }
' "$EXTRACT" | LC_ALL=C sort -n > "$OUT"

count="$(wc -l < "$OUT" | tr -d " ")"
echo "EXTRACT_OK out=$OUT candidates=$count"
cat "$OUT"
