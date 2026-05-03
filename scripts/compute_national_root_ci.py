#!/usr/bin/env python3
"""ALMS CI national root recompute.

GitHub Direct only. No on-chain claims.

Reads known state claim wrappers, verifies frozen source snapshot hashes,
computes per-state roots where possible, then computes a national Merkle
commitment over explicit state statuses.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "alms" / "national"

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
    state_results = [compute_state(state, claims) for state, claims in STATES.items()]
    national_leaves = []
    for s in state_results:
        material = "|".join([s["state"], s.get("state_root") or "NULL", s["status"], s["version"]])
        national_leaves.append(sha256_text(material))

    verdict = "PASS" if all(s["status"] == "PASS" for s in state_results) else "INDETERMINATE"
    out = {
        "artifact": "CI_NATIONAL_ROOT_RECOMPUTE",
        "version": "US_SNAPSHOT_2026-05-03",
        "status": verdict,
        "national_root": merkle_root(national_leaves),
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "states": state_results,
        "leaf_hashes": sorted(national_leaves),
        "boundary": "GitHub CI recompute only. Not Base/EAS anchored. National PASS requires every state PASS.",
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "national_root_ci_latest.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
