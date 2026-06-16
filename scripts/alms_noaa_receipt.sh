#!/usr/bin/env bash
set -euo pipefail
echo "🌦️ ALMS Receipt #5 - NOAA Weather BigQuery-only"
source .venv/bin/activate
source .alms_env
mkdir -p _truth/bigquery
OUT="_truth/bigquery/noaa_gsod_2022_top10.csv"
python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys
client = bigquery.Client()
query = """
SELECT
  stn,
  date,
  temp,
  dewp,
  slp,
  wdsp,
  prcp
FROM `bigquery-public-data.noaa_gsod.gsod2022`
WHERE temp IS NOT NULL
ORDER BY date
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
DATASET: noaa_gsod_2022_top10
QUERY_TYPE: PUBLIC_LIMIT_10
OUTPUT: $OUT
ROWS: $ROWS
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: MEASURED
LEDGER
echo "✅ NOAA_RECEIPT_OK"
echo "ROWS: $ROWS"
echo "HASH: $HASH"
echo "OUTPUT: $OUT"
