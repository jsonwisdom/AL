#!/usr/bin/env python3
"""
Deterministic replay walker for Seed Epistemic Kernel v0.
"""

from __future__ import annotations

from typing import Set

from kernel import Kernel


def replay(kernel: Kernel, claim_id: str, seen: Set[str] | None = None, depth: int = 0) -> None:
    seen = seen or set()

    if claim_id in seen:
        print("  " * depth + f"↺ already visited {claim_id[:12]}...")
        return

    seen.add(claim_id)

    claim = kernel.get_claim(claim_id)
    if not claim:
        print("  " * depth + f"❌ missing claim {claim_id}")
        return

    if depth == 0:
        print(f"🔎 Replaying {claim_id[:12]}...")

    transform = kernel.get_transform_for_output(claim_id)

    if not transform:
        print(
            "  " * depth
            + f"✓ root claim by {claim['asserted_by']} | "
            + f"uncertainty={claim['uncertainty']}"
        )
        return

    print(
        "  " * depth
        + f"← {transform['operation']} via {transform['policy']} "
        + f"(transform {transform['id'][:12]}...)"
    )

    for input_claim_id in transform["input_claim_ids"]:
        replay(kernel, input_claim_id, seen=seen, depth=depth + 1)

    if depth == 0:
        print("✅ Replay complete")
