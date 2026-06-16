#!/usr/bin/env python3
"""
ALMS NY 62-County FIPS Loader

Purpose:
  Produce a deterministic New York county scaffold for downstream ALMS civic joins.

Boundaries:
  - No network fetches.
  - No dynamic mutation.
  - Static NY county FIPS seed only.
  - Output is a scaffold, not an external data claim.

Next allowed overlays:
  - ACS full-county income/demographics.
  - NOAA station/county coverage.
  - Future county labor source only after schema proof.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("_truth/bigquery/ny_county_fips_62.csv")
MANIFEST = Path("_truth/bigquery/ny_county_fips_62_manifest.json")
LEDGER = Path("_truth/bigquery/alms_ledger.txt")

COUNTIES = [
    ("36001", "Albany County"),
    ("36003", "Allegany County"),
    ("36005", "Bronx County"),
    ("36007", "Broome County"),
    ("36009", "Cattaraugus County"),
    ("36011", "Cayuga County"),
    ("36013", "Chautauqua County"),
    ("36015", "Chemung County"),
    ("36017", "Chenango County"),
    ("36019", "Clinton County"),
    ("36021", "Columbia County"),
    ("36023", "Cortland County"),
    ("36025", "Delaware County"),
    ("36027", "Dutchess County"),
    ("36029", "Erie County"),
    ("36031", "Essex County"),
    ("36033", "Franklin County"),
    ("36035", "Fulton County"),
    ("36037", "Genesee County"),
    ("36039", "Greene County"),
    ("36041", "Hamilton County"),
    ("36043", "Herkimer County"),
    ("36045", "Jefferson County"),
    ("36047", "Kings County"),
    ("36049", "Lewis County"),
    ("36051", "Livingston County"),
    ("36053", "Madison County"),
    ("36055", "Monroe County"),
    ("36057", "Montgomery County"),
    ("36059", "Nassau County"),
    ("36061", "New York County"),
    ("36063", "Niagara County"),
    ("36065", "Oneida County"),
    ("36067", "Onondaga County"),
    ("36069", "Ontario County"),
    ("36071", "Orange County"),
    ("36073", "Orleans County"),
    ("36075", "Oswego County"),
    ("36077", "Otsego County"),
    ("36079", "Putnam County"),
    ("36081", "Queens County"),
    ("36083", "Rensselaer County"),
    ("36085", "Richmond County"),
    ("36087", "Rockland County"),
    ("36089", "St. Lawrence County"),
    ("36091", "Saratoga County"),
    ("36093", "Schenectady County"),
    ("36095", "Schoharie County"),
    ("36097", "Schuyler County"),
    ("36099", "Seneca County"),
    ("36101", "Steuben County"),
    ("36103", "Suffolk County"),
    ("36105", "Sullivan County"),
    ("36107", "Tioga County"),
    ("36109", "Tompkins County"),
    ("36111", "Ulster County"),
    ("36113", "Warren County"),
    ("36115", "Washington County"),
    ("36117", "Wayne County"),
    ("36119", "Westchester County"),
    ("36121", "Wyoming County"),
    ("36123", "Yates County"),
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    if len(COUNTIES) != 62:
        raise SystemExit(f"STOP: expected 62 counties, got {len(COUNTIES)}")

    if len({fips for fips, _ in COUNTIES}) != 62:
        raise SystemExit("STOP: duplicate FIPS detected")

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["geo_id", "county_name", "state_fips"])
        writer.writeheader()
        for geo_id, county_name in COUNTIES:
            writer.writerow({"geo_id": geo_id, "county_name": county_name, "state_fips": "36"})

    digest = sha256_file(OUT)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    manifest = {
        "artifact": "NY_COUNTY_FIPS_62_SCAFFOLD",
        "status": "MEASURED",
        "rows": 62,
        "hash": digest,
        "output": str(OUT),
        "policy": "LOCAL_ONLY_NO_DYNAMIC_FETCH_NO_GHOST_PROMOTION",
        "guardrail": "This is a static county FIPS scaffold, not an external live dataset receipt.",
        "blocked_claim": "Do not claim multi-signal statewide coverage until overlays are joined and hashed."
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(
            f"\n=== SCAFFOLD_RECEIPT ===\n"
            f"TIMESTAMP: {timestamp}\n"
            f"ARTIFACT: ny_county_fips_62\n"
            f"OUTPUT: {OUT}\n"
            f"ROWS: 62\n"
            f"HASH: {digest}\n"
            f"POLICY: LOCAL_ONLY_NO_DYNAMIC_FETCH_NO_GHOST_PROMOTION\n"
            f"STATUS: MEASURED\n"
        )

    print("✅ NY_FIPS_62_SCAFFOLD_OK")
    print("ROWS: 62")
    print(f"HASH: {digest}")
    print(f"OUTPUT: {OUT}")


if __name__ == "__main__":
    main()
