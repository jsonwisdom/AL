#!/usr/bin/env python3
"""
EAS Control Receipt V1 verifier.

Schema is law.
Verifier is executor.
CI is gate.
Network is witness.

This verifier is intentionally deterministic and local-first. It does not fetch live EAS,
RPC, GraphQL, or external URLs. Field runners may create cached observations; CI only
verifies replayable local artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "eas_control_receipt_v1.schema.json"
LINEAGE_INDEX_PATH = ROOT / "testdata" / "lineage-index.json"
FL001_LINEAGE_DIGEST = "60efc1b3e76c69439f74d2813e02d6f63b8e8869edfc6bfb94a18c04b4d20d9a"

ANCHORED_STATUSES = {"ANCHORED_CONTROL_SAMPLE", "VERIFIED"}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_lineage_index() -> Dict[str, Any]:
    if not LINEAGE_INDEX_PATH.exists():
        return {
            "root_lineage_digest": FL001_LINEAGE_DIGEST,
            "receipts": {
                "FED-AI-2026-FL-001": {
                    "lineage_digest": FL001_LINEAGE_DIGEST,
                    "children": []
                }
            }
        }
    return load_json(LINEAGE_INDEX_PATH)


def canonical_bytes(obj: Dict[str, Any]) -> bytes:
    """Deterministic compact JSON bytes for hashing.

    canonical_hash is excluded to avoid self-reference.
    verdict_codes and notes are excluded from canonical receipt identity because they
    are verifier output / commentary, not evidence identity.
    """
    excluded = {"canonical_hash", "verdict_codes", "notes"}
    stable = {k: v for k, v in obj.items() if k not in excluded}
    return json.dumps(stable, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_prefixed(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def max_severity(severities: List[str]) -> str:
    order = {"GREEN": 0, "YELLOW": 1, "ORANGE": 2, "RED": 3}
    return max(severities, key=lambda s: order.get(s, 3)) if severities else "GREEN"


def schema_errors(schema: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    if jsonschema is None:
        return ["JSONSCHEMA_LIBRARY_MISSING"]
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(receipt), key=lambda e: list(e.path))
    codes: List[str] = []
    for err in errors:
        if err.validator == "required":
            codes.append("SCHEMA_REQUIRED_FIELD_MISSING")
        elif err.validator == "additionalProperties":
            codes.append("SCHEMA_ADDITIONAL_FIELD")
        elif err.validator == "const" and list(err.path) == ["chain_id"]:
            codes.append("EAS_WRONG_CHAIN_ID")
        elif err.validator == "const" and list(err.path) == ["chain"]:
            codes.append("EAS_WRONG_CHAIN")
        elif list(err.path) == ["uid"]:
            codes.append("EAS_UID_INVALID_FORMAT")
        elif list(err.path) == ["tx_hash"]:
            codes.append("EAS_TX_HASH_INVALID_FORMAT")
        elif list(err.path) == ["canonical_hash"]:
            codes.append("CANONICAL_HASH_MISSING")
        else:
            codes.append("INVALID_SCHEMA")
    return sorted(set(codes))


def lineage_checks(receipt: Dict[str, Any], lineage_index: Dict[str, Any]) -> List[str]:
    codes: List[str] = []
    receipt_id = receipt.get("receipt_id")
    parent_digest = receipt.get("parent_lineage_digest")
    receipt_digest = receipt.get("lineage_digest")
    receipts = lineage_index.get("receipts", {})

    if not parent_digest:
        return ["LINEAGE_PARENT_EMPTY"]

    parent_id = None
    for candidate_id, candidate in receipts.items():
        if candidate.get("lineage_digest") == parent_digest:
            parent_id = candidate_id
            break

    if parent_id is None:
        codes.append("LINEAGE_ORPHANED")
        return codes

    children = receipts.get(parent_id, {}).get("children", [])
    if receipt_id not in children:
        codes.append("LINEAGE_CLAIM_INVALID")

    indexed = receipts.get(receipt_id)
    if indexed is not None:
        if indexed.get("parent_lineage_digest") != parent_digest:
            codes.append("LINEAGE_CLAIM_INVALID")
        if receipt_digest and indexed.get("lineage_digest") != receipt_digest:
            codes.append("CANONICAL_HASH_MISMATCH")

    return sorted(set(codes))


def constitutional_checks(receipt: Dict[str, Any], lineage_index: Dict[str, Any]) -> List[str]:
    codes: List[str] = []
    status = receipt.get("status")

    codes.extend(lineage_checks(receipt, lineage_index))

    if receipt.get("chain") != "Base":
        codes.append("EAS_WRONG_CHAIN")
    if receipt.get("chain_id") != 8453:
        codes.append("EAS_WRONG_CHAIN_ID")

    if status in ANCHORED_STATUSES:
        for key, code in [
            ("uid", "EAS_UID_MISSING"),
            ("schema_uid", "SCHEMA_UID_MISSING"),
            ("tx_hash", "EAS_TX_HASH_MISSING"),
            ("source_url", "ANCHOR_WITHOUT_EVIDENCE"),
            ("artifact_hash", "ANCHOR_WITHOUT_EVIDENCE"),
        ]:
            if not receipt.get(key):
                codes.append(code)
        if receipt.get("replay_status") != "PASS":
            codes.append("REPLAY_FALSE_PASS")

    if status == "PENDING_FETCH":
        for key in ("uid", "tx_hash", "artifact_hash"):
            if receipt.get(key):
                codes.append("ANCHOR_WITHOUT_EVIDENCE")

    expected_canonical = receipt.get("canonical_hash")
    if not expected_canonical:
        codes.append("CANONICAL_HASH_MISSING")
    else:
        actual = sha256_prefixed(canonical_bytes(receipt))
        if actual != expected_canonical:
            codes.append("CANONICAL_HASH_MISMATCH")

    return sorted(set(codes))


def classify(codes: List[str], receipt: Dict[str, Any]) -> Tuple[bool, str, str]:
    status = receipt.get("status")

    red_codes = {
        "JSONSCHEMA_LIBRARY_MISSING",
        "SCHEMA_REQUIRED_FIELD_MISSING",
        "SCHEMA_ADDITIONAL_FIELD",
        "INVALID_SCHEMA",
        "EAS_UID_INVALID_FORMAT",
        "EAS_TX_HASH_INVALID_FORMAT",
        "EAS_WRONG_CHAIN_ID",
        "EAS_WRONG_CHAIN",
        "LINEAGE_PARENT_EMPTY",
        "LINEAGE_ORPHANED",
        "LINEAGE_CLAIM_INVALID",
        "LINEAGE_PARENT_MUTATION_ATTEMPT",
        "CANONICAL_HASH_MISSING",
        "CANONICAL_HASH_MISMATCH",
        "REPLAY_NON_DETERMINISTIC",
        "REPLAY_FALSE_PASS",
        "ANCHOR_WITHOUT_EVIDENCE",
        "METADATA_ONLY_CHECKSUM",
        "URL_DEAD_NO_EVIDENCE",
        "RETROACTIVE_PROMOTION_ATTEMPT",
    }
    yellow_codes = {"EAS_UID_MISSING", "EAS_TX_HASH_MISSING", "SCHEMA_UID_MISSING", "SCHEMA_HASH_DRIFT"}
    orange_codes = {"URL_DEAD_ARCHIVE_AVAILABLE"}

    severities = []
    if any(c in red_codes for c in codes):
        severities.append("RED")
    if any(c in orange_codes for c in codes):
        severities.append("ORANGE")
    if any(c in yellow_codes for c in codes):
        severities.append("YELLOW" if status == "PENDING_FETCH" else "RED")

    severity = max_severity(severities)
    valid = not codes and receipt.get("replay_status") == "PASS" and severity == "GREEN"
    replay_status = "PASS" if valid else "FAIL"
    return valid, severity, replay_status


def verify(path: Path) -> Dict[str, Any]:
    schema = load_json(SCHEMA_PATH)
    lineage_index = load_lineage_index()
    receipt = load_json(path)
    codes = sorted(set(schema_errors(schema, receipt) + constitutional_checks(receipt, lineage_index)))
    valid, severity, replay_status = classify(codes, receipt)

    actual_hash = sha256_prefixed(canonical_bytes(receipt)) if "canonical_hash" in receipt else None

    return {
        "receipt_id": receipt.get("receipt_id"),
        "valid": valid,
        "severity": severity,
        "codes": codes,
        "canonical_hash": actual_hash,
        "lineage_digest": receipt.get("parent_lineage_digest") if "LINEAGE_ORPHANED" not in codes else None,
        "replay_status": replay_status,
        "path": str(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify EAS Control Receipt V1 fixture(s).")
    parser.add_argument("paths", nargs="+", help="Receipt JSON files to verify")
    parser.add_argument("--expect-invalid", action="store_true", help="Return success only if all fixtures fail")
    parser.add_argument("--json", action="store_true", help="Emit JSON array")
    args = parser.parse_args()

    results = [verify(Path(p)) for p in args.paths]

    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for result in results:
            print(json.dumps(result, sort_keys=True))

    if args.expect_invalid:
        return 0 if all(not r["valid"] and r["severity"] == "RED" for r in results) else 1
    return 0 if all(r["valid"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
