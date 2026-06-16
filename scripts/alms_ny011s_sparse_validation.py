import pandas as pd
import hashlib, json
from datetime import datetime, timezone

print("=== NY-011S: Sparse Validation — GSOD Station Truth Only ===")

trends = pd.read_csv("_truth/bigquery/ny007b_gsod_trends.csv", dtype=str)
trends["county_fips"] = trends["county_fips"].astype(str).str.zfill(5)

climate = pd.read_csv("_truth/bigquery/ny_noaa_income_overlay_62.csv", dtype=str)
climate["county_fips"] = climate["county_fips"].astype(str).str.zfill(5)

extremes = pd.read_csv("_truth/bigquery/ny010_extreme_events_2024.csv", dtype=str)
extremes["county_fips"] = extremes["county_fips"].astype(str).str.zfill(5)

validation = trends.merge(
    climate[["county_fips", "avg_annual_temp_f", "stations_in_county"]],
    on="county_fips",
    how="left"
).merge(
    extremes[["county_fips", "heavy_rain_days_1in", "extreme_score", "station_count"]],
    on="county_fips",
    how="left"
)

for col in ["avg_annual_temp_f", "stations_in_county", "heavy_rain_days_1in", "extreme_score", "station_count", "temp_trend_f_per_decade"]:
    validation[col] = pd.to_numeric(validation[col], errors="coerce")

validation = validation[(validation["stations_in_county"] > 0) | (validation["station_count"] > 0)].copy()

out_csv = "_truth/bigquery/ny011s_sparse_validation_statistics.csv"
out_json = "_truth/bigquery/ny011s_sparse_validation_report.json"

validation.to_csv(out_csv, index=False)

report = {
    "receipt": "NY-011S",
    "artifact": "SPARSE_GSOD_VALIDATION_REPORT",
    "status": "MEASURED",
    "scope": "GSOD station counties only",
    "counties_validated": int(len(validation)),
    "county_list": validation["county_name"].dropna().tolist(),
    "coverage": f"{len(validation)} of 62 counties",
    "statewide_validation": False,
    "prism_baseline": "MISSING",
    "inputs": [
        "_truth/bigquery/ny007b_gsod_trends.csv",
        "_truth/bigquery/ny_noaa_income_overlay_62.csv",
        "_truth/bigquery/ny010_extreme_events_2024.csv"
    ],
    "temp_trend_summary": {
        "mean_f_per_decade": float(validation["temp_trend_f_per_decade"].mean()),
        "min_f_per_decade": float(validation["temp_trend_f_per_decade"].min()),
        "max_f_per_decade": float(validation["temp_trend_f_per_decade"].max())
    },
    "guardrails": [
        "Sparse validation only.",
        "No PRISM or gridded baseline comparison.",
        "No statewide validation claim.",
        "No causality, health impact, economic loss, or attribution claim."
    ],
    "timestamp_utc": datetime.now(timezone.utc).isoformat()
}

with open(out_json, "w") as f:
    f.write(json.dumps(report, indent=2) + "\n")

digest = hashlib.sha256(open(out_json, "rb").read()).hexdigest()

with open("_truth/bigquery/alms_ledger.txt", "a") as f:
    f.write(
        f"\n=== VALIDATION_RECEIPT ===\n"
        f"RECEIPT: NY-011S\n"
        f"ARTIFACT: SPARSE_GSOD_VALIDATION_REPORT\n"
        f"COUNTIES_VALIDATED: {len(validation)}\n"
        f"HASH: {digest}\n"
        f"POLICY: SPARSE_ONLY_NO_STATEWIDE_VALIDATION\n"
        f"STATUS: MEASURED\n"
    )

print("\n✅ NY-011S Sparse Validation Complete")
print(f"Counties validated: {len(validation)} of 62")
print(f"HASH: {digest}")
print("\nValidation details:")
print(validation[["county_name","temp_trend_f_per_decade","avg_annual_temp_f","heavy_rain_days_1in","extreme_score"]].to_string(index=False))
