#!/usr/bin/env bash
set -euo pipefail

MONTH="${1:-$(date -u +%Y-%m)}"
ROOT="_truth/ledger"
OUT="$ROOT/$MONTH.jsonl"
mkdir -p "$ROOT"

: > "$OUT"

find _truth/receipts -maxdepth 1 -type f -name 'CLAIM_*.json' | LC_ALL=C sort | while read -r f; do
  claim_id="$(jq -r '.claim_id' "$f")"
  ts="$(jq -r '.timestamp_utc' "$f")"
  actor="$(jq -r '.actor' "$f")"
  verdict="$(jq -r '.verdict' "$f")"
  sha256="$(sha256sum "$f" | awk '{print $1}')"
  bytes="$(wc -c < "$f" | tr -d ' ')"

  case "$ts" in
    "$MONTH"-*) ;;
    *) continue ;;
  esac

  jq -cn \
    --arg ts "$ts" \
    --arg claim_id "$claim_id" \
    --arg path "$f" \
    --arg sha256 "$sha256" \
    --arg actor "$actor" \
    --arg verdict "$verdict" \
    --argjson bytes "$bytes" \
    '{ts:$ts, claim_id:$claim_id, path:$path, sha256:$sha256, bytes:$bytes, actor:$actor, verdict:$verdict}'
done > "$OUT"

LEDGER_HASH="$(sha256sum "$OUT" | awk '{print $1}')"
COUNT="$(wc -l < "$OUT" | tr -d ' ')"

echo "ALMS_LEDGER_BUILD_OK month=$MONTH count=$COUNT ledger=$OUT ledger_sha256=$LEDGER_HASH"
