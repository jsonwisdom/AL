#!/usr/bin/env python3
"""
Epistemic Kernel Demo: Alice → Bob → Fork
Full DAG replay demonstration.
"""

import json
from pathlib import Path

from export import export_bundle, import_bundle
from kernel import Kernel
from replay import replay

EXPORT_FILE = "alice_export.json"


def cleanup() -> None:
    for path in ["alice.db", "bob.db", EXPORT_FILE]:
        p = Path(path)
        if p.exists():
            p.unlink()


cleanup()

print("=" * 60)
print("Epistemic Kernel Demo: Alice → Bob → Fork")
print("=" * 60)

# === Alice ===
alice = Kernel("alice", db_path="alice.db")

source_id = alice.assert_claim(
    "Q3 revenue from payment system: $12.4M",
    uncertainty=0.05,
    tags=["finance", "q3"],
    source_refs=["finance_db.extract"],
)

summary_id = alice.transform(
    input_ids=[source_id],
    operation="summarize",
    policy="model:claude-3.5",
    output_body="Q3 revenue was $12.4M",
    params={"prompt": "extract revenue figure", "temperature": 0.1},
    uncertainty=0.08,
)

print("\n--- Alice's Reasoning Graph ---")
replay(alice, summary_id)

export_bundle(
    alice,
    summary_id,
    EXPORT_FILE,
    viewport_filter={"policies": ["model:claude-3.5"]},
)

print(f"\n📤 Alice exported to {EXPORT_FILE}")
print("   viewport: only model transforms visible")

# === Bob ===
bob = Kernel("bob", db_path="bob.db")
imported_root = import_bundle(bob, EXPORT_FILE)

wire_id = bob.assert_claim(
    "Wire transfers excluded from payment system: $49.2M",
    uncertainty=0.15,
    tags=["finance", "q3", "adjustment"],
    source_refs=["treasury_report"],
    branch="bob/wire_inclusive",
)

revised_id = bob.transform(
    input_ids=[imported_root, wire_id],
    operation="recalc",
    policy="human:bob",
    output_body="Q3 revenue (wire inclusive) is $61.6M",
    params={"method": "addition", "note": "contested assumption"},
    uncertainty=0.20,
    branch="bob/wire_inclusive",
)

print("\n--- Bob's Forked Reasoning Graph ---")
replay(bob, revised_id)

print("=" * 60)
print("DIFF: Alice's Summary vs Bob's Revision")
print("=" * 60)
print("Divergence point: summarize → recalc")
print("  Alice output: $12.4M (u=0.05)")
print("  Bob input delta: +$49.2M wire data (u=0.15)")
print("  Bob output: $61.6M (u=0.20)")
print()
print("✅ Kernel demonstrates: forkable, replayable, portable reasoning")
