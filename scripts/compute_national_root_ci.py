#!/usr/bin/env python3
"""ALMS CI national root recompute.

GitHub Direct only. No on-chain claims.

Reads known state claim wrappers, verifies frozen source snapshot hashes,
computes per-state roots where possible, then computes a national Merkle
commitment over explicit state statuses. Also writes the GitHub Direct
runtime anchor receipt so the CI output loop is complete.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "alms" / "national"
ANCHOR_DIR = ROOT / "alms" / "anchors" / "runtime"

STATES = {
    "MN": [
        {
            "id": "MN-BUDGET-2026-01",
            "claim": "fixtures/mn/mn_budget_2026_claim.json",
            "source": "fixtures/mn/sources/mmb_budget_snapshot_2026-05-03.txt",
            "version": "MN_SNAPSHOT_2026-05-03",
        },
        {
            "id": "MN-BUDGET-RESERVE-2026-01",
            "claim": "fixtures/mn/mn_budget_reserve_2026_claim.json",
            "source": "fixtures/mn/sources/mmb_budget_reserve_snapshot_2026-05-03.txt",
            "version": "MN_SNAPSHOT_2026-05-03",
        },
    ],
    "AL": [
        {
            "id": "AL-BUDGET-2026-01",
            "claim": "fixtures/al/al_budget_2026_claim.json",
            "source": "fixtures/al/sources/al_budget_snapshot_2026-05-03.txt",
            "version": "AL_BOOTSTRAP_2026-05-03",
        }
    ],
    "TX": [
        {
            "id": "TX-BUDGET-2026-01",
            "claim": "fixtures/tx/tx_budget_2026_claim.json",
            "source": "fixtures/tx/sources/tx_budget_snapshot_2026-05-03.txt",
            "version": "TX_BOOTSTRAP_2026-05-03",
        }
    ],
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def read_json(path: Path):
    return json.loads(path.read_text())


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        return sha256_text("")
    level = sorted(x.replace("sha256:", "") for x in leaves)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(hashlib.sha256(bytes.fromhex(left) + bytes.fromhex(right)).hexdigest())
        level = nxt
    return "sha256:" + level[0]


def compute_state(state: str, claims: list[dict]) -> dict:
    results = []
    blockers = []
    matched_hashes = []
    version = claims[0]["version"] if claims else f"{state}_EMPTY"

    for item in claims:
        claim_path = ROOT / item["claim"]
        source_path = ROOT / item["source"]
        try:
            claim = read_json(claim_path)
            expected = claim.get("hash", "UNSET")
            computed = sha256_bytes(source_path.read_bytes())
            match = isinstance(expected, str) and expected.startswith("sha256:") and expected == computed
            if not match:
                blockers.append({
                    "id": item["id"],
                    "reason": "expected hash missing or mismatch",
                    "expected_hash": expected,
                    "computed_hash": computed,
                })
            else:
                matched_hashes.append(computed)
            results.append({
                "id": item["id"],
                "claim_path": item["claim"],
                "source_path": item["source"],
                "expected_hash": expected,
                "computed_hash": computed,
                "hash_match": match,
            })
        except Exception as exc:
            blockers.append({"id": item.get("id", "UNKNOWN"), "reason": str(exc)})
            results.append({"id": item.get("id", "UNKNOWN"), "hash_match": False, "error": str(exc)})

    status = "PASS" if results and not blockers else "INDETERMINATE"
    return {
        "state": state,
        "version": version,
        "status": status,
        "state_root": merkle_root(matched_hashes) if status == "PASS" else None,
        "claim_count": len(results),
        "matched_count": len([r for r in results if r.get("hash_match")]),
        "claims": results,
        "blockers": blockers,
    }


def main() -> int:
    generated_utc = now_utc()
    state_results = [compute_state(state, claims) for state, claims in STATES.items()]
    national_leaves = []
    for s in state_results:
        material = "|".join([s["state"], s.get("state_root") or "NULL", s["status"], s["version"]])
        national_leaves.append(sha256_text(material))

    verdict = "PASS" if all(s["status"] == "PASS" for s in state_results) else "INDETERMINATE"
    national_root = merkle_root(national_leaves)
    out = {
        "artifact": "CI_NATIONAL_ROOT_RECOMPUTE",
        "version": "US_SNAPSHOT_2026-05-03",
        "status": verdict,
        "national_root": national_root,
        "generated_utc": generated_utc,
        "states": state_results,
        "leaf_hashes": sorted(national_leaves),
        "boundary": "GitHub CI recompute only. Not Base/EAS anchored. National PASS requires every state PASS.",
    }

    runtime_anchor = {
        "artifact": "GITHUB_DIRECT_ANCHOR_STATE",
        "status": "GITHUB_ANCHORED_ONLY",
        "onchain_status": "NOT_REGISTERED",
        "public_label": "GITHUB_ANCHORED_ONLY",
        "national_root": national_root,
        "national_status": verdict,
        "commit_sha": os.getenv("GITHUB_SHA", "LOCAL_OR_UNKNOWN"),
        "repo": os.getenv("GITHUB_REPOSITORY", "jsonwisdom/AL"),
        "run_id": os.getenv("GITHUB_RUN_ID", "LOCAL_OR_UNKNOWN"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", "LOCAL_OR_UNKNOWN"),
        "created_utc": generated_utc,
        "blocked_claims": [
            "ANCHORED_ON_BASE",
            "EAS_ATTESTED",
            "ENS_COMPLETE",
            "VERIFIED_NATIONAL_ROOT",
            "ONCHAIN_CONFIRMED"
        ],
        "boundary": "GitHub Direct anchor only. No wallet signature, no Base/EAS transaction, no ENS update."
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ANCHOR_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "national_root_ci_latest.json").write_text(json.dumps(out, indent=2) + "\n")
    (ANCHOR_DIR / "github_direct_anchor_state.json").write_text(json.dumps(runtime_anchor, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
