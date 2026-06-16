#!/usr/bin/env bash
set -euo pipefail
echo "🌐 ALMS Receipt #7 - Wikipedia Pageviews (Fixed)"
source .venv/bin/activate
source .alms_env
mkdir -p _truth/bigquery
OUT="_truth/bigquery/wikipedia_pageviews_fixed_top10.csv"
python3 <<'PY' > "$OUT"
from google.cloud import bigquery
import sys
client = bigquery.Client()
query = """
SELECT
  title,
  views,
  datehour
FROM `bigquery-public-data.wikipedia.pageviews_2024`
WHERE wiki = 'en'
  AND datehour >= '2024-01-01'
  AND datehour < '2024-01-02'
  AND title NOT LIKE '%Special%'
ORDER BY views DESC
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
DATASET: wikipedia_pageviews_fixed_top10
QUERY_TYPE: PUBLIC_LIMIT_10_WITH_PARTITION
OUTPUT: $OUT
ROWS: $ROWS
HASH: $HASH
POLICY: BIGQUERY_ONLY_NO_VERTEX_NO_COMPUTE
STATUS: MEASURED
LEDGER
  echo "✅ WIKIPEDIA_FIXED_RECEIPT_OK"
  echo "ROWS: $ROWS"
  echo "HASH: $HASH"
else
  echo "❌ ROWS: $ROWS - Expected 10"
  exit 1
fi
