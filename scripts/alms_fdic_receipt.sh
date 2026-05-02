#!/usr/bin/env bash
set -euo pipefail
echo "🏦 ALMS Receipt #7 - FDIC Banking Data (Infrastructure Signal)"
source .venv/bin/activate
source .alms_env
mkdir -p _truth/bigquery
OUT="_truth/bigquery/fdic_banking_ny_top10.csv"
python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys
client = bigquery.Client()
query = """
SELECT
  cert,
  name,
  city,
  stalp,
  asset,
  depdom
FROM `bigquery-public-data.fdic.fdic_institutions`
WHERE stalp = 'NY'
  AND asset IS NOT NULL
ORDER BY asset DESC
LIMIT 10
"""
df = client.query(query).to_dataframe()
df.to_csv(sys.stdout, index=False, header=True)
PY
HASH="$(sha256sum "$OUT" | awk '{print $1}')"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ROWS="$(($(wc -l < "$OUT") - 1))"
if [ "$ROWS" -eq "10" ]; then
  cat >> _truth/bigquery/alms_ledger.txt <<LEDGER
=== DATASET_RECEIPT ===
TIMESTAMP: $TS
DATASET: fdic_banking_ny_top10
QUERY_TYPE: PUBLIC_LIMIT_10
OUTPUT: $OUT
ROWS: $ROWS
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: MEASURED
LEDGER
  echo "✅ FDIC_RECEIPT_OK"
  echo "ROWS: $ROWS"
  echo "HASH: $HASH"
  echo "OUTPUT: $OUT"
else
  echo "❌ ROWS: $ROWS - Expected 10, stopping"
  exit 1
fi
