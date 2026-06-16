from google.cloud import bigquery
import hashlib, json
from datetime import datetime, timezone

client = bigquery.Client()

out = "_truth/bigquery/ny007_era5_schema_probe.csv"
manifest = "_truth/bigquery/ny007_era5_schema_probe_manifest.json"

datasets = ["era5", "era5_land"]
rows = []

for ds in datasets:
    try:
        tables = list(client.list_tables(client.dataset(ds, project="bigquery-public-data")))
        for t in tables[:50]:
            rows.append({
                "dataset": ds,
                "table": t.table_id,
                "type": t.table_type
            })
    except Exception as e:
        rows.append({
            "dataset": ds,
            "table": "UNAVAILABLE",
            "type": f"{type(e).__name__}: {e}"
        })

import pandas as pd
df = pd.DataFrame(rows)
df.to_csv(out, index=False)

digest = hashlib.sha256(open(out, "rb").read()).hexdigest()

m = {
    "receipt": "NY-007_SCHEMA_PROBE",
    "artifact": "ERA5_PUBLIC_DATASET_DISCOVERY",
    "rows": int(len(df)),
    "hash": digest,
    "output": out,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "guardrail": "Do not build ERA5 panel until actual table names and schema are confirmed."
}

with open(manifest, "w") as f:
    f.write(json.dumps(m, indent=2) + "\n")

print("✅ NY007_ERA5_PROBE_OK")
print("ROWS:", len(df))
print("HASH:", digest)
print(df.to_string(index=False))
