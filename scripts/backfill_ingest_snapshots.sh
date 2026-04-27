#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAP="$ROOT/data/backfill/fuel_food_2021_2022/snapshots"
OUT="$ROOT/_truth/backfill"
LOG="$ROOT/_truth/logs/backfill_ingest.log"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ID="ingest_$(date -u +"%Y%m%dT%H%M%SZ")"

mkdir -p "$OUT"

RAW="$OUT/${ID}_raw.json"
LEAF="$OUT/${ID}_leaf.json"

jq -n \
  --arg ts "$TS" \
  --arg diesel "$(cat $SNAP/diesel.csv)" \
  --arg planting "$(cat $SNAP/planting.csv)" \
  --arg harvest "$(cat $SNAP/harvest.csv)" \
  --arg cpi "$(cat $SNAP/cpi.csv)" \
  '{
    timestamp_utc: $ts,
    model: "backfill_ingest_v0.1",
    data: {
      diesel: $diesel,
      planting: $planting,
      harvest: $harvest,
      cpi: $cpi
    }
  }' > "$RAW"

HASH="$(jq -cS . "$RAW" | sha256sum | awk '{print $1}')"

cat > "$LEAF" <<JSON
{
  "leaf_id": "$ID",
  "model": "backfill_ingest_leaf_v0.1",
  "timestamp_utc": "$TS",
  "canonical_hash_sha256": "$HASH",
  "raw_path": "$RAW",
  "status": "CAPTURED"
}
JSON

echo "BACKFILL_INGEST_OK ts=$TS hash=$HASH" | tee -a "$LOG"
