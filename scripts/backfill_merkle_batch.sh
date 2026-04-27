#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$ROOT/_truth/backfill"
LOG="$ROOT/_truth/logs/backfill_merkle.log"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ID="backfill_merkle_$(date -u +"%Y%m%dT%H%M%SZ")"
OUT="$DIR/${ID}.json"

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

find "$DIR" -type f -name '*_leaf.json' | sort | while read -r f; do
  jq -cS . "$f" | sha256sum | awk -v file="$f" '{print "{\"file\":\"" file "\",\"hash\":\"" $1 "\"}"}'
done > "$TMP"

COUNT="$(wc -l < "$TMP" | tr -d ' ')"
[ "$COUNT" -gt 0 ] || { echo "BACKFILL_MERKLE_FAIL no_leaves" | tee -a "$LOG"; exit 1; }

ROOT_HASH="$(jq -s -cS . "$TMP" | sha256sum | awk '{print $1}')"

jq -s \
  --arg ts "$TS" \
  --arg id "$ID" \
  --arg root "$ROOT_HASH" \
  --arg count "$COUNT" \
  '{
    batch_id: $id,
    model: "backfill_merkle_batch_v0.1",
    timestamp_utc: $ts,
    leaf_count: ($count|tonumber),
    merkle_root_sha256: $root,
    leaves: .
  }' "$TMP" > "$OUT"

echo "BACKFILL_MERKLE_OK ts=$TS count=$COUNT root=$ROOT_HASH out=$OUT" | tee -a "$LOG"
