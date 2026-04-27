#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/root_history/root_history.jsonl"

NOW="$(date -u +%FT%TZ)"
ROOT="$(jq -r '.root_sha256' _truth/root/alms_root.json)"
MERKLE="$(jq -r '.merkle_root // "UNKNOWN"' merkle_proofs.json 2>/dev/null || echo "UNKNOWN")"

ENTRY=$(jq -cS -n \
  --arg t "$NOW" \
  --arg r "$ROOT" \
  --arg m "$MERKLE" \
  '{
    ts: $t,
    root_sha256: $r,
    merkle_root: $m
  }')

echo "$ENTRY" >> "$OUT"

echo "ROOT_HISTORY_APPEND $NOW"
