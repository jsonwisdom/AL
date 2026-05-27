#!/usr/bin/env python3
"""Dual-witness replay membrane runner.

Implements DUAL_WITNESS_REPLAY_RUNNER_SPEC_V1 as a deterministic CLI.
Authority: NONE. This runner validates only replay-visible receipt shape and
lineage binding. It does not claim social, legal, or cryptographic authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

EXPECTED_RED = "PR_256"
EXPECTED_GREEN = "PR_257"
ISSUER_ID = "membrane/preflight/v1"
INVARIANT_SET = {
    "version": "DUAL_WITNESS_INVARIANT_SET_V1",
    "invariants": [
        "LINEAGE_PROVENANCE_INVARIANT",
        "FAIL_CLOSED_INVARIANT",
        "REPLAY_IDENTITY_INVARIANT",
        "RECEIPT_BINDING_INVARIANT",
    ],
}

EXIT_SUCCESS = 0
EXIT_RED_FALSE_POSITIVE = 1
EXIT_GREEN_FALSE_NEGATIVE = 2
EXIT_INTERNAL_ERROR = 3
EXIT_NON_DETERMINISM = 4


@dataclass(frozen=True)
class PRInput:
    pr: str
    payload_path: str
    payload_bytes: bytes
    receipt_path: Optional[str]
    receipt: Optional[dict[str, Any]]


@dataclass(frozen=True)
class Decision:
    pr: str
    decision: str
    reason: str
    receipt_present: bool
    payload_hash: str
    expected_lineage_hash: str
    receipt_lineage_hash: Optional[str]


def sha256_hex(data: bytes) -> str:
    return "0x" + hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def invariant_set_hash() -> str:
    return sha256_hex(canonical_json_bytes(INVARIANT_SET))


def read_bytes(path: str) -> bytes:
    return Path(path).read_bytes()


def read_receipt(path: Optional[str]) -> Optional[dict[str, Any]]:
    if path is None:
        return None
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("receipt must be a JSON object")
    return value


def validate_receipt_shape(receipt: dict[str, Any]) -> tuple[bool, str]:
    required = ["id", "lineage_hash", "issued_at", "issuer_id", "signature"]
    missing = [field for field in required if field not in receipt]
    if missing:
        return False, "RECEIPT_MISSING_FIELDS:" + ",".join(missing)
    if receipt.get("issuer_id") != ISSUER_ID:
        return False, "RECEIPT_ISSUER_MISMATCH"
    for field in required:
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            return False, "RECEIPT_FIELD_INVALID:" + field
    return True, "RECEIPT_SHAPE_VALID"


def validate_pr(pr_input: PRInput) -> Decision:
    payload_hash = sha256_hex(pr_input.payload_bytes)
    expected_lineage_hash = payload_hash

    if pr_input.receipt is None:
        return Decision(
            pr=pr_input.pr,
            decision="REJECT",
            reason="MISSING_PREFLIGHT_RECEIPT",
            receipt_present=False,
            payload_hash=payload_hash,
            expected_lineage_hash=expected_lineage_hash,
            receipt_lineage_hash=None,
        )

    shape_ok, shape_reason = validate_receipt_shape(pr_input.receipt)
    receipt_lineage_hash = pr_input.receipt.get("lineage_hash")
    if not shape_ok:
        return Decision(
            pr=pr_input.pr,
            decision="REJECT",
            reason=shape_reason,
            receipt_present=True,
            payload_hash=payload_hash,
            expected_lineage_hash=expected_lineage_hash,
            receipt_lineage_hash=receipt_lineage_hash if isinstance(receipt_lineage_hash, str) else None,
        )

    if receipt_lineage_hash != expected_lineage_hash:
        return Decision(
            pr=pr_input.pr,
            decision="REJECT",
            reason="LINEAGE_HASH_MISMATCH",
            receipt_present=True,
            payload_hash=payload_hash,
            expected_lineage_hash=expected_lineage_hash,
            receipt_lineage_hash=receipt_lineage_hash,
        )

    return Decision(
        pr=pr_input.pr,
        decision="ADMIT",
        reason="VALID_PREFLIGHT_LINEAGE_RECEIPT",
        receipt_present=True,
        payload_hash=payload_hash,
        expected_lineage_hash=expected_lineage_hash,
        receipt_lineage_hash=receipt_lineage_hash,
    )


def run_once(red: PRInput, green: PRInput) -> dict[str, Any]:
    red_decision = validate_pr(red)
    green_decision = validate_pr(green)

    if red_decision.decision == "ADMIT":
        exit_code = EXIT_RED_FALSE_POSITIVE
        exit_reason = "RED_PATH_FALSE_POSITIVE"
    elif green_decision.decision == "REJECT":
        exit_code = EXIT_GREEN_FALSE_NEGATIVE
        exit_reason = "GREEN_PATH_FALSE_NEGATIVE"
    else:
        exit_code = EXIT_SUCCESS
        exit_reason = "DUAL_WITNESS_SUCCESS"

    return {
        "exit_code": exit_code,
        "exit_reason": exit_reason,
        "red": asdict(red_decision),
        "green": asdict(green_decision),
        "invariant_set_hash": invariant_set_hash(),
    }


def stable_projection(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "exit_code": result["exit_code"],
        "exit_reason": result["exit_reason"],
        "red": result["red"],
        "green": result["green"],
        "invariant_set_hash": result["invariant_set_hash"],
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def write_receipt_log(path: Path, decision: dict[str, Any]) -> None:
    path.write_text(json.dumps(decision, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def build_inputs(args: argparse.Namespace) -> tuple[PRInput, PRInput]:
    if args.red != EXPECTED_RED:
        raise ValueError(f"--red must be {EXPECTED_RED}")
    if args.green != EXPECTED_GREEN:
        raise ValueError(f"--green must be {EXPECTED_GREEN}")

    red = PRInput(
        pr=args.red,
        payload_path=args.red_payload,
        payload_bytes=read_bytes(args.red_payload),
        receipt_path=args.red_receipt,
        receipt=read_receipt(args.red_receipt),
    )
    green = PRInput(
        pr=args.green,
        payload_path=args.green_payload,
        payload_bytes=read_bytes(args.green_payload),
        receipt_path=args.green_receipt,
        receipt=read_receipt(args.green_receipt),
    )
    return red, green


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="replay_membrane")
    parser.add_argument("--red", required=True)
    parser.add_argument("--green", required=True)
    parser.add_argument("--red-payload", required=True)
    parser.add_argument("--green-payload", required=True)
    parser.add_argument("--red-receipt")
    parser.add_argument("--green-receipt")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        red, green = build_inputs(args)
        first = run_once(red, green)
        second = run_once(red, green)

        deterministic = stable_projection(first) == stable_projection(second)
        if not deterministic:
            first = dict(first)
            first["exit_code"] = EXIT_NON_DETERMINISM
            first["exit_reason"] = "NON_DETERMINISM_DETECTED"

        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "run_id": "replay-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "cli": "replay_membrane",
            "exit_code": first["exit_code"],
            "exit_reason": first["exit_reason"],
            "red": first["red"],
            "green": first["green"],
            "invariant_set_hash": first["invariant_set_hash"],
            "deterministic": deterministic,
        }

        comparison_report = {
            "proof": "SAME_INVARIANT_SET_HANDLED_BOTH_PATHS",
            "red_decision": first["red"]["decision"],
            "green_decision": first["green"]["decision"],
            "opposite_lawful_outcomes": first["red"]["decision"] == "REJECT" and first["green"]["decision"] == "ADMIT",
            "authority": False,
            "interpretation": False,
            "invariant_set_hash": first["invariant_set_hash"],
        }

        write_receipt_log(output_dir / "PR_256_receipt.log", first["red"])
        write_receipt_log(output_dir / "PR_257_receipt.log", first["green"])
        write_json(output_dir / "comparison_report.json", comparison_report)
        write_json(output_dir / "replay_manifest.json", manifest)

        if args.verbose:
            print(json.dumps(manifest, sort_keys=True, indent=2))

        return int(first["exit_code"])
    except Exception as exc:  # noqa: BLE001 - CLI must convert all failures to exit 3.
        sys.stderr.write(f"HARNESS_INTERNAL_ERROR: {exc}\n")
        return EXIT_INTERNAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
