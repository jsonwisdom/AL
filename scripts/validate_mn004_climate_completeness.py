#!/usr/bin/env python3
"""
MN-004 climate completeness validator.

Validates the external-truth CSV before it can become a receipt.
This script is infrastructure only. It does not fetch data, synthesize rows,
or mint receipt hashes for missing payloads.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_HEADERS = [
    "station_id",
    "station_name",
    "state",
    "year",
    "days_expected",
    "days_observed",
    "completeness_pct",
    "source",
    "source_url",
]

EXPECTED_STATIONS = {"KMSP", "KDLH", "KSTC"}
EXPECTED_YEARS = {2020, 2021, 2022, 2023, 2024}
EXPECTED_ROWS = 15
THRESHOLD = 98.0
ALLOWED_SOURCES = {"IEM_ASOS", "NCEI_LCD", "ASOS_LCD"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], report_path: Path | None = None) -> None:
    print("❌ MN004_VALIDATION_FAIL")
    for e in errors:
        print(f"ERROR: {e}")
    if report_path:
        print(f"REPORT: {report_path}")
    raise SystemExit(1)


def parse_int(value: str, field: str, row_num: int, errors: list[str]) -> int | None:
    try:
        return int(str(value).strip())
    except Exception:
        errors.append(f"row {row_num}: {field} must be integer, got {value!r}")
        return None


def parse_float(value: str, field: str, row_num: int, errors: list[str]) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        errors.append(f"row {row_num}: {field} must be float, got {value!r}")
        return None


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: validate_mn004_climate_completeness.py _truth/minnesota/MN-004_climate_completeness.csv")
        raise SystemExit(2)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        fail([f"missing CSV: {csv_path}"])

    errors: list[str] = []
    admitted_rows = []
    blocked_rows = []

    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        if headers != EXPECTED_HEADERS:
            errors.append(f"headers mismatch: expected {EXPECTED_HEADERS}, got {headers}")
        rows = list(reader)

    if len(rows) != EXPECTED_ROWS:
        errors.append(f"row_count mismatch: expected {EXPECTED_ROWS}, got {len(rows)}")

    seen = Counter()
    station_years = set()

    for idx, row in enumerate(rows, start=2):
        station = str(row.get("station_id", "")).strip().upper()
        station_name = str(row.get("station_name", "")).strip()
        state = str(row.get("state", "")).strip().upper()
        source = str(row.get("source", "")).strip().upper()
        source_url = str(row.get("source_url", "")).strip()

        year = parse_int(row.get("year", ""), "year", idx, errors)
        days_expected = parse_int(row.get("days_expected", ""), "days_expected", idx, errors)
        days_observed = parse_int(row.get("days_observed", ""), "days_observed", idx, errors)
        completeness_pct = parse_float(row.get("completeness_pct", ""), "completeness_pct", idx, errors)

        if station not in EXPECTED_STATIONS:
            errors.append(f"row {idx}: unexpected station_id {station!r}")
        if not station_name:
            errors.append(f"row {idx}: station_name blank")
        if state != "MN":
            errors.append(f"row {idx}: state must be MN, got {state!r}")
        if year is not None and year not in EXPECTED_YEARS:
            errors.append(f"row {idx}: unexpected year {year}")
        if source not in ALLOWED_SOURCES:
            errors.append(f"row {idx}: source must be one of {sorted(ALLOWED_SOURCES)}, got {source!r}")
        if not source_url or source_url.lower() in {"na", "n/a", "none", "placeholder"}:
            errors.append(f"row {idx}: source_url must be non-placeholder")

        if year is not None:
            key = (station, year)
            seen[key] += 1
            station_years.add(key)

        if days_expected is not None:
            if days_expected not in {365, 366}:
                errors.append(f"row {idx}: days_expected must be 365 or 366, got {days_expected}")
        if days_expected is not None and days_observed is not None:
            if days_observed < 0 or days_observed > days_expected:
                errors.append(f"row {idx}: days_observed must be between 0 and days_expected")
        if days_expected and days_observed is not None and completeness_pct is not None:
            recomputed = round((days_observed / days_expected) * 100, 2)
            if abs(recomputed - completeness_pct) > 0.01:
                errors.append(
                    f"row {idx}: completeness_pct mismatch; csv={completeness_pct:.2f}, recomputed={recomputed:.2f}"
                )
            pass_flag = recomputed >= THRESHOLD
            out_row = {
                "station_id": station,
                "year": year,
                "days_expected": days_expected,
                "days_observed": days_observed,
                "completeness_pct": recomputed,
                "pass_98pct": pass_flag,
            }
            if pass_flag:
                admitted_rows.append(out_row)
            else:
                blocked_rows.append(out_row)

    duplicate_keys = [f"{s}:{y}" for (s, y), c in seen.items() if c != 1]
    if duplicate_keys:
        errors.append(f"duplicate or repeated station-year keys: {duplicate_keys}")

    expected_pairs = {(s, y) for s in EXPECTED_STATIONS for y in EXPECTED_YEARS}
    missing_pairs = sorted(expected_pairs - station_years)
    if missing_pairs:
        errors.append(f"missing station-year pairs: {missing_pairs}")

    station_pass_counts = Counter(r["station_id"] for r in admitted_rows)
    admitted_station_set = sorted([s for s in EXPECTED_STATIONS if station_pass_counts[s] == len(EXPECTED_YEARS)])
    blocked_station_set = sorted(EXPECTED_STATIONS - set(admitted_station_set))

    report = {
        "receipt_candidate": "MN-004",
        "status": "PASS" if not errors else "FAIL",
        "csv_path": str(csv_path),
        "csv_sha256": sha256_file(csv_path),
        "validated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rows": len(rows),
        "expected_rows": EXPECTED_ROWS,
        "threshold_pct": THRESHOLD,
        "admitted_station_set": admitted_station_set,
        "blocked_station_set": blocked_station_set,
        "blocked_rows": blocked_rows,
        "errors": errors,
        "guardrails": [
            "No synthetic completeness values.",
            "No interpolation.",
            "No statewide climate claims.",
            "No ACS authorization until MN-004 validation passes."
        ],
    }

    report_path = csv_path.with_name("MN-004_climate_completeness_validation_report.json")
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if errors:
        fail(errors, report_path)

    print("✅ MN004_VALIDATION_PASS")
    print(f"ROWS: {len(rows)}")
    print(f"CSV_SHA256: {report['csv_sha256']}")
    print(f"ADMITTED_STATIONS: {','.join(admitted_station_set)}")
    print(f"BLOCKED_STATIONS: {','.join(blocked_station_set) if blocked_station_set else 'NONE'}")
    print(f"REPORT: {report_path}")


if __name__ == "__main__":
    main()
