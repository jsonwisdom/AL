#!/usr/bin/env python3
"""
JAYWISDOM inception replay validator.

Read-only validator for an operator-supplied BaseScan/export/RPC CSV.
Optional RPC mode reads ERC-20 totalSupply() via eth_call.

No wallet. No signing. No broadcast. No authority claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.request
from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation
from typing import Any

REQUIRED_HEADERS = [
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

DEFAULT_CONTRACT = "0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F"
TOTAL_SUPPLY_SELECTOR = "0x18160ddd"
ZERO_HASH = "0x" + "0" * 64
ZERO_ADDRESS = "0x" + "0" * 40
PLACEHOLDER_MARKERS = {
    "",
    "-",
    "n/a",
    "na",
    "null",
    "none",
    "placeholder",
    "synthetic",
    "fake",
    "padded_insufficient_events",
    "insufficient_events",
    "deployment_ts",
    "formatted",
    "source",
    "ts2",
}


@dataclass
class ValidationFinding:
    kind: str
    severity: str
    message: str


@dataclass
class ValidationReceipt:
    receipt_id: str
    csv_path: str
    network: str
    contract: str
    source_mode: str
    requested_limit: int
    required_headers_present: bool
    missing_headers: list[str]
    row_count: int
    short_event_set: bool
    missing_event_slots: int
    padding_used: bool
    placeholder_rows_detected: int
    earliest_row: dict[str, Any] | None
    latest_row: dict[str, Any] | None
    value_raw_sum: str
    value_formatted_sum: str
    rpc_total_supply_raw: str | None
    csv_raw_sum_matches_rpc_total_supply: bool | None
    findings: list[ValidationFinding]
    ruling: dict[str, Any]


def parse_int(value: str, default: int = 0) -> int:
    value = str(value or "").strip().replace(",", "")
    try:
        return int(value)
    except ValueError:
        return default


def parse_decimal(value: str) -> Decimal:
    value = str(value or "0").strip().replace(",", "")
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(0)


def row_sort_key(row: dict[str, str]) -> tuple[int, str, str]:
    return (
        parse_int(row.get("blockNumber", "0")),
        row.get("timestamp_utc", ""),
        row.get("txHash", ""),
    )


def read_csv_rows(path: str) -> tuple[list[str], list[dict[str, str]]]:
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        return headers, list(reader)


def normalized(value: str) -> str:
    return str(value or "").strip().lower()


def looks_like_placeholder(row: dict[str, str]) -> bool:
    for key in REQUIRED_HEADERS:
        value = normalized(row.get(key, ""))
        if value in PLACEHOLDER_MARKERS:
            return True
        if value.startswith("0xcreator") or value.startswith("0xsender") or value.startswith("0xrecipient"):
            return True

    tx_hash = normalized(row.get("txHash", ""))
    from_address = normalized(row.get("from_address", ""))
    to_address = normalized(row.get("to_address", ""))
    source = normalized(row.get("source", ""))

    if tx_hash == ZERO_HASH and from_address == ZERO_ADDRESS and to_address == ZERO_ADDRESS:
        return True
    if "padded" in source or "insufficient" in source or "placeholder" in source:
        return True
    return False


def rpc_eth_call_total_supply(rpc_url: str, contract: str) -> str:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [
            {
                "to": contract,
                "data": TOTAL_SUPPLY_SELECTOR,
            },
            "latest",
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        rpc_url,
        data=data,
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        parsed = json.loads(response.read().decode("utf-8"))
    if "error" in parsed:
        raise RuntimeError(parsed["error"])
    result = parsed.get("result")
    if not isinstance(result, str) or not result.startswith("0x"):
        raise RuntimeError(f"Invalid eth_call result: {result!r}")
    return str(int(result, 16))


def build_receipt(args: argparse.Namespace) -> ValidationReceipt:
    findings: list[ValidationFinding] = []
    headers, rows = read_csv_rows(args.csv)
    missing = [header for header in REQUIRED_HEADERS if header not in headers]

    if missing:
        findings.append(ValidationFinding(
            kind="missing_headers",
            severity="high",
            message=f"Missing required headers: {', '.join(missing)}",
        ))

    if not rows:
        findings.append(ValidationFinding(
            kind="empty_csv",
            severity="medium",
            message="CSV has headers but no transfer rows. Replay remains pending real feed.",
        ))

    if len(rows) > args.requested_limit:
        findings.append(ValidationFinding(
            kind="row_count_exceeds_requested_limit",
            severity="high",
            message=f"CSV has {len(rows)} rows but requested limit is {args.requested_limit}.",
        ))

    placeholder_count = sum(1 for row in rows if looks_like_placeholder(row))
    padding_used = placeholder_count > 0
    if padding_used:
        findings.append(ValidationFinding(
            kind="placeholder_or_padding_rows_detected",
            severity="high",
            message=f"Detected {placeholder_count} placeholder/padded/synthetic row(s). CSV must contain real transfer events only.",
        ))

    sorted_rows = sorted(rows, key=row_sort_key)
    earliest = sorted_rows[0] if sorted_rows else None
    latest = sorted_rows[-1] if sorted_rows else None

    raw_sum = sum(parse_int(row.get("value_raw", "0")) for row in rows)
    formatted_sum = sum(parse_decimal(row.get("value_formatted", "0")) for row in rows)

    sources = sorted({row.get("source", "").strip() or "UNSPECIFIED" for row in rows})
    if "UNSPECIFIED" in sources:
        findings.append(ValidationFinding(
            kind="missing_source",
            severity="medium",
            message="One or more rows are missing a source value.",
        ))

    rpc_total: str | None = None
    matches: bool | None = None
    rpc_url = args.rpc_url or os.environ.get("BASE_RPC_URL")
    if rpc_url:
        try:
            rpc_total = rpc_eth_call_total_supply(rpc_url, args.contract)
            matches = str(raw_sum) == rpc_total
            if not matches:
                findings.append(ValidationFinding(
                    kind="supply_mismatch_or_partial_csv",
                    severity="medium",
                    message="CSV value_raw sum does not equal RPC totalSupply(). This may mean the CSV is partial, filtered, or value_raw is not a mint/burn supply ledger.",
                ))
        except Exception as exc:  # noqa: BLE001
            findings.append(ValidationFinding(
                kind="rpc_total_supply_failed",
                severity="medium",
                message=f"RPC totalSupply read failed: {exc}",
            ))

    source_mode = "CSV_ONLY" if not rpc_url else "CSV_PLUS_OPTIONAL_RPC"
    short_event_set = 0 < len(rows) < args.requested_limit
    missing_event_slots = max(args.requested_limit - len(rows), 0)
    high_findings = [finding for finding in findings if finding.severity == "high"]
    replay_ready = bool(rows) and not high_findings and len(missing) == 0

    return ValidationReceipt(
        receipt_id="JAYWISDOM_REAL_FEED_REPLAY_VALIDATION_V0_2",
        csv_path=args.csv,
        network=args.network,
        contract=args.contract,
        source_mode=source_mode,
        requested_limit=args.requested_limit,
        required_headers_present=len(missing) == 0,
        missing_headers=missing,
        row_count=len(rows),
        short_event_set=short_event_set,
        missing_event_slots=missing_event_slots,
        padding_used=padding_used,
        placeholder_rows_detected=placeholder_count,
        earliest_row=earliest,
        latest_row=latest,
        value_raw_sum=str(raw_sum),
        value_formatted_sum=str(formatted_sum),
        rpc_total_supply_raw=rpc_total,
        csv_raw_sum_matches_rpc_total_supply=matches,
        findings=findings,
        ruling={
            "real_feed_present": bool(rows) and not padding_used,
            "csv_rows_operator_supplied": True,
            "replay_ready": replay_ready,
            "inception_candidate_present": bool(earliest and len(missing) == 0 and not padding_used),
            "short_event_set_valid": short_event_set and not padding_used,
            "padding_allowed": False,
            "rpc_total_supply_checked": rpc_total is not None,
            "transfer_count_verified": False,
            "full_history_verified": False,
            "revenue_confirmed": False,
            "chain_write": False,
            "wallet_control": False,
            "signing": False,
            "broadcast": False,
            "authority": False,
            "no_fake_green": True,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate JAYWISDOM real-feed replay CSV")
    parser.add_argument("--csv", required=True, help="CSV path with BaseScan/export/RPC rows")
    parser.add_argument("--contract", default=DEFAULT_CONTRACT, help="ERC-20 contract address")
    parser.add_argument("--network", default="Base", help="Network label")
    parser.add_argument("--requested-limit", type=int, default=50, help="Requested real-event row limit")
    parser.add_argument("--rpc-url", default=None, help="Optional Base RPC URL for read-only totalSupply check")
    args = parser.parse_args()

    receipt = build_receipt(args)
    print(json.dumps(asdict(receipt), indent=2, sort_keys=True))

    has_high = any(f.severity == "high" for f in receipt.findings)
    return 1 if has_high else 0


if __name__ == "__main__":
    sys.exit(main())
