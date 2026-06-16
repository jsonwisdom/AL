import pandas as pd, hashlib, json

acs_path = "_truth/bigquery/acs_ny_counties_2022_top10.csv"
noaa_path = "_truth/bigquery/noaa_ny_stations_with_county.csv"
out_path = "_truth/bigquery/acs_noaa_fips_join_result.csv"
manifest_path = "_truth/bigquery/acs_noaa_fips_join_manifest.json"

# Minimal locked NY county-name → FIPS map for counties visible in Receipt #9.
# Guardrail: NOAA upstream county_fips remains pending; this is a local normalization receipt.
county_fips = {
    "Albany County": "36001",
    "Broome County": "36007",
    "Chautauqua County": "36013",
    "Erie County": "36029",
    "Franklin County": "36033",
    "Jefferson County": "36045",
    "Orange County": "36071",
    "Suffolk County": "36103",
    "Chittenden County": "50007"
}

acs = pd.read_csv(acs_path, dtype={"geo_id": str})
noaa = pd.read_csv(noaa_path)

noaa["county_fips_norm"] = noaa["county_name"].map(county_fips)
noaa_joinable = noaa.dropna(subset=["county_fips_norm"]).copy()

weather_by_county = (
    noaa_joinable.groupby(["county_fips_norm", "county_name"], as_index=False)
    .agg(
        station_count=("name", "count"),
        avg_station_elev=("elev", "mean")
    )
)

joined = acs.merge(
    weather_by_county,
    left_on="geo_id",
    right_on="county_fips_norm",
    how="inner"
)

joined.to_csv(out_path, index=False)
digest = hashlib.sha256(open(out_path, "rb").read()).hexdigest()

manifest = {
    "artifact": "ACS_NOAA_FIPS_JOIN_RESULT",
    "status": "MEASURED" if len(joined) > 0 else "NO_MATCH",
    "join_key": "acs.geo_id == noaa.county_fips_norm",
    "rows": int(len(joined)),
    "hash": digest,
    "output": out_path,
    "guardrail": "FIPS normalized from Receipt #9 county_name map; full NOAA county_fips still pending upstream.",
    "blocked_claim": "Do not claim NOAA source shipped FIPS until county_fips is populated upstream."
}

with open(manifest_path, "w") as f:
    f.write(json.dumps(manifest, indent=2) + "\n")

print("✅ ACS_NOAA_FIPS_JOIN_OK")
print("ROWS:", len(joined))
print("HASH:", digest)
print(joined.head(20).to_string(index=False))
