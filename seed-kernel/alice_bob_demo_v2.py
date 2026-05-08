#!/usr/bin/env python3
"""
Alice/Bob replay + portability demo for Seed Epistemic Kernel v0.
"""

from pathlib import Path

from export import export_bundle, import_bundle
from kernel import Kernel
from replay import replay

EXPORT_PATH = "alice_export.json"


def reset_demo_files() -> None:
    for path in ["alice.db", "bob.db", EXPORT_PATH]:
        p = Path(path)
        if p.exists():
            p.unlink()


reset_demo_files()

print("=== Alice ===")
alice = Kernel("alice", db_path="alice.db")

source_claim = alice.assert_claim(
    "Q3 revenue from payment system: $12.4M",
    uncertainty=0.05,
    tags=["finance", "q3"],
    source_refs=["finance_db:q3_ledger"],
)

summary_claim = alice.transform(
    input_ids=[source_claim],
    operation="summarize",
    policy="model:claude-3.5",
    output_body="Q3 revenue was $12.4M",
    uncertainty=0.08,
)

export_bundle(
    alice,
    summary_claim,
    EXPORT_PATH,
    viewport_filter={"policies": ["model:claude-3.5"]},
)

print("\n=== Export to Bob ===")

print("\n=== Bob ===")
bob = Kernel("bob", db_path="bob.db")
imported_root = import_bundle(bob, EXPORT_PATH)

wire_claim = bob.assert_claim(
    "Additional wire transfer ledger indicates +$49.2M",
    uncertainty=0.22,
    tags=["wire", "supplemental"],
    source_refs=["wire_ledger:batch_77"],
    branch="bob/wire_inclusive",
)

forked_claim = bob.transform(
    input_ids=[imported_root, wire_claim],
    operation="recalc",
    policy="human:bob",
    output_body="Q3 revenue (wire inclusive) was $61.6M",
    uncertainty=0.18,
    branch="bob/wire_inclusive",
)

print("\n=== Diff (conceptual) ===")
print("Divergence at transform after Alice's summary")
print("Bob's branch: +wire_data → higher total, higher uncertainty")
print()

replay(bob, forked_claim)
