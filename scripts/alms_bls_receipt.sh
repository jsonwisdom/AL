#!/usr/bin/env bash
set -euo pipefail
echo "👷 ALMS Receipt #4 - BLS Unemployment BigQuery-only"
source .venv/bin/activate
source .alms_env
mkdir -p _truth/bigquery
OUT="_truth/bigquery/bls_unemployment_cps_2023_top10.csv"
python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys
client = bigquery.Client()
query = """
SELECT
  series_id,
  year,
  period,
  value
FROM `bigquery-public-data.bls.unemployment_cps`
WHERE year = 2023
ORDER BY series_id, period
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
DATASET: bls_unemployment_cps_2023_top10
QUERY_TYPE: PUBLIC_LIMIT_10
OUTPUT: $OUT
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: MEASURED
LEDGER
echo "✅ BLS_RECEIPT_OK"
echo "HASH: $HASH"
echo "OUTPUT: $OUT"
