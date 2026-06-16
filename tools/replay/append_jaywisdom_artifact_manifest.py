#!/usr/bin/env python3
"""
Append one real artifact record to the Jay Wisdom Zora artifact manifest CSV.

This helper does not fetch Zora, call chain RPC, control a wallet, or verify revenue.
It only appends user-supplied artifact metadata with an explicit source and status.
"""

from __future__ import annotations

import argparse
import csv
import os
from datetime import date

DEFAULT_MANIFEST = "docs/zora/artifacts/jaywisdom_zora_artifact_manifest_v0_1.csv"
FIELDNAMES = [
    "artifact_id",
    "title",
    "zora_profile",
    "zora_url",
    "contract_or_coin",
    "source",
    "observed_at",
    "status",
    "verification_level",
    "notes",
]
ALLOWED_SOURCES = {
    "operator_screenshot",
    "fresh_screenshot",
    "manual_title_list",
    "verified_artifact_url",
    "zora_api_json",
    "csv_export",
}


def existing_ids(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8") as handle:
        return {row.get("artifact_id", "") for row in csv.DictReader(handle)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a Jay Wisdom Zora artifact manifest row")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--zora-profile", default="jaywisdom")
    parser.add_argument("--zora-url", default="")
    parser.add_argument("--contract-or-coin", default="unknown")
    parser.add_argument("--source", required=True, choices=sorted(ALLOWED_SOURCES))
    parser.add_argument("--observed-at", default=date.today().isoformat())
    parser.add_argument("--status", default="reported")
    parser.add_argument("--verification-level", default="seed_only")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    if args.artifact_id in existing_ids(args.manifest):
        raise SystemExit(f"artifact_id already exists: {args.artifact_id}")

    file_exists = os.path.exists(args.manifest)
    row = {
        "artifact_id": args.artifact_id,
        "title": args.title,
        "zora_profile": args.zora_profile,
        "zora_url": args.zora_url,
        "contract_or_coin": args.contract_or_coin,
        "source": args.source,
        "observed_at": args.observed_at,
        "status": args.status,
        "verification_level": args.verification_level,
        "notes": args.notes,
    }

    os.makedirs(os.path.dirname(args.manifest), exist_ok=True)
    with open(args.manifest, "a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"appended_artifact_id={args.artifact_id}")
    print("revenue_confirmed=false")
    print("authority=false")
    print("no_fake_green=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
