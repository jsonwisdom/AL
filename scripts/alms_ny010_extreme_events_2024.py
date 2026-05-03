from google.cloud import bigquery
import pandas as pd
import hashlib, json
from datetime import datetime, timezone

client = bigquery.Client()

# Load station map
station_map = pd.read_csv("_truth/bigquery/noaa_station_county_map.csv", dtype=str)
station_map["usaf"] = station_map["station_id"].str[:6].str.zfill(6)

# Stations proven available in GSOD 2024 schema probe path.
valid_stations = ["725016", "725180", "725280", "726228"]
station_map = station_map[station_map["usaf"].isin(valid_stations)]

print(f"Using {len(station_map)} station-county pairs from {len(valid_stations)} stations")

# GSOD mo is STRING with zero-padded values: '05', '06', etc.
query = """
SELECT stn, mo, da, temp, prcp, mxpsd
FROM `bigquery-public-data.noaa_gsod.gsod2024`
WHERE stn IN ('725016','725180','725280','726228')
  AND mo IN ('05','06','07','08','09')
"""

df = client.query(query).to_dataframe()
print(f"Retrieved records: {len(df)}")

if len(df) == 0:
    raise SystemExit("STOP: no GSOD records for summer months")

# Clean data in Python after retrieval to avoid SQL type drift.
df["temp"] = pd.to_numeric(df["temp"], errors="coerce")
df["prcp"] = pd.to_numeric(df["prcp"], errors="coerce")
df["mxpsd"] = pd.to_numeric(df["mxpsd"], errors="coerce")

df = df[(df["temp"] > -50) & (df["temp"] < 120)].copy()
df["usaf"] = df["stn"].astype(str).str.zfill(6)
df = df.merge(station_map[["usaf", "county_fips"]], on="usaf", how="left")
df = df[df["county_fips"].notna()].copy()
print(f"County-matched records: {len(df)}")

# Compute extreme flags.
df["is_heat_day_90f"] = (df["temp"] >= 90).astype(int)
df["is_heat_stress_85f"] = (df["temp"] >= 85).astype(int)
df["is_heavy_rain_1in"] = (df["prcp"] >= 1.0).fillna(False).astype(int)
df["is_extreme_wind_50"] = (df["mxpsd"] >= 50).fillna(False).astype(int)

print(f"Heat days (90F+): {df['is_heat_day_90f'].sum()}")
print(f"Heat stress days (85F+): {df['is_heat_stress_85f'].sum()}")
print(f"Heavy rain days (1in+): {df['is_heavy_rain_1in'].sum()}")
print(f"Extreme wind days (50+ knots): {df['is_extreme_wind_50'].sum()}")

# Aggregate to county level.
county_agg = df.groupby("county_fips", as_index=False).agg(
    heat_days_90f=("is_heat_day_90f", "sum"),
    heat_stress_days_85f=("is_heat_stress_85f", "sum"),
    heavy_rain_days_1in=("is_heavy_rain_1in", "sum"),
    extreme_wind_days_50=("is_extreme_wind_50", "sum"),
    mean_temp_f=("temp", "mean"),
    total_precip_in=("prcp", "sum"),
    station_records=("stn", "count"),
    station_count=("usaf", "nunique"),
)

# Get all 62 counties.
spine = pd.read_csv("_truth/bigquery/ny_county_fips_62.csv", dtype=str)
if "county_fips" not in spine.columns:
    spine["county_fips"] = spine["geo_id"].astype(str).str.zfill(5)

result = spine.merge(county_agg, on="county_fips", how="left")

# Fill event counts with 0; leave mean/precip null for counties without station records.
for col in ["heat_days_90f", "heat_stress_days_85f", "heavy_rain_days_1in", "extreme_wind_days_50", "station_records", "station_count"]:
    result[col] = result[col].fillna(0).astype(int)

for col in ["mean_temp_f", "total_precip_in"]:
    result[col] = pd.to_numeric(result[col], errors="coerce").round(2)


def safe_norm(series, weight):
    m = series.max()
    if pd.isna(m) or m == 0:
        return 0
    return series / m * weight


result["extreme_score"] = (
    safe_norm(result["heat_days_90f"], 30)
    + safe_norm(result["heat_stress_days_85f"], 20)
    + safe_norm(result["heavy_rain_days_1in"], 25)
    + safe_norm(result["extreme_wind_days_50"], 25)
).round(2)

# Add county names from income surface if available.
county_names = pd.read_csv("_truth/bigquery/ny_acs_income_overlay_62.csv", dtype=str)
if "fips" in county_names.columns:
    county_names = county_names[["fips", "county_name"]].rename(columns={"fips": "county_fips"})
elif "geo_id" in county_names.columns:
    county_names = county_names[["geo_id", "county_name"]].rename(columns={"geo_id": "county_fips"})
else:
    county_names = pd.DataFrame(columns=["county_fips", "county_name"])

result = result.merge(county_names.drop_duplicates(), on="county_fips", how="left")

out = "_truth/bigquery/ny010_extreme_events_2024.csv"
result.to_csv(out, index=False)

digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
station_to_county = station_map[["usaf", "county_fips"]].drop_duplicates()
station_to_county = station_to_county.merge(county_names.drop_duplicates(), on="county_fips", how="left")

manifest = {
    "receipt": "NY-010",
    "artifact": "NY_EXTREME_EVENTS_2024",
    "source": "bigquery-public-data.noaa_gsod.gsod2024",
    "season": "May-September 2024",
    "stations_used": valid_stations,
    "station_county_mapping": station_to_county[["usaf", "county_name"]].to_dict(orient="records"),
    "rows": int(len(result)),
    "counties_with_station_data": int((result["station_count"] > 0).sum()),
    "hash": digest,
    "output": out,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "guardrails": [
        "Station coverage sparse; only stations proven available in GSOD 2024 are used.",
        "GSOD mo is STRING with zero-padded month values; filter uses '05' through '09'.",
        "Zero event counts for counties without stations do not mean no extreme events occurred.",
        "Do not claim health impact, economic loss, disaster attribution, or climate trend."
    ],
}

with open("_truth/bigquery/ny010_extreme_events_manifest.json", "w") as f:
    f.write(json.dumps(manifest, indent=2) + "\n")

print("\n✅ NY-010 Extreme Events Complete")
print(f"ROWS: {len(result)}")
print(f"Counties with station data: {(result['station_count'] > 0).sum()} of 62")
print(f"HASH: {digest}")

print("\nStation to county mapping:")
for _, row in station_to_county.iterrows():
    print(f"  Station {row['usaf']} -> {row.get('county_name', '')}")

print("\nCounties with station data:")
cols = ["county_name", "heat_days_90f", "heavy_rain_days_1in", "extreme_score", "mean_temp_f"]
print(result[result["station_count"] > 0][cols].to_string(index=False))
