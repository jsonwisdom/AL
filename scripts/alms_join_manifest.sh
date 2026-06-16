#!/usr/bin/env bash
set -euo pipefail

echo "🧭 ALMS Receipt #8 - Cross-Signal JOIN Manifest"
mkdir -p _truth/bigquery

OUT="_truth/bigquery/cross_signal_join_manifest.json"

cat > "$OUT" <<'JSON'
{
  "artifact": "ALMS_CROSS_SIGNAL_JOIN_MANIFEST",
  "version": "1.0",
  "policy": "NO_GHOST_PROMOTION",
  "cost_policy": "LOCAL_ONLY_NO_BIGQUERY_NO_VERTEX_NO_COMPUTE",
  "scope": "current_green_bigquery_receipts",
  "verdict": "PARTIAL",
  "county_level_join": "PARTIAL",
  "receipts": [
    {
      "dataset": "usa_names_ny_2020_top10",
      "signal": "identity_context",
      "spatial_key": "state",
      "temporal_key": "year",
      "join_status": "PARTIAL",
      "note": "State/year context only; not county-level."
    },
    {
      "dataset": "census_acs_ny_counties_2022_top10",
      "signal": "demographics_income",
      "spatial_key": "county_name_geo_id",
      "temporal_key": "acs_2022_5yr",
      "join_status": "JOIN_READY",
      "note": "Best county-level anchor currently available."
    },
    {
      "dataset": "bls_employment_2023_top10",
      "signal": "labor_sector",
      "spatial_key": "none_or_national",
      "temporal_key": "year",
      "join_status": "NOT_JOINABLE_COUNTY",
      "note": "Green receipt, but not NY county-aligned; useful as national labor context."
    },
    {
      "dataset": "noaa_gsod_2022_top10",
      "signal": "climate_weather",
      "spatial_key": "station",
      "temporal_key": "date",
      "join_status": "PARTIAL",
      "note": "Needs station-to-county crosswalk before county joins."
    },
    {
      "dataset": "wikipedia_pageviews_fixed_top10",
      "signal": "attention",
      "spatial_key": "none",
      "temporal_key": "datehour",
      "join_status": "NOT_JOINABLE_COUNTY",
      "note": "Global attention signal; not county-level without topic/geography mapping."
    }
  ],
  "allowed_next_steps": [
    "Normalize BLS to county/FIPS via LAUS or another county labor source.",
    "Normalize NOAA using station-to-county crosswalk.",
    "Treat names and Wikipedia as context signals, not county join keys."
  ],
  "blocked_claims": [
    "Do not claim a county-level civic risk fingerprint yet.",
    "Do not join all five signals as if they share a common key.",
    "Do not promote attention or names data as county evidence without a mapping receipt."
  ]
}
JSON

HASH="$(sha256sum "$OUT" | awk '{print $1}')"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat >> _truth/bigquery/alms_ledger.txt <<LEDGER

=== JOIN_MANIFEST_RECEIPT ===
TIMESTAMP: $TS
ARTIFACT: cross_signal_join_manifest
OUTPUT: $OUT
HASH: $HASH
POLICY: LOCAL_ONLY_NO_BIGQUERY_NO_VERTEX_NO_COMPUTE
STATUS: PARTIAL_JOINABILITY_CONFIRMED
LEDGER

echo "✅ JOIN_MANIFEST_OK"
echo "STATUS: PARTIAL_JOINABILITY_CONFIRMED"
echo "HASH: $HASH"
echo "OUTPUT: $OUT"
