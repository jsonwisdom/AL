#!/usr/bin/env bash
set -euo pipefail
echo "🏛️ ALMS Receipt #3 - Census ACS BigQuery-only"
source .venv/bin/activate
source .alms_env
mkdir -p _truth/bigquery
OUT="_truth/bigquery/acs_ny_counties_2022_top10.csv"
python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys
client = bigquery.Client()
query = """
SELECT
  geo_id,
  county_name,
  total_pop,
  median_income
FROM `bigquery-public-data.census_bureau_acs.county_2022_5yr`
WHERE state_fips_code = '36'
ORDER BY county_name
LIMIT 10
"""
df = client.query(query).to_dataframe()
df.to_csv(sys.stdout, index=False, header=True)
PY
HASH="$(sha256sum "$OUT" | awk '{print $1}')"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
cat >> _truth/bigquery/alms_ledger.txt <<LEDGER
=== DATASET_RECEIPT ===
TIMESTAMP: $TS
DATASET: census_acs_ny_counties_2022_top10
QUERY_TYPE: PUBLIC_LIMIT_10
OUTPUT: $OUT
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: MEASURED
LEDGER
echo "✅ ACS_RECEIPT_OK"
echo "HASH: $HASH"
