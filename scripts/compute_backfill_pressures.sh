#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAP="$ROOT/data/backfill/fuel_food_2021_2022/snapshots"
OUT="$ROOT/_truth/backfill"
LOG="$ROOT/_truth/logs/backfill_pressure.log"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ID="pressure_$(date -u +"%Y%m%dT%H%M%SZ")"

mkdir -p "$OUT" "$(dirname "$LOG")"

RAW="$OUT/${ID}_raw.json"
LEAF="$OUT/${ID}_leaf.json"

python3 - "$SNAP" "$RAW" "$TS" <<'PY'
import csv, json, sys
from pathlib import Path

snap = Path(sys.argv[1])
raw_out = Path(sys.argv[2])
ts = sys.argv[3]

def rows(name):
    with open(snap / name, newline="") as f:
        return list(csv.DictReader(f))

def f(x):
    return float(x)

diesel = rows("diesel.csv")
planting = rows("planting.csv")
harvest = rows("harvest.csv")
cpi = rows("cpi.csv")

# Edge 1: diesel pressure = worst/latest fuel constraint
d_last = diesel[-1]
diesel_pressure = min(
    f(d_last["padd2_stocks"]),
    f(d_last["padd3_stocks"]),
    1 / f(d_last["diesel_price"]),
    f(d_last["refinery_util"])
)

# Edge 3: planting velocity = planted / 5yr avg, capped by diesel pressure
p_last = planting[-1]
corn_pressure = f(p_last["corn_planted"]) / f(p_last["five_year_avg"])
soy_pressure = f(p_last["soy_planted"]) / f(p_last["five_year_avg"])
planting_velocity = min(diesel_pressure, corn_pressure, soy_pressure)

# Edge 4: harvest output = crop condition + harvest progress capped by planting
h_last = harvest[-1]
harvest_output = min(
    planting_velocity,
    f(h_last["crop_condition"]),
    f(h_last["harvest_progress"])
)

# Edge 5: CPI food pressure = inverse price stress capped by harvest output
c_last = cpi[-1]
cpi_pressure = min(
    1 / f(c_last["cpi_food_home"]),
    1 / f(c_last["cpi_cereals"])
)
urban_food_pressure = min(harvest_output, cpi_pressure)

def band(x):
    if x >= 0.85: return "GREEN"
    if x >= 0.70: return "YELLOW"
    if x >= 0.50: return "RED"
    return "DARK_RED"

doc = {
    "timestamp_utc": ts,
    "model": "fuel_food_backfill_pressure_engine_v0.1",
    "case": "fuel_food_2021_2022",
    "inputs": {
        "diesel_latest": d_last,
        "planting_latest": p_last,
        "harvest_latest": h_last,
        "cpi_latest": c_last
    },
    "edges": {
        "edge_1_diesel": {
            "pressure": round(diesel_pressure, 6),
            "status": band(diesel_pressure)
        },
        "edge_3_planting_velocity": {
            "pressure": round(planting_velocity, 6),
            "status": band(planting_velocity)
        },
        "edge_4_harvest_output": {
            "pressure": round(harvest_output, 6),
            "status": band(harvest_output)
        },
        "edge_5_urban_food_price": {
            "pressure": round(urban_food_pressure, 6),
            "status": band(urban_food_pressure)
        }
    },
    "doctrine": "edges fail first; prices show later",
    "status": "PRESSURES_COMPUTED"
}

raw_out.write_text(json.dumps(doc, sort_keys=True, indent=2))
PY

HASH="$(jq -cS . "$RAW" | sha256sum | awk '{print $1}')"

cat > "$LEAF" <<JSON
{
  "leaf_id": "$ID",
  "model": "backfill_pressure_leaf_v0.1",
  "timestamp_utc": "$TS",
  "canonical_hash_sha256": "$HASH",
  "raw_path": "$RAW",
  "status": "CAPTURED"
}
JSON

echo "BACKFILL_PRESSURE_OK ts=$TS hash=$HASH raw=$RAW leaf=$LEAF" | tee -a "$LOG"
