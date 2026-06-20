"""
ToolGate fsync latency bench v0.1

Purpose:
    Benchmark receipt-write overhead for the ECC Witness ToolGate canopy.

Modes:
    fsync_on      : append + fsync every receipt
    fsync_off     : append without fsync
    wal_batch     : buffered batch append + fsync per batch

Doctrine:
    Review harness only. Does not change runtime security posture.
    Runtime v0.1 remains fail-closed with fsync enabled.

Example:
    python bench_toolgate_fsync_latency_v0_1.py --agents 50 --events-per-agent 200 --mode fsync_on
    python bench_toolgate_fsync_latency_v0_1.py --agents 50 --events-per-agent 200 --mode fsync_off
    python bench_toolgate_fsync_latency_v0_1.py --agents 50 --events-per-agent 200 --mode wal_batch --batch-size 25
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import statistics
import tempfile
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Literal

BenchMode = Literal["fsync_on", "fsync_off", "wal_batch"]


@dataclass(frozen=True)
class BenchReceipt:
    receipt_type: str
    schema_version: str
    mode: str
    agent_id: int
    event_id: int
    input_hash: str
    timestamp_ns: int


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * pct))
    return ordered[index]


def write_line(path: Path, line: str, fsync_enabled: bool) -> None:
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, line.encode("utf-8"))
        if fsync_enabled:
            os.fsync(fd)
    finally:
        os.close(fd)


def run_agent(agent_id: int, events_per_agent: int, path: Path, mode: BenchMode, batch_size: int) -> List[float]:
    latencies_ms: List[float] = []
    batch_lines: List[str] = []

    for event_id in range(events_per_agent):
        receipt = BenchReceipt(
            receipt_type="TOOLGATE_FSYNC_BENCH_RECEIPT_V0_1",
            schema_version="0.1",
            mode=mode,
            agent_id=agent_id,
            event_id=event_id,
            input_hash=sha256_obj({"agent_id": agent_id, "event_id": event_id}),
            timestamp_ns=time.time_ns(),
        )
        line = canonical_json({"receipt_hash": sha256_obj(asdict(receipt)), "body": asdict(receipt)}) + "\n"

        start_ns = time.perf_counter_ns()
        if mode == "fsync_on":
            write_line(path, line, fsync_enabled=True)
        elif mode == "fsync_off":
            write_line(path, line, fsync_enabled=False)
        elif mode == "wal_batch":
            batch_lines.append(line)
            if len(batch_lines) >= batch_size:
                write_line(path, "".join(batch_lines), fsync_enabled=True)
                batch_lines.clear()
        else:
            raise ValueError(f"unknown mode: {mode}")
        end_ns = time.perf_counter_ns()
        latencies_ms.append((end_ns - start_ns) / 1_000_000)

    if mode == "wal_batch" and batch_lines:
        start_ns = time.perf_counter_ns()
        write_line(path, "".join(batch_lines), fsync_enabled=True)
        end_ns = time.perf_counter_ns()
        latencies_ms.append((end_ns - start_ns) / 1_000_000)

    return latencies_ms


def run_bench(agents: int, events_per_agent: int, mode: BenchMode, batch_size: int, output_path: Path) -> Dict[str, object]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    started_ns = time.perf_counter_ns()
    all_latencies: List[float] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=agents) as executor:
        futures = [
            executor.submit(run_agent, agent_id, events_per_agent, output_path, mode, batch_size)
            for agent_id in range(agents)
        ]
        for future in concurrent.futures.as_completed(futures):
            all_latencies.extend(future.result())

    ended_ns = time.perf_counter_ns()
    duration_s = (ended_ns - started_ns) / 1_000_000_000
    total_events = agents * events_per_agent
    file_size_bytes = output_path.stat().st_size if output_path.exists() else 0

    result = {
        "bench_type": "TOOLGATE_FSYNC_LATENCY_BENCH_V0_1",
        "mode": mode,
        "agents": agents,
        "events_per_agent": events_per_agent,
        "total_events": total_events,
        "batch_size": batch_size if mode == "wal_batch" else None,
        "duration_seconds": duration_s,
        "throughput_events_per_second": total_events / duration_s if duration_s else 0,
        "latency_ms": {
            "count": len(all_latencies),
            "min": min(all_latencies) if all_latencies else 0,
            "mean": statistics.fmean(all_latencies) if all_latencies else 0,
            "median": statistics.median(all_latencies) if all_latencies else 0,
            "p50": percentile(all_latencies, 0.50),
            "p95": percentile(all_latencies, 0.95),
            "p99": percentile(all_latencies, 0.99),
            "max": max(all_latencies) if all_latencies else 0,
        },
        "output_path": str(output_path),
        "output_bytes": file_size_bytes,
        "result_hash": None,
    }
    result["result_hash"] = sha256_obj(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark ECC Witness ToolGate receipt fsync overhead.")
    parser.add_argument("--agents", type=int, default=10, choices=[10, 50, 200])
    parser.add_argument("--events-per-agent", type=int, default=100)
    parser.add_argument("--mode", choices=["fsync_on", "fsync_off", "wal_batch"], required=True)
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    if args.mode == "wal_batch" and args.batch_size < 1:
        raise SystemExit("batch-size must be >= 1")

    output_path = Path(args.output) if args.output else Path(tempfile.gettempdir()) / f"toolgate_fsync_bench_{args.mode}.jsonl"
    result = run_bench(
        agents=args.agents,
        events_per_agent=args.events_per_agent,
        mode=args.mode,
        batch_size=args.batch_size,
        output_path=output_path,
    )
    print(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
