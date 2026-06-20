"""
Witness hot-reload leak bench v0.1

Purpose:
    Stress the ECC Witness canopy wrapper under repeated hot-reload cycles.

Invariants enforced:
    1. Object Growth Gate
       Wrapped functions counted via gc.get_objects() must return to baseline
       after registry teardown and gc.collect().

    2. Heap Delta Ceiling
       tracemalloc snapshot at iter 10 vs final iter must remain below 5 KB.

    3. Reference Cycle Audit
       Live wrapped functions must not dangle outside the current REGISTRY.skills dict.

Exit codes:
    0 = PASS
    2 = WITNESS_LEAK_OBJECT_GROWTH / WITNESS_LEAK_HEAP_DELTA / WITNESS_LEAK_REF_CYCLE

Doctrine:
    Review harness only. Any leak keeps PR #339 Draft. No runtime-green.

Example:
    python projects/cwaas/ecc-witness/bench_witness_hot_reload_leak_v0_1.py --skills 246 --iterations 1000
"""

from __future__ import annotations

import argparse
import gc
import importlib.util
import json
import os
import sys
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from types import FunctionType
from typing import Any, Dict, List, Set, Tuple

WRAPPER_ATTR = "__witness_wrapped__"
EXIT_LEAK = 2
HEAP_DELTA_LIMIT_BYTES = 5 * 1024
SNAPSHOT_BASELINE_ITERATION = 10


@dataclass
class MockSkill:
    handler: Any
    allowed_tools: List[str]
    sub_agent_id: str = "hot-reload-test-agent"
    tool_id: str | None = None


