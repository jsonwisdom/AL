from google.cloud import bigquery
import hashlib, json
from datetime import datetime, timezone

client = bigquery.Client()

out = "_truth/bigquery/gsod2024_schema_probe.csv"
manifest = "_truth/bigquery/gsod2024_schema_probe_manifest.json"

query = """
WITH schema_rows AS (
  SELECT
    'SCHEMA' AS section,
    column_name AS key_name,
    data_type AS value_text,
    CAST(NULL AS INT64) AS row_count
  FROM `bigquery-public-data.noaa_gsod.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = 'gsod2024'
    AND column_name IN ('stn','year','mo','da','date','temp','prcp','mxpsd')
),
sample_rows AS (
  SELECT
    'SAMPLE' AS section,
    CONCAT(CAST(stn AS STRING), ':', CAST(mo AS STRING), ':', CAST(da AS STRING)) AS key_name,
    CAST(mo AS STRING) AS value_text,
    COUNT(*) AS row_count
  FROM `bigquery-public-data.noaa_gsod.gsod2024`
  WHERE CAST(stn AS STRING) = '725016'
  GROUP BY key_name, value_text
  ORDER BY key_name
  LIMIT 40
)
SELECT * FROM schema_rows
UNION ALL
SELECT * FROM sample_rows
ORDER BY section, key_name
"""

df = client.query(query).to_dataframe()
df.to_csv(out, index=False)

digest = hashlib.sha256(open(out, "rb").read()).hexdigest()

m = {
    "receipt": "GSOD_SCHEMA_PROBE",
    "table": "bigquery-public-data.noaa_gsod.gsod2024",
    "rows": int(len(df)),
    "hash": digest,
    "output": out,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "purpose": "Determine mo/stn/date schema before NY-010 extraction"
}

with open(manifest, "w") as f:
    f.write(json.dumps(m, indent=2) + "\n")

print("✅ GSOD_SCHEMA_PROBE_OK")
print("ROWS:", len(df))
print("HASH:", digest)
print("\n--- Probe Results ---")
print(df.to_string(index=False))
