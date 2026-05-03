#!/usr/bin/env python3
"""
NY-011 dependency audit.

Purpose:
  Determine whether validation/uncertainty quantification can proceed using real anchored files.

This script does not create a validation result. It only audits local artifacts and writes
an explicit GO/BLOCK manifest.
"""

from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

FILES = [
    "_truth/bigquery/ny010_extreme_events_2024.csv",
    "_truth/bigquery/ny010_extreme_events_manifest.json",
    "_truth/bigquery/ny_noaa_income_overlay_62.csv",
    "_truth/bigquery/ny004_noaa_manifest.json",
    "_truth/bigquery/ny005_prism_county_normals.csv",
    "_truth/bigquery/ny007b_gsod_panel.csv",
    "_truth/bigquery/ny007b_gsod_trends.csv",
    "_truth/bigquery/ny007b_gsod_manifest.json",
]

OUT = Path("_truth/bigquery/ny011_dependency_audit.json")
LEDGER = Path("_truth/bigquery/alms_ledger.txt")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(path: Path) -> int | None:
    if path.suffix.lower() not in {".csv", ".txt", ".json"}:
        return None
    return len(path.read_text(errors="replace").splitlines())


def main() -> None:
    records = []
    for name in FILES:
        p = Path(name)
        records.append({
            "path": name,
            "exists": p.exists(),
            "bytes": p.stat().st_size if p.exists() else 0,
            "lines": line_count(p) if p.exists() else None,
            "sha256": sha256(p) if p.exists() else None,
        })

    missing = [r["path"] for r in records if not r["exists"]]
    status = "GO" if not missing else "BLOCKED_MISSING_DEPENDENCIES"

    manifest = {
        "receipt": "NY-011_DEPENDENCY_AUDIT",
        "status": status,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": records,
        "missing": missing,
        "guardrails": [
            "Do not run NY-011 validation unless status is GO.",
            "Do not synthesize PRISM or NY-007B files from narrative claims.",
            "If dependencies are missing, open a dependency reconstruction receipt first."
        ]
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    digest = sha256(OUT)

    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(
            "\n=== DEPENDENCY_AUDIT_RECEIPT ===\n"
            f"TIMESTAMP: {manifest['timestamp_utc']}\n"
            "RECEIPT: NY-011_DEPENDENCY_AUDIT\n"
            f"STATUS: {status}\n"
            f"MISSING_COUNT: {len(missing)}\n"
            f"OUTPUT: {OUT}\n"
            f"HASH: {digest}\n"
            "POLICY: NO_SYNTHETIC_VALIDATION_NO_GHOST_PROMOTION\n"
        )

    print("✅ NY-011_DEPENDENCY_AUDIT_COMPLETE")
    print(f"STATUS: {status}")
    print(f"MISSING_COUNT: {len(missing)}")
    for m in missing:
        print(f"MISSING: {m}")
    print(f"HASH: {digest}")
    print(f"OUTPUT: {OUT}")


if __name__ == "__main__":
    main()
