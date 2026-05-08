#!/usr/bin/env python3
"""
Portable subgraph export/import for Seed Epistemic Kernel v0.

This is the first MVP portability primitive.
It exports a root claim plus the visible transform ancestry needed for replay.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from kernel import Kernel


def _policy_allowed(transform: Dict[str, Any], viewport_filter: Optional[Dict[str, Any]]) -> bool:
    if not viewport_filter:
        return True
    policies = viewport_filter.get("policies")
    if policies is None:
        return True
    return transform.get("policy") in policies


def export_bundle(
    kernel: Kernel,
    root_claim_id: str,
    path: str,
    viewport_filter: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Export a claim and its visible transform ancestry as a portable JSON bundle."""
    bundle: Dict[str, Any] = {
        "kernel_bundle": "SEED_EPISTEMIC_KERNEL_EXPORT_V0",
        "root": root_claim_id,
        "claims": {},
        "transforms": {},
        "viewport": viewport_filter or {},
    }

    visited_claims: Set[str] = set()
    visited_transforms: Set[str] = set()
    queue: List[str] = [root_claim_id]

    while queue:
        claim_id = queue.pop(0)
        if claim_id in visited_claims:
            continue
        visited_claims.add(claim_id)

        claim = kernel.get_claim(claim_id)
        if not claim:
            continue
        bundle["claims"][claim_id] = claim

        transform = kernel.get_transform_for_output(claim_id)
        if not transform:
            continue

        transform_id = transform["id"]
        if transform_id in visited_transforms:
            continue
        visited_transforms.add(transform_id)

        if _policy_allowed(transform, viewport_filter):
            bundle["transforms"][transform_id] = transform
            queue.extend(transform.get("input_claim_ids", []))

    Path(path).write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
    print(
        f"📤 Exported {path} "
        f"({len(bundle['claims'])} claims, {len(bundle['transforms'])} transforms)"
    )
    return bundle


def import_bundle(kernel: Kernel, path: str) -> str:
    """Import a portable JSON bundle into a local kernel and return its root claim."""
    bundle = json.loads(Path(path).read_text(encoding="utf-8"))

    if bundle.get("kernel_bundle") != "SEED_EPISTEMIC_KERNEL_EXPORT_V0":
        raise ValueError("unsupported bundle type")

    for claim_id, claim in bundle.get("claims", {}).items():
        kernel.conn.execute(
            "INSERT OR IGNORE INTO claims VALUES (?, ?)",
            (claim_id, kernel._canonical(claim).decode("utf-8")),
        )

    for transform_id, transform in bundle.get("transforms", {}).items():
        kernel.conn.execute(
            "INSERT OR IGNORE INTO transforms VALUES (?, ?, ?)",
            (
                transform_id,
                transform["output_claim_id"],
                kernel._canonical(transform).decode("utf-8"),
            ),
        )

    kernel.conn.commit()
    print(
        f"📥 Imported {len(bundle.get('claims', {}))} claims, "
        f"{len(bundle.get('transforms', {}))} transforms ← {path}"
    )
    return bundle["root"]
