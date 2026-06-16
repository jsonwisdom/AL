#!/usr/bin/env bash
set -euo pipefail
echo "🔎 ALMS Receipt #6 - BLS Schema Probe BigQuery-only"
source .venv/bin/activate
source .alms_env
mkdir -p _truth/bigquery
OUT="_truth/bigquery/bls_schema_probe.csv"
python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys
client = bigquery.Client()
query = """
SELECT
  table_name,
  column_name,
  data_type
FROM `bigquery-public-data.bls.INFORMATION_SCHEMA.COLUMNS`
WHERE LOWER(table_name) LIKE '%laus%'
   OR LOWER(table_name) LIKE '%cps%'
   OR LOWER(table_name) LIKE '%unemployment%'
ORDER BY table_name, ordinal_position
LIMIT 200
"""
df = client.query(query).to_dataframe()
df.to_csv(sys.stdout, index=False, header=True)
PY
HASH="$(sha256sum "$OUT" | awk '{print $1}')"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ROWS="$(($(wc -l < "$OUT") - 1))"
cat >> _truth/bigquery/alms_ledger.txt <<LEDGER
=== SCHEMA_PROBE_RECEIPT ===
TIMESTAMP: $TS
DATASET: bls_schema_probe
QUERY_TYPE: INFORMATION_SCHEMA_LIMIT_200
OUTPUT: $OUT
ROWS: $ROWS
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: PROBED
LEDGER
echo "✅ BLS_SCHEMA_PROBE_OK"
echo "ROWS: $ROWS"
echo "HASH: $HASH"
echo "OUTPUT: $OUT"
