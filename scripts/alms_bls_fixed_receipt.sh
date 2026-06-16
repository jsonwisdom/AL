#!/usr/bin/env bash
set -euo pipefail
echo "👷 ALMS Receipt #6 - BLS Employment Data (Fixed)"
source .venv/bin/activate
source .alms_env
mkdir -p _truth/bigquery
OUT="_truth/bigquery/bls_employment_ny_2023_top10.csv"
python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys
client = bigquery.Client()
query = """
SELECT
  year,
  sector,
  subsector,
  total_employed_in_thousands
FROM `bigquery-public-data.bls.cpsaat18`
WHERE year = 2023
ORDER BY sector, subsector
LIMIT 10
"""
df = client.query(query).to_dataframe()
df.to_csv(sys.stdout, index=False, header=True)
PY
HASH="$(sha256sum "$OUT" | awk '{print $1}')"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ROWS="$(($(wc -l < "$OUT") - 1))"
cat >> _truth/bigquery/alms_ledger.txt <<LEDGER
=== DATASET_RECEIPT ===
TIMESTAMP: $TS
DATASET: bls_employment_ny_2023_top10
QUERY_TYPE: PUBLIC_LIMIT_10
OUTPUT: $OUT
ROWS: $ROWS
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: MEASURED
LEDGER
echo "✅ BLS_FIXED_RECEIPT_OK"
echo "ROWS: $ROWS"
echo "HASH: $HASH"
echo "OUTPUT: $OUT"
