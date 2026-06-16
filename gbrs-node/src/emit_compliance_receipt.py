#!/usr/bin/env python3
"""
GBRS Compliance Receipt Emitter

Transforms verifier output into deterministic, replayable compliance evidence.

This module is intentionally narrow:
- no network access;
- no mutation of truth surfaces;
- no routing surface mutation;
- only writes a receipt artifact when explicitly called.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


SCHEMA_VERSION = "gbrs.compliance_receipt.v1"
DEFAULT_VERIFIER_VERSION = "mvv.v1"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def derive_fixture_id(fixture_path: str) -> str:
    clean = fixture_path.rstrip("/").split("/")[-1]
    return clean or "UNKNOWN_FIXTURE"


def build_compliance_receipt(
    *,
    verifier_output: Dict[str, Any],
    fixture_path: str,
    verifier_commit: str,
    verifier_version: str = DEFAULT_VERIFIER_VERSION,
    expected_verdict: Optional[str] = None,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a deterministic compliance receipt object from verifier output."""

    actual_verdict = verifier_output.get("verdict", "UNKNOWN")
    action = verifier_output.get("action", "UNKNOWN")
    fixture_id = derive_fixture_id(fixture_path)
    expected = expected_verdict or actual_verdict
    passed = actual_verdict == expected

    surfaces = verifier_output.get("surfaces", [])
    divergences = verifier_output.get("divergences", [])

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "receipt_id": None,
        "timestamp": timestamp or utc_now(),
        "fixture_id": fixture_id,
        "fixture_path": fixture_path,
        "verifier": {
            "verifier_commit": verifier_commit,
            "verifier_version": verifier_version,
            "verifier_role": "GBRS_MVV_READ_ONLY"
        },
        "verdict": {
            "expected_verdict": expected,
            "actual_verdict": actual_verdict,
            "action": action,
            "passed": passed
        },
        "evidence": {
            "verifier_output_hash": sha256_json(verifier_output),
            "surfaces": surfaces,
            "divergences": divergences
        },
        "constitutional_boundary": {
            "truth_rule": "Routing is downstream of truth, not upstream of it.",
            "compliance_rule": "A test is not passed until the pass itself becomes replayable evidence.",
            "mutation_policy": "Receipt emission does not mutate truth surfaces or routing surfaces."
        }
    }

    # receipt_id is derived after all stable fields are present except receipt_id.
    tmp = dict(receipt)
    tmp["receipt_id"] = "PENDING"
    receipt_hash = sha256_json(tmp)
    receipt["receipt_id"] = "GBRS_COMPLIANCE_" + receipt_hash.replace("sha256:", "")[:16]
    receipt["receipt_hash"] = sha256_json(receipt)
    return receipt


def emit_compliance_receipt(
    *,
    verifier_output: Dict[str, Any],
    fixture_path: str,
    output_dir: Path,
    verifier_commit: str,
    verifier_version: str = DEFAULT_VERIFIER_VERSION,
    expected_verdict: Optional[str] = None,
    timestamp: Optional[str] = None,
) -> Path:
    """Write a compliance receipt and return its path."""

    output_dir.mkdir(parents=True, exist_ok=True)
    receipt = build_compliance_receipt(
        verifier_output=verifier_output,
        fixture_path=fixture_path,
        verifier_commit=verifier_commit,
        verifier_version=verifier_version,
        expected_verdict=expected_verdict,
        timestamp=timestamp,
    )
    file_name = receipt["receipt_id"] + ".json"
    path = output_dir / file_name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
        f.write("\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit a GBRS compliance receipt")
    parser.add_argument("--verifier-output", required=True, help="Path to verifier output JSON")
    parser.add_argument("--fixture", required=True, help="Fixture path used for the verifier run")
    parser.add_argument("--output-dir", default="compliance_receipts", help="Receipt output directory")
    parser.add_argument("--verifier-commit", required=True, help="Verifier commit SHA")
    parser.add_argument("--verifier-version", default=DEFAULT_VERIFIER_VERSION)
    parser.add_argument("--expected-verdict", default=None)
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()

    verifier_output = load_json(Path(args.verifier_output))
    path = emit_compliance_receipt(
        verifier_output=verifier_output,
        fixture_path=args.fixture,
        output_dir=Path(args.output_dir),
        verifier_commit=args.verifier_commit,
        verifier_version=args.verifier_version,
        expected_verdict=args.expected_verdict,
        timestamp=args.timestamp,
    )
    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
