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
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

EXPECTED_RED = "PR_256"
EXPECTED_GREEN = "PR_257"
ISSUER_ID = "membrane/preflight/v1"
SELF_EXCLUDED = "sha256:SELF_EXCLUDED"

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


def sha256_profile(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return sha256_hex(canonical_json_bytes(value))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def assert_profile_hash(profile: dict[str, Any]) -> str:
    declared = profile.get("profile_hash")
    if not isinstance(declared, str):
        raise ValueError("profile_hash missing or invalid")

    excluded = dict(profile)
    excluded["profile_hash"] = SELF_EXCLUDED
    computed = sha256_profile(canonical_json_bytes(excluded))

    if computed != declared:
        raise ValueError(f"profile hash mismatch for {profile.get('profile_id')}: {computed} != {declared}")

    return computed


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_profiles() -> tuple[dict[str, Any], dict[str, Any], str, str]:
    root = repo_root()

    invariant_profile = load_json(root / "profiles" / "INVARIANT_PROFILE_V1.json")
    canon_profile = load_json(root / "profiles" / "CANON_PROFILE_V1.json")

    invariant_hash = assert_profile_hash(invariant_profile)
    canon_hash = assert_profile_hash(canon_profile)

    return invariant_profile, canon_profile, invariant_hash, canon_hash


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


def validate_pr(
    pr_input: PRInput,
    invariant_profile: dict[str, Any],
    canon_profile: dict[str, Any],
    invariant_profile_hash: str,
    canon_profile_hash: str,
) -> Decision:
    _ = invariant_profile
    _ = canon_profile
    _ = invariant_profile_hash
    _ = canon_profile_hash

    payload_hash = sha256_hex(pr_input.payload_bytes)
    expected_lineage_hash = payload_hash

    if pr_input.receipt is None:
        return Decision(
            pr_input.pr,
            "REJECT",
            "MISSING_PREFLIGHT_RECEIPT",
            False,
            payload_hash,
            expected_lineage_hash,
            None,
        )

    shape_ok, shape_reason = validate_receipt_shape(pr_input.receipt)
    receipt_lineage_hash = pr_input.receipt.get("lineage_hash")

    if not shape_ok:
        return Decision(
            pr_input.pr,
            "REJECT",
            shape_reason,
            True,
            payload_hash,
            expected_lineage_hash,
            receipt_lineage_hash if isinstance(receipt_lineage_hash, str) else None,
        )

    if receipt_lineage_hash != expected_lineage_hash:
        return Decision(
            pr_input.pr,
            "REJECT",
            "LINEAGE_HASH_MISMATCH",
            True,
            payload_hash,
            expected_lineage_hash,
            receipt_lineage_hash,
        )

    return Decision(
        pr_input.pr,
        "ADMIT",
        "VALID_PREFLIGHT_LINEAGE_RECEIPT",
        True,
        payload_hash,
        expected_lineage_hash,
        receipt_lineage_hash,
    )


def run_once(
    red: PRInput,
    green: PRInput,
    invariant_profile: dict[str, Any],
    canon_profile: dict[str, Any],
    invariant_profile_hash: str,
    canon_profile_hash: str,
) -> dict[str, Any]:
    red_decision = validate_pr(red, invariant_profile, canon_profile, invariant_profile_hash, canon_profile_hash)
    green_decision = validate_pr(green, invariant_profile, canon_profile, invariant_profile_hash, canon_profile_hash)

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
        "profile_hash_invariant": invariant_profile_hash,
        "profile_hash_canon": canon_profile_hash,
        "authority": False,
    }


def stable_projection(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "exit_code": result["exit_code"],
        "exit_reason": result["exit_reason"],
        "red": result["red"],
        "green": result["green"],
        "profile_hash_invariant": result["profile_hash_invariant"],
        "profile_hash_canon": result["profile_hash_canon"],
        "authority": result["authority"],
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

    return (
        PRInput(args.red, args.red_payload, read_bytes(args.red_payload), args.red_receipt, read_receipt(args.red_receipt)),
        PRInput(args.green, args.green_payload, read_bytes(args.green_payload), args.green_receipt, read_receipt(args.green_receipt)),
    )


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

        invariant_profile, canon_profile, invariant_hash, canon_hash = load_profiles()
        red, green = build_inputs(args)

        run_1 = run_once(red, green, invariant_profile, canon_profile, invariant_hash, canon_hash)
        run_2 = run_once(red, green, invariant_profile, canon_profile, invariant_hash, canon_hash)

        stable_1 = stable_projection(run_1)
        stable_2 = stable_projection(run_2)

        manifest_hash_1 = canonical_hash(stable_1)
        manifest_hash_2 = canonical_hash(stable_2)

        trace_hash_red_1 = canonical_hash(stable_1["red"])
        trace_hash_red_2 = canonical_hash(stable_2["red"])

        trace_hash_green_1 = canonical_hash(stable_1["green"])
        trace_hash_green_2 = canonical_hash(stable_2["green"])

        deterministic = (
            manifest_hash_1 == manifest_hash_2
            and trace_hash_red_1 == trace_hash_red_2
            and trace_hash_green_1 == trace_hash_green_2
        )

        if not deterministic:
            run_1 = dict(run_1)
            run_1["exit_code"] = EXIT_NON_DETERMINISM
            run_1["exit_reason"] = "NON_DETERMINISM_DETECTED"

        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        determinism_audit_report = {
            "deterministic": deterministic,
            "manifest_hash_1": manifest_hash_1,
            "manifest_hash_2": manifest_hash_2,
            "trace_hash_red_1": trace_hash_red_1,
            "trace_hash_red_2": trace_hash_red_2,
            "trace_hash_green_1": trace_hash_green_1,
            "trace_hash_green_2": trace_hash_green_2,
            "invariant_profile_hash": invariant_hash,
            "canon_profile_hash": canon_hash,
            "authority": False,
        }

        manifest = {
            "run_id": "replay-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "cli": "replay_membrane",
            "exit_code": run_1["exit_code"],
            "exit_reason": run_1["exit_reason"],
            "red": run_1["red"],
            "green": run_1["green"],
            "profile_hash_invariant": invariant_hash,
            "profile_hash_canon": canon_hash,
            "determinism_audit_report": determinism_audit_report,
        }

        comparison_report = {
            "proof": "SAME_INVARIANT_SET_HANDLED_BOTH_PATHS",
            "red_decision": run_1["red"]["decision"],
            "green_decision": run_1["green"]["decision"],
            "opposite_lawful_outcomes": run_1["red"]["decision"] == "REJECT" and run_1["green"]["decision"] == "ADMIT",
            "authority": False,
            "interpretation": False,
            "profile_hash_invariant": invariant_hash,
            "profile_hash_canon": canon_hash,
        }

        write_receipt_log(output_dir / "PR_256_receipt.log", run_1["red"])
        write_receipt_log(output_dir / "PR_257_receipt.log", run_1["green"])
        write_json(output_dir / "comparison_report.json", comparison_report)
        write_json(output_dir / "determinism_audit_report.json", determinism_audit_report)
        write_json(output_dir / "replay_manifest.json", manifest)

        if args.verbose:
            print(json.dumps(manifest, sort_keys=True, indent=2))

        return int(run_1["exit_code"])

    except Exception as exc:
        sys.stderr.write(f"HARNESS_INTERNAL_ERROR: {exc}\n")
        return EXIT_INTERNAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
