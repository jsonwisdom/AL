#!/usr/bin/env bash
set -euo pipefail
echo "🔎 ALMS Receipt #9 - BLS LAUS Schema Probe"
mkdir -p _truth/bigquery
OUT="_truth/bigquery/bls_laus_schema_probe.csv"
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
ORDER BY table_name, ordinal_position
LIMIT 200
"""
df = client.query(query).to_dataframe()
df.to_csv(sys.stdout, index=False, header=True)
PY
HASH="$(sha256sum "$OUT" | awk '{print $1}')"
ROWS="$(($(wc -l < "$OUT") - 1))"
echo "✅ LAUS_PROBE_OK"
echo "ROWS: $ROWS"
echo "HASH: $HASH"
echo "OUTPUT: $OUT"
head -60 "$OUT"
