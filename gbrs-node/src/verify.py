#!/usr/bin/env python3
"""
GBRS Minimal Viable Verifier (MVV)

Read-only constitutional verifier.

It compares expected projection surfaces against observed live state and emits a
machine-readable verdict. It does not mutate ENS, MCP, files, servers, wallets,
or any routing surface.

Exit codes:
  0  COMPLIANT
  10 DIVERGENT
  20 MIGRATION_REJECTED
  30 FAIL_CLOSED
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from project_agent_caps import project_agent_caps
except Exception:
    project_agent_caps = None


EXIT_CODES = {
    "COMPLIANT": 0,
    "DIVERGENT": 10,
    "MIGRATION_REJECTED": 20,
    "FAIL_CLOSED": 30,
}


def load_json(path: Path) -> Optional[Any]:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def compare_surface(name: str, expected_path: Path, live_path: Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    expected = load_json(expected_path)
    live = load_json(live_path)

    meta = {
        "surface": name,
        "expected_path": str(expected_path),
        "live_path": str(live_path),
        "expected_state_hash": sha256_json(expected) if expected is not None else None,
        "live_state_hash": sha256_json(live) if live is not None else None,
    }

    divergences: List[Dict[str, Any]] = []

    if expected is None and live is None:
        meta["status"] = "ABSENT"
        return divergences, meta

    if expected is None or live is None:
        meta["status"] = "DIVERGENT"
        divergences.append({
            "surface": name,
            "type": "MISSING_SURFACE_STATE",
            "expected_present": expected is not None,
            "live_present": live is not None,
        })
        return divergences, meta

    if expected != live:
        meta["status"] = "DIVERGENT"
        divergences.append({
            "surface": name,
            "type": "STATE_MISMATCH",
            "expected_state_hash": meta["expected_state_hash"],
            "live_state_hash": meta["live_state_hash"],
        })
    else:
        meta["status"] = "COMPLIANT"

    return divergences, meta


def derive_agent_caps_if_possible(fixture: Path) -> Optional[Dict[str, Any]]:
    canonical_index = fixture / "canonical" / "index.json"
    receipts_dir = fixture / "canonical" / "receipts"

    if project_agent_caps is None:
        return None
    if not canonical_index.exists() or not receipts_dir.exists():
        return None

    ts_c = load_json(canonical_index)
    if not isinstance(ts_c, dict):
        return None

    return project_agent_caps(ts_c, receipts_dir)


def verify_fixture(fixture: Path) -> Dict[str, Any]:
    if not fixture.exists() or not fixture.is_dir():
        return {
            "verdict": "FAIL_CLOSED",
            "action": "FAIL_CLOSED",
            "error": f"fixture not found or not a directory: {fixture}",
            "divergences": [],
            "surfaces": [],
        }

    surfaces: List[Dict[str, Any]] = []
    divergences: List[Dict[str, Any]] = []

    surface_specs = [
        ("ENS", fixture / "expected" / "ens.json", fixture / "live_state" / "ens.json"),
        ("MCP", fixture / "expected" / "mcp.json", fixture / "live_state" / "mcp.json"),
        ("AGT_CAPS", fixture / "expected" / "agent_capabilities.json", fixture / "live_state" / "agent_capabilities.json"),
    ]

    for name, expected_path, live_path in surface_specs:
        ds, meta = compare_surface(name, expected_path, live_path)
        divergences.extend(ds)
        surfaces.append(meta)

    # If a fixture provides canonical grant/revoke receipts, verify the expected
    # AGT_CAPS surface itself is derivable from the canonical truth surface.
    derived_agent_caps = derive_agent_caps_if_possible(fixture)
    expected_agent_caps = load_json(fixture / "expected" / "agent_capabilities.json")
    if derived_agent_caps is not None and expected_agent_caps is not None:
        derived_hash = sha256_json(derived_agent_caps)
        expected_hash = sha256_json(expected_agent_caps)
        surfaces.append({
            "surface": "AGT_CAPS_DERIVED",
            "expected_state_hash": expected_hash,
            "derived_state_hash": derived_hash,
            "status": "COMPLIANT" if derived_agent_caps == expected_agent_caps else "DIVERGENT",
        })
        if derived_agent_caps != expected_agent_caps:
            divergences.append({
                "surface": "AGT_CAPS_DERIVED",
                "type": "PROJECTION_MISMATCH",
                "expected_state_hash": expected_hash,
                "derived_state_hash": derived_hash,
            })

    verdict = "COMPLIANT" if not divergences else "DIVERGENT"
    action = "NONE" if verdict == "COMPLIANT" else "ROLLBACK_VISIBLE"

    return {
        "verdict": verdict,
        "action": action,
        "fixture": str(fixture),
        "divergences": divergences,
        "surfaces": surfaces,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="GBRS Minimal Viable Verifier")
    parser.add_argument("--fixture", required=True, help="Path to a GBRS fixture directory")
    args = parser.parse_args()

    result = verify_fixture(Path(args.fixture))
    print(json.dumps(result, indent=2, sort_keys=True))
    return EXIT_CODES.get(result.get("verdict", "FAIL_CLOSED"), 30)


if __name__ == "__main__":
    sys.exit(main())
