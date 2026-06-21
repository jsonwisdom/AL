#!/usr/bin/env bash
# Boss Bre runner v0.2: source ingest + statewide PDF scanner + jurisdiction forensic sweep.
# Doctrine: NO_FAKE_GREEN. Logs observations and receipts only; no public claim promotion.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
JFILE="$ROOT/data/mn_jurisdictions.json"
WORKER="$ROOT/scripts/mn001_forensic_worker_v0_1.sh"
SCANNER="$ROOT/scripts/boss_bre_pdf_scanner.sh"
INGEST="$ROOT/scripts/boss_bre_fetch_extract_v0_1.sh"

if [ ! -f "$JFILE" ]; then
  echo "BLOCKED_REASON: missing jurisdiction registry: $JFILE"
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "BLOCKED_REASON: jq is required"
  exit 1
fi
chmod +x "$WORKER" 2>/dev/null || true
chmod +x "$SCANNER" 2>/dev/null || true
chmod +x "$INGEST" 2>/dev/null || true

git config user.name "github-actions[bot]" || true
git config user.email "41898282+github-actions[bot]@users.noreply.github.com" || true

echo "=== Boss Bre Agent 00: source ingest + baseline rotation ==="
if [ -x "$INGEST" ]; then
  "$INGEST" || echo "INGEST_BLOCKED: continuing with scanner and jurisdiction receipts"
else
  echo "INGEST_MISSING: $INGEST"
fi

echo "=== Boss Bre Agent 01: PDF scan + learning state ==="
if [ -x "$SCANNER" ]; then
  "$SCANNER" || echo "SCANNER_BLOCKED: continuing with jurisdiction receipts"
else
  echo "SCANNER_MISSING: $SCANNER"
fi

echo "=== Boss Bre Agent 02: jurisdiction forensic sweep ==="
jq -c '.jurisdictions[]' "$JFILE" | while IFS= read -r J; do
  CODE="$(echo "$J" | jq -r '.code')"
  NAME="$(echo "$J" | jq -r '.name')"
  TYPE="$(echo "$J" | jq -r '.type')"
  PDF="$(echo "$J" | jq -r '.pdf_url // empty')"
  OUTDIR="$ROOT/projects/mn-fiscal-replay/live_fetch/$CODE"

  echo "=== Boss Bre sweep: $CODE | $TYPE | $NAME ==="
  mkdir -p "$OUTDIR"

  if [ -z "$PDF" ] || echo "$PDF" | grep -q '^TODO_'; then
    echo "FETCH_BLOCKED: missing real source PDF URL for $CODE" > "$OUTDIR/fetch_status.txt"
  elif [ -f "$OUTDIR/source_latest.pdf" ]; then
    echo "SOURCE_PDF_PRESENT: source_latest.pdf" > "$OUTDIR/fetch_status.txt"
  else
    echo "SOURCE_URL_REGISTERED: $PDF" > "$OUTDIR/fetch_status.txt"
    echo "FETCH_BLOCKED: ingest did not produce source_latest.pdf" >> "$OUTDIR/fetch_status.txt"
  fi

  JURISDICTION="$CODE" "$WORKER" "$ROOT" || true
  git add "$OUTDIR" || true
done

echo "=== Boss Bre Agent 03: stage scanner and learning artifacts ==="
git add "$ROOT/projects/mn-fiscal-replay/boss_bre" || true

if git diff --cached --quiet; then
  echo "Boss Bre: no receipt changes to commit"
else
  git commit -m "Boss Bre: 15m PDF sweep $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  git push || true
fi
