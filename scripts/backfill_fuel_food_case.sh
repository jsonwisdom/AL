#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CASE_DIR="$ROOT/data/backfill/fuel_food_2021_2022"
OUT_DIR="$ROOT/_truth/backfill"
LOG="$ROOT/_truth/logs/backfill_fuel_food.log"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ID="fuel_food_2021_2022_$(date -u +"%Y%m%dT%H%M%SZ")"

mkdir -p "$OUT_DIR" "$(dirname "$LOG")"

MANIFEST="$CASE_DIR/source_manifest.json"
RAW="$OUT_DIR/${ID}_raw.json"
LEAF="$OUT_DIR/${ID}_leaf.json"

jq -cS \
  --arg ts "$TS" \
  '{
    timestamp_utc: $ts,
    case_id: .case_id,
    model: .model,
    hypothesis: .hypothesis,
    windows: .windows,
    sources: .sources,
    validation_rule: {
      edge_1_or_2_RED: true,
      edge_3_drop_within_days: [14,45],
      edge_4_drop_within_days: [90,180],
      edge_5_price_shock_within_days: [120,210],
      result: "sequence_match_required"
    },
    status: "BACKFILL_CASE_DEFINED"
  }' "$MANIFEST" > "$RAW"

HASH="$(jq -cS . "$RAW" | sha256sum | awk '{print $1}')"

cat > "$LEAF" <<JSON
{
  "leaf_id": "$ID",
  "model": "backfill_lag_validation_leaf_v0.1",
  "timestamp_utc": "$TS",
  "case": "fuel_food_2021_2022",
  "canonical_hash_sha256": "$HASH",
  "raw_path": "$RAW",
  "status": "CAPTURED",
  "next": "ingest_public_time_series"
}
JSON

echo "BACKFILL_CASE_OK ts=$TS hash=$HASH leaf=$LEAF" | tee -a "$LOG"
