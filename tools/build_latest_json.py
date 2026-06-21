#!/usr/bin/env python3
"""Build receipts/latest.json from validated ZTVS receipts.

This script is intentionally display-layer only. It does not decide truth.
It expects receipt taxonomy validation to have already passed in CI.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"FATAL: {message}")


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_validator(*paths: Path) -> None:
    cmd = ["node", "scripts/validate-receipt-taxonomy.cjs", *[str(path) for path in paths]]
    subprocess.run(cmd, check=True)


def city_from_target(target_id: str) -> str:
    if target_id.endswith("_001"):
        return target_id[:-4]
    return target_id


def build_latest(librarian: dict, gauntlet: dict, latest_verified_commit: str) -> dict:
    if librarian.get("master_runtime", {}).get("status") != "GREEN":
        fail("Librarian receipt is not GREEN")
    if librarian.get("audit_summary", {}).get("settlement_guard") != "PASS":
        fail("Librarian receipt settlement_guard is not PASS")
    if gauntlet.get("verdict", {}).get("green_claim") is not False:
        fail("Gauntlet receipt attempted green_claim")
    if gauntlet.get("verdict", {}).get("settlement_guard") is not False:
        fail("Gauntlet receipt attempted settlement_guard")

    nodes = []
    for node in librarian.get("nodes", []):
        target_id = node.get("target_id")
        nodes.append({
            "city": city_from_target(target_id),
            "target_id": target_id,
            "state": node.get("state"),
            "verdict": node.get("verdict"),
            "drift": bool(node.get("payload", {}).get("drift_analysis", {}).get("has_drift", False)),
            "schema_version": node.get("schema_version"),
            "evidence_card_sha256": node.get("evidence_card_sha256"),
        })

    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "system_status": "OPERATIONAL_VERIFIED",
        "no_fake_green": "PRESERVED",
        "latest_verified_commit": latest_verified_commit,
        "librarian_receipt": {
            "receipt_id": librarian.get("receipt_id"),
            "verdict": "LIBRARIAN_REPLAY_VALID",
            "authorized_green": True,
            "commit_anchor": librarian.get("master_runtime", {}).get("commit_anchor"),
            "run_id": librarian.get("master_runtime", {}).get("run_id"),
            "signature": librarian.get("signature"),
            "settlement_guard": librarian.get("audit_summary", {}).get("settlement_guard"),
            "drift_detected": librarian.get("audit_summary", {}).get("drift_detected"),
            "node_count": librarian.get("audit_summary", {}).get("node_count"),
        },
        "gauntlet_receipt": {
            "receipt_id": gauntlet.get("receipt_id"),
            "verdict": "GAUNTLET_RUN_VALID",
            "authorized_green": False,
            "commit_anchor": gauntlet.get("commit_anchor"),
            "run_id": gauntlet.get("run_id"),
            "signature": gauntlet.get("signature"),
            "status": gauntlet.get("verdict", {}).get("status"),
            "green_claim": gauntlet.get("verdict", {}).get("green_claim"),
            "settlement_guard": gauntlet.get("verdict", {}).get("settlement_guard"),
            "pytest_returncode": gauntlet.get("verdict", {}).get("pytest_returncode"),
        },
        "taxonomy_gate": {
            "validator": "scripts/validate-receipt-taxonomy.cjs",
            "golden_manifest": "test/fixtures/receipt-taxonomy-golden-manifest.json",
            "golden_regression": "scripts/test-receipt-taxonomy-golden.cjs",
            "expected_output": [
                "GOLDEN_RECEIPT_TAXONOMY_PASS",
                "LIBRARIAN=LIBRARIAN_REPLAY_VALID",
                "GAUNTLET=GAUNTLET_RUN_VALID",
            ],
        },
        "timeline": [
            {"label": "Drift blocked", "commit": "0ddde30", "state": "FATAL_LOCKDOWN_CONFIRMED"},
            {"label": "Clean runtime pass", "commit": "63844ca", "state": "OPERATIONAL_VERIFIED"},
            {"label": "Librarian replay receipt", "receipt_id": librarian.get("receipt_id"), "state": "LIBRARIAN_REPLAY_VALID"},
            {"label": "Gauntlet trace receipt", "receipt_id": gauntlet.get("receipt_id"), "state": "GAUNTLET_RUN_VALID"},
            {"label": "Canonicalization fix verified", "commit": latest_verified_commit[:7], "state": "GAUNTLET_PASS"},
        ],
        "nodes": nodes,
        "constitutional_rules": [
            "Official source is origin, not authority.",
            "Replay loop is proof, not presentation.",
            "Public explorer is access, not validation.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--librarian", required=True)
    parser.add_argument("--gauntlet", required=True)
    parser.add_argument("--latest-verified-commit", required=True)
    parser.add_argument("--output", default="receipts/latest.json")
    args = parser.parse_args()

    librarian_path = Path(args.librarian)
    gauntlet_path = Path(args.gauntlet)
    output_path = Path(args.output)

    run_validator(librarian_path, gauntlet_path)
    latest = build_latest(read_json(librarian_path), read_json(gauntlet_path), args.latest_verified_commit)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(latest, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print(f"LATEST_JSON_WRITTEN={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
