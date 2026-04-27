#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/root_history/root_history.jsonl"
TMP="$(mktemp)"

NOW="$(date -u +%FT%TZ)"
ROOT="$(jq -r '.root_sha256' _truth/root/alms_root.json)"
MERKLE="$(jq -r '.merkle_root // "UNKNOWN"' merkle_proofs.json 2>/dev/null || echo "UNKNOWN")"

# previous hash
if [ -f "$OUT" ] && [ -s "$OUT" ]; then
  PREV_HASH="$(tail -n 1 "$OUT" | jq -r '.entry_hash')"
else
  PREV_HASH="GENESIS"
fi

# canonical entry (without entry_hash)
ENTRY_CANON=$(jq -cS -n \
  --arg t "$NOW" \
  --arg r "$ROOT" \
  --arg m "$MERKLE" \
  --arg p "$PREV_HASH" \
  '{
    ts: $t,
    root_sha256: $r,
    merkle_root: $m,
    prev_entry_hash: $p
  }')

ENTRY_HASH=$(printf '%s' "$ENTRY_CANON" | sha256sum | awk '{print $1}')

# final entry
jq -cS -n \
  --argjson base "$ENTRY_CANON" \
  --arg h "$ENTRY_HASH" \
  '$base + {entry_hash: $h}' > "$TMP"

cat "$TMP" >> "$OUT"
rm -f "$TMP"

echo "ROOT_HISTORY_CHAIN_APPEND $ENTRY_HASH"
