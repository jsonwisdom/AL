#!/usr/bin/env python3
"""
NY-004 NOAA climate x income overlay.

Purpose:
  Join NOAA station-derived climate normals to the NY-003C 62-county income surface.

Guardrails:
  - Depends on NY-003C income surface.
  - Uses a station-to-county mapping artifact; NOAA station coverage is uneven.
  - County-level values are station averages, not gridded climate products.
  - No risk model, hazard model, trend claim, or climate-change claim is produced here.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from google.cloud import bigquery

NY_INCOME = Path("_truth/bigquery/ny_acs_income_overlay_62_5yr.csv")
# Expected columns: station_id, county_fips
STATION_MAP = Path("_truth/bigquery/noaa_station_county_map.csv")
OUT = Path("_truth/bigquery/ny_noaa_income_overlay_62.csv")
MANIFEST = Path("_truth/bigquery/ny004_noaa_manifest.json")
LEDGER = Path("_truth/bigquery/alms_ledger.txt")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise SystemExit(f"STOP: {label} missing columns: {missing}")


def main() -> None:
    if not NY_INCOME.exists():
        raise SystemExit(f"STOP: missing NY income input: {NY_INCOME}")
    if not STATION_MAP.exists():
        raise SystemExit(f"STOP: missing station county map: {STATION_MAP}")

    ny_df = pd.read_csv(NY_INCOME, dtype={"geo_id": str, "fips": str})
    station_map = pd.read_csv(STATION_MAP, dtype={"station_id": str, "county_fips": str})

    if "fips" not in ny_df.columns:
        if "geo_id" in ny_df.columns:
            ny_df["fips"] = ny_df["geo_id"].astype(str).str.zfill(5)
        else:
            raise SystemExit("STOP: NY income input needs fips or geo_id")

    require_columns(ny_df, {"fips"}, "NY income")
    require_columns(station_map, {"station_id", "county_fips"}, "NOAA station map")

    ny_df["fips"] = ny_df["fips"].astype(str).str.zfill(5)
    station_map["county_fips"] = station_map["county_fips"].astype(str).str.zfill(5)

    client = bigquery.Client()
    query = """
    SELECT
      station_id,
      normal_ann_tavg_c AS annual_mean_temp_c,
      normal_ann_prcp_mm AS annual_precip_mm
    FROM `bigquery-public-data.ghcn_d.ghcnd_normals_annual`
    WHERE country_code = 'US'
    """
    noaa_df = client.query(query).to_dataframe()
    noaa_df["station_id"] = noaa_df["station_id"].astype(str)

    noaa_county = station_map.merge(noaa_df, on="station_id", how="left")
    noaa_agg = (
        noaa_county.groupby("county_fips", as_index=False)
        .agg(
            station_count=("station_id", "count"),
            stations_with_normals=("annual_mean_temp_c", lambda s: int(s.notna().sum())),
            annual_mean_temp_c=("annual_mean_temp_c", "mean"),
            annual_precip_mm=("annual_precip_mm", "mean"),
        )
    )

    merged = ny_df.merge(noaa_agg, left_on="fips", right_on="county_fips", how="left")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT, index=False)

    digest = sha256_file(OUT)
    rows = int(len(merged))
    rows_with_noaa = int(merged["annual_mean_temp_c"].notna().sum()) if "annual_mean_temp_c" in merged else 0

    manifest = {
        "receipt": "NY-004",
        "artifact": "NY_NOAA_INCOME_OVERLAY",
        "input": "NY-003C",
        "rows": rows,
        "rows_with_noaa": rows_with_noaa,
        "hash": digest,
        "output": str(OUT),
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "join_key": "fips",
        "policy": "BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE",
        "guardrails": [
            "NOAA station coverage is uneven; do not claim uniform spatial resolution.",
            "County-level values are station averages, not gridded climate products.",
            "Do not claim risk model; this is exposure overlay only.",
            "Do not infer trends or climate change from normals alone."
        ]
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(
            "\n=== DATASET_RECEIPT ===\n"
            f"TIMESTAMP: {manifest['timestamp_utc']}\n"
            "RECEIPT: NY-004\n"
            "ARTIFACT: NY_NOAA_INCOME_OVERLAY\n"
            f"OUTPUT: {OUT}\n"
            f"ROWS: {rows}\n"
            f"ROWS_WITH_NOAA: {rows_with_noaa}\n"
            f"HASH: {digest}\n"
            "POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE\n"
            "STATUS: MEASURED\n"
        )

    print("✅ NY-004 NOAA overlay complete")
    print(f"ROWS: {rows}")
    print(f"Rows with NOAA data: {rows_with_noaa}")
    print(f"HASH: {digest}")
    print(f"OUTPUT: {OUT}")


if __name__ == "__main__":
    main()