class MockRegistry:
    def __init__(self, skills: Dict[str, MockSkill]):
        self.skills = skills


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def load_witness_module() -> Any:
    current_dir = Path(__file__).resolve().parent
    module_path = current_dir / "ecc_witness_skill_receipt_v0_1.py"
    spec = importlib.util.spec_from_file_location("ecc_witness_skill_receipt_v0_1", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load witness module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["ecc_witness_skill_receipt_v0_1"] = module
    spec.loader.exec_module(module)
    return module


def make_handler(iteration: int, skill_index: int):
    def handler(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {
            "status": "ok",
            "iteration": iteration,
            "skill_index": skill_index,
            "args": args,
            "kwargs": kwargs,
        }

    handler.__name__ = f"mock_skill_{iteration}_{skill_index}"
    return handler


def make_registry(skill_count: int, iteration: int) -> MockRegistry:
    skills = {
        f"skill_{idx:04d}": MockSkill(
            handler=make_handler(iteration, idx),
            allowed_tools=["read", "write"],
            sub_agent_id=f"agent_{idx % 8}",
        )
        for idx in range(skill_count)
    }
    return MockRegistry(skills)


def count_live_wrapped_functions() -> int:
    count = 0
    for obj in gc.get_objects():
        try:
            if isinstance(obj, FunctionType) and getattr(obj, WRAPPER_ATTR, False):
                count += 1
        except Exception:
            continue
    return count


def live_wrapped_function_ids() -> Set[int]:
    ids: Set[int] = set()
    for obj in gc.get_objects():
        try:
            if isinstance(obj, FunctionType) and getattr(obj, WRAPPER_ATTR, False):
                ids.add(id(obj))
        except Exception:
            continue
    return ids


def current_registry_wrapped_ids(registry: MockRegistry) -> Set[int]:
    ids: Set[int] = set()
    for skill in registry.skills.values():
        handler = getattr(skill, "handler", None)
        if callable(handler) and getattr(handler, WRAPPER_ATTR, False):
            ids.add(id(handler))
    return ids


def check_ref_cycle_audit(registry: MockRegistry) -> Tuple[bool, int]:
    live_ids = live_wrapped_function_ids()
    registry_ids = current_registry_wrapped_ids(registry)
    dangling = live_ids - registry_ids
    return (len(dangling) == 0, len(dangling))


def snapshot_size_bytes(snapshot: tracemalloc.Snapshot) -> int:
    return sum(stat.size for stat in snapshot.statistics("filename"))


def fail(code: str, details: Dict[str, Any]) -> int:
    payload = {
        "bench_type": "WITNESS_HOT_RELOAD_LEAK_BENCH_V0_1",
        "status": "FAIL",
        "failure_class": code,
        "details": details,
    }
    print(canonical_json(payload))
    return EXIT_LEAK


def run_bench(skill_count: int, iterations: int, heap_limit_bytes: int) -> int:
    witness = load_witness_module()

    gc.collect()
    baseline_wrapped = count_live_wrapped_functions()

    tracemalloc.start()
    baseline_snapshot = None
    final_snapshot = None
    last_registry: MockRegistry | None = None

    for iteration in range(1, iterations + 1):
        registry = make_registry(skill_count, iteration)
        manifest = witness.inject_witness_canopy(registry)

        if manifest.get("total_discovered") != skill_count:
            return fail(
                "WITNESS_LEAK_OBJECT_GROWTH",
                {
                    "reason": "registry discovery mismatch",
                    "iteration": iteration,
                    "expected": skill_count,
                    "actual": manifest.get("total_discovered"),
                },
            )

        if manifest.get("total_wrapped") != skill_count:
            return fail(
                "WITNESS_LEAK_OBJECT_GROWTH",
                {
                    "reason": "wrapper coverage mismatch",
                    "iteration": iteration,
                    "expected": skill_count,
                    "actual": manifest.get("total_wrapped"),
                    "unwrapped_ids": manifest.get("unwrapped_ids"),
                },
            )

        ref_ok, dangling_count = check_ref_cycle_audit(registry)
        if not ref_ok:
            return fail(
                "WITNESS_LEAK_REF_CYCLE",
                {
                    "iteration": iteration,
                    "dangling_wrapped_functions": dangling_count,
                    "current_registry_wrapped": len(current_registry_wrapped_ids(registry)),
                },
            )

        if iteration == SNAPSHOT_BASELINE_ITERATION:
            gc.collect()
            baseline_snapshot = tracemalloc.take_snapshot()

        last_registry = registry

        # Simulate hot reload teardown. Only the newest registry may remain alive.
        if iteration != iterations:
            del registry
            gc.collect()

    gc.collect()
    final_snapshot = tracemalloc.take_snapshot()

    if baseline_snapshot is None:
        baseline_snapshot = final_snapshot

    heap_delta = snapshot_size_bytes(final_snapshot) - snapshot_size_bytes(baseline_snapshot)
    if heap_delta > heap_limit_bytes:
        return fail(
            "WITNESS_LEAK_HEAP_DELTA",
            {
                "baseline_iteration": SNAPSHOT_BASELINE_ITERATION,
                "iterations": iterations,
                "heap_delta_bytes": heap_delta,
                "heap_limit_bytes": heap_limit_bytes,
            },
        )

    # Drop the final registry and demand that wrappers return to baseline.
    last_registry = None
    gc.collect()
    final_wrapped = count_live_wrapped_functions()
    object_growth = final_wrapped - baseline_wrapped

    if object_growth != 0:
        return fail(
            "WITNESS_LEAK_OBJECT_GROWTH",
            {
                "baseline_wrapped_functions": baseline_wrapped,
                "final_wrapped_functions": final_wrapped,
                "object_growth": object_growth,
                "skills": skill_count,
                "iterations": iterations,
            },
        )

    payload = {
        "bench_type": "WITNESS_HOT_RELOAD_LEAK_BENCH_V0_1",
        "status": "PASS",
        "skills": skill_count,
        "iterations": iterations,
        "baseline_wrapped_functions": baseline_wrapped,
        "final_wrapped_functions": final_wrapped,
        "object_growth": object_growth,
        "heap_delta_bytes": heap_delta,
        "heap_limit_bytes": heap_limit_bytes,
        "reference_cycle_audit": "PASS",
    }
    print(canonical_json(payload))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Stress ECC Witness wrapper under hot-reload cycles.")
    parser.add_argument("--skills", type=int, default=246)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--heap-limit-bytes", type=int, default=HEAP_DELTA_LIMIT_BYTES)
    args = parser.parse_args()

    if args.skills < 1:
        raise SystemExit("skills must be >= 1")
    if args.iterations < SNAPSHOT_BASELINE_ITERATION:
        raise SystemExit(f"iterations must be >= {SNAPSHOT_BASELINE_ITERATION}")

    return run_bench(
        skill_count=args.skills,
        iterations=args.iterations,
        heap_limit_bytes=args.heap_limit_bytes,
    )


if __name__ == "__main__":
    raise SystemExit(main())
