#!/usr/bin/env bash
set -euo pipefail

echo "🔎 ALMS Receipt #9b - Census County Employment Probe"
mkdir -p _truth/bigquery

OUT="_truth/bigquery/census_county_employment_probe.csv"

python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys

client = bigquery.Client()

query = """
SELECT
  table_name,
  column_name,
  data_type
FROM `bigquery-public-data.census_bureau_economic_indicators.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name, ordinal_position
LIMIT 100
"""

df = client.query(query).to_dataframe()
df.to_csv(sys.stdout, index=False, header=True)
PY

HASH="$(sha256sum "$OUT" | awk '{print $1}')"
ROWS="$(($(wc -l < "$OUT") - 1))"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat >> _truth/bigquery/alms_ledger.txt <<LEDGER

=== SCHEMA_PROBE_RECEIPT ===
TIMESTAMP: $TS
DATASET: census_bureau_economic_indicators
QUERY_TYPE: INFORMATION_SCHEMA_LIMIT_100
OUTPUT: $OUT
ROWS: $ROWS
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: PROBED
LEDGER

echo "✅ CENSUS_EMPLOYMENT_PROBE_OK"
echo "ROWS: $ROWS"
echo "HASH: $HASH"
echo "OUTPUT: $OUT"
head -50 "$OUT"
