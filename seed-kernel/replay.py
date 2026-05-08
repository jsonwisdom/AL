#!/usr/bin/env python3
"""
Full DAG replay walker for Seed Epistemic Kernel v0.
"""

from __future__ import annotations

import json
from collections import deque
from typing import Deque, Set, Tuple

from kernel import Kernel


def replay(kernel: Kernel, root_claim_id: str, max_depth: int = 30) -> Set[str]:
    """Replay a claim's transform ancestry as a visible DAG walk."""
    print(f"\n🔎 Replaying DAG for {root_claim_id[:12]}...\n")

    visited: Set[str] = set()
    queue: Deque[Tuple[str, int, str]] = deque([(root_claim_id, 0, "")])

    while queue:
        claim_id, depth, prefix = queue.popleft()
        if claim_id in visited:
            print(f"{prefix}↺ already visited {claim_id[:12]}...")
            continue
        if depth > max_depth:
            print(f"{prefix}⚠️ max depth reached at {claim_id[:12]}...")
            continue

        visited.add(claim_id)
        claim = kernel.get_claim(claim_id)
        if not claim:
            print(f"{prefix}⚠️ missing claim {claim_id[:12]}...")
            continue

        body = claim["body"]
        if len(body) > 80:
            body = body[:80] + "..."

        print(f"{prefix}📍 {claim_id[:12]} | {body}")
        print(f"{prefix}   asserted by {claim['asserted_by']} (u={claim['uncertainty']})")

        rows = kernel.conn.execute(
            "SELECT data FROM transforms WHERE output_claim_id = ? ORDER BY id",
            (claim_id,),
        ).fetchall()

        for row in rows:
            transform = json.loads(row["data"])
            print(
                f"{prefix}   ← {transform['operation']} via {transform['policy']} "
                f"(tx {transform['id'][:12]})"
            )
            for input_claim_id in transform.get("input_claim_ids", []):
                queue.append((input_claim_id, depth + 1, prefix + "  │ "))

    print(f"\n✅ DAG replay complete ({len(visited)} nodes)\n")
    return visited
