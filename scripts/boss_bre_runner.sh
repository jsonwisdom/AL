#!/usr/bin/env bash
# Boss Bre runner: sweep configured Minnesota jurisdictions.
# Doctrine: NO_FAKE_GREEN. This runner commits receipts only; it never promotes a public claim.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
JFILE="$ROOT/data/mn_jurisdictions.json"
WORKER="$ROOT/scripts/mn001_forensic_worker_v0_1.sh"

if [ ! -f "$JFILE" ]; then
  echo "BLOCKED_REASON: missing jurisdiction registry: $JFILE"
  exit 1
fi
if [ ! -x "$WORKER" ]; then
  chmod +x "$WORKER"
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "BLOCKED_REASON: jq is required"
  exit 1
fi

git config user.name "github-actions[bot]" || true
git config user.email "41898282+github-actions[bot]@users.noreply.github.com" || true

jq -c '.jurisdictions[]' "$JFILE" | while IFS= read -r J; do
  CODE="$(echo "$J" | jq -r '.code')"
  NAME="$(echo "$J" | jq -r '.name')"
  TYPE="$(echo "$J" | jq -r '.type')"
  PDF="$(echo "$J" | jq -r '.pdf_url // empty')"
  OUTDIR="$ROOT/projects/mn-fiscal-replay/live_fetch/$CODE"

  echo "=== Boss Bre sweep: $CODE | $TYPE | $NAME ==="
  mkdir -p "$OUTDIR"

  # Fetch/normalize is intentionally not faked here. A lane goes blocked until real baseline/live or diff payloads exist.
  if [ -z "$PDF" ] || echo "$PDF" | grep -q '^TODO_'; then
    echo "FETCH_BLOCKED: missing real source PDF URL for $CODE" > "$OUTDIR/fetch_status.txt"
  else
    echo "SOURCE_URL_REGISTERED: $PDF" > "$OUTDIR/fetch_status.txt"
    echo "FETCH_NOT_IMPLEMENTED_IN_BOSS_BRE_V0_1: wire real extractor before promotion" >> "$OUTDIR/fetch_status.txt"
  fi

  JURISDICTION="$CODE" "$WORKER" "$ROOT" || true

  git add "$OUTDIR" || true
done

if git diff --cached --quiet; then
  echo "Boss Bre: no receipt changes to commit"
else
  git commit -m "Boss Bre: 15m sweep $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  git push || true
fi
