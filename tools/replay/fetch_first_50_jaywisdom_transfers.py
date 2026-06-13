#!/usr/bin/env python3
"""
Fetch first 50 ERC-20 Transfer logs for the JAYWISDOM token via public RPC.

Read-only RPC only: eth_getLogs, eth_getBlockByNumber, eth_call optional elsewhere.
No wallet. No signer. No broadcast. No revenue claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

DEFAULT_CONTRACT = "0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F"
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
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


def rpc(rpc_url: str, method: str, params: list[Any]) -> Any:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    req = urllib.request.Request(
        rpc_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    if "error" in data:
        raise RuntimeError(data["error"])
    return data["result"]


def topic_to_address(topic: str) -> str:
    return "0x" + topic[-40:]


def hex_to_int(value: str) -> int:
    return int(value, 16)


def format_units(raw: int, decimals: int) -> str:
    scale = Decimal(10) ** decimals
    return format(Decimal(raw) / scale, "f")


def block_timestamp(rpc_url: str, block_number: int, cache: dict[int, str]) -> str:
    if block_number in cache:
        return cache[block_number]
    block = rpc(rpc_url, "eth_getBlockByNumber", [hex(block_number), False])
    timestamp = datetime.fromtimestamp(hex_to_int(block["timestamp"]), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    cache[block_number] = timestamp
    return timestamp


def fetch_logs_chunked(rpc_url: str, contract: str, from_block: int, to_block: int, chunk_size: int) -> list[dict[str, Any]]:
    all_logs: list[dict[str, Any]] = []
    start = from_block
    while start <= to_block:
        end = min(start + chunk_size - 1, to_block)
        logs = rpc(rpc_url, "eth_getLogs", [{
            "fromBlock": hex(start),
            "toBlock": hex(end),
            "address": contract,
            "topics": [TRANSFER_TOPIC],
        }])
        all_logs.extend(logs)
        start = end + 1
        time.sleep(0.05)
    return all_logs


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch first 50 JAYWISDOM Transfer logs via read-only RPC")
    parser.add_argument("--rpc-url", required=True, help="Base RPC URL")
    parser.add_argument("--contract", default=DEFAULT_CONTRACT)
    parser.add_argument("--from-block", type=int, default=0)
    parser.add_argument("--to-block", type=int, default=0, help="0 means latest")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--chunk-size", type=int, default=50000)
    parser.add_argument("--decimals", type=int, default=18)
    parser.add_argument("--output", default="docs/zora/fixtures/JAYWISDOM_first50_transfers.csv")
    args = parser.parse_args()

    latest = hex_to_int(rpc(args.rpc_url, "eth_blockNumber", []))
    to_block = latest if args.to_block == 0 else args.to_block

    logs = fetch_logs_chunked(args.rpc_url, args.contract, args.from_block, to_block, args.chunk_size)
    logs.sort(key=lambda item: (hex_to_int(item["blockNumber"]), hex_to_int(item["logIndex"])))
    selected = logs[: args.limit]

    ts_cache: dict[int, str] = {}
    rows: list[dict[str, str]] = []
    for log in selected:
        block_no = hex_to_int(log["blockNumber"])
        raw_value = hex_to_int(log["data"])
        rows.append({
            "blockNumber": str(block_no),
            "timestamp_utc": block_timestamp(args.rpc_url, block_no, ts_cache),
            "txHash": log["transactionHash"],
            "from_address": topic_to_address(log["topics"][1]),
            "to_address": topic_to_address(log["topics"][2]),
            "value_raw": str(raw_value),
            "value_formatted": format_units(raw_value, args.decimals),
            "method": "Transfer",
            "source": "rpc_getLogs",
        })

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({
        "receipt_id": "JAYWISDOM_FIRST50_RPC_FETCH_V0_1",
        "network": "Base",
        "contract": args.contract,
        "from_block": args.from_block,
        "to_block": to_block,
        "latest_block_observed": latest,
        "transfer_logs_found": len(logs),
        "rows_written": len(rows),
        "output": str(output),
        "chain_write": False,
        "wallet_control": False,
        "signing": False,
        "broadcast": False,
        "revenue_confirmed": False,
        "authority": False,
        "no_fake_green": True,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
