#!/usr/bin/env python3
"""
Convert an operator-supplied BaseScan token transfer CSV into the JAYWISDOM
inception replay CSV format.

Read-only. No crawling. No chain write. No wallet. No revenue claim.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

OUTPUT_HEADERS = [
    "blockNumber",
    "timestamp_utc",
    "txHash",
    "from_address",
    "to_address",
    "value_raw",
    "value_formatted",
    "method",
    "source",
]

COMMON_FIELD_ALIASES = {
    "blockNumber": ["Blockno", "Block Number", "Block", "blockNumber", "block_number"],
    "timestamp": ["UnixTimestamp", "DateTime (UTC)", "DateTime", "Timestamp", "timestamp_utc"],
    "txHash": ["Txhash", "Transaction Hash", "Hash", "txHash", "hash"],
    "from_address": ["From", "from", "from_address"],
    "to_address": ["To", "to", "to_address"],
    "value_formatted": ["Quantity", "TokenValue", "Value", "value_formatted"],
    "value_raw": ["value_raw", "Raw Value", "TokenValueRaw", "ValueRaw"],
    "method": ["Method", "method"],
}


def pick(row: dict[str, str], aliases: list[str], default: str = "") -> str:
    for alias in aliases:
        if alias in row and str(row[alias]).strip() != "":
            return str(row[alias]).strip()
    return default


def parse_timestamp(value: str) -> str:
    value = value.strip()
    if not value:
        return ""

    if value.isdigit():
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%b-%d-%Y %I:%M:%S %p %z",
        "%b-%d-%Y %I:%M:%S %p +UTC",
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(value, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        except ValueError:
            continue

    return value


def decimal_to_raw(value: str, decimals: int) -> str:
    value = value.replace(",", "").strip()
    if not value:
        return "0"
    try:
        amount = Decimal(value)
    except InvalidOperation:
        return "0"
    return str(int(amount * (Decimal(10) ** decimals)))


def convert(input_path: Path, output_path: Path, decimals: int, source: str) -> int:
    with input_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    out_rows: list[dict[str, str]] = []
    for row in rows:
        raw_value = pick(row, COMMON_FIELD_ALIASES["value_raw"])
        formatted = pick(row, COMMON_FIELD_ALIASES["value_formatted"])
        if not raw_value:
            raw_value = decimal_to_raw(formatted, decimals)

        out_rows.append({
            "blockNumber": pick(row, COMMON_FIELD_ALIASES["blockNumber"]),
            "timestamp_utc": parse_timestamp(pick(row, COMMON_FIELD_ALIASES["timestamp"])),
            "txHash": pick(row, COMMON_FIELD_ALIASES["txHash"]),
            "from_address": pick(row, COMMON_FIELD_ALIASES["from_address"]),
            "to_address": pick(row, COMMON_FIELD_ALIASES["to_address"]),
            "value_raw": raw_value,
            "value_formatted": formatted,
            "method": pick(row, COMMON_FIELD_ALIASES["method"], "Transfer") or "Transfer",
            "source": source,
        })

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        writer.writerows(out_rows)

    return len(out_rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert BaseScan token transfer CSV to JAYWISDOM replay CSV")
    parser.add_argument("--input", required=True, help="Operator-supplied BaseScan CSV export")
    parser.add_argument("--output", default="docs/zora/fixtures/JAYWISDOM_first50_transfers.csv")
    parser.add_argument("--decimals", type=int, default=18, help="Token decimals for raw value calculation if raw field is absent")
    parser.add_argument("--source", default="basescan_export")
    args = parser.parse_args()

    count = convert(Path(args.input), Path(args.output), args.decimals, args.source)
    print(f"converted_rows={count}")
    print(f"output={args.output}")
    print("chain_write=false wallet_control=false signing=false broadcast=false revenue_confirmed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
