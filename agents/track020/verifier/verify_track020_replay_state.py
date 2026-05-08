#!/usr/bin/env python3
"""
TRACK_020 Replay State Verifier v1

Deterministically classifies TRACK_020 artifacts as:
- CANDIDATE
- REGISTERED_SCHEMA
- ATTESTATION

Then emits a verdict_code without making chain calls.
This is an offline membrane checker: Git candidate != registered schema != attestation != mainnet activation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple


VALID_KINDS = {"CANDIDATE", "REGISTERED_SCHEMA", "ATTESTATION"}


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def truthy(v: Any) -> bool:
    return v is True or (isinstance(v, str) and v.lower() in {"true", "present", "verified", "confirmed"})


def classify(inp: Dict[str, Any]) -> str:
    schema_uid = inp.get("schema_uid")
    attestation_uid = inp.get("attestation_uid")

    if attestation_uid:
        return "ATTESTATION"
    if schema_uid:
        return "REGISTERED_SCHEMA"
    return "CANDIDATE"


def verdict(kind: str, inp: Dict[str, Any]) -> str:
    operator_signature_present = truthy(inp.get("operator_signature_present")) or bool(inp.get("operator_signature"))
    track019_verified = truthy(inp.get("TRACK_019_TESTNET_PROOF_verified")) or truthy(inp.get("track019_testnet_proof_verified"))
    payload_matches = inp.get("payload_matches_candidate", True)
    schema_payload_matches = inp.get("registration_payload_matches_candidate", True)

    if kind == "CANDIDATE":
        return "CANDIDATE_ONLY"

    if kind == "REGISTERED_SCHEMA":
        if not operator_signature_present:
            return "FAIL_OPERATOR_SIGNATURE_REQUIRED"
        if schema_payload_matches is False:
            return "FAIL_SCHEMA_PAYLOAD_DRIFT"
        return "REGISTERED_SCHEMA_ONLY"

    if kind == "ATTESTATION":
        if not track019_verified:
            return "MAINNET_ACTIVATION_BLOCKED"
        if not operator_signature_present:
            return "FAIL_OPERATOR_SIGNATURE_REQUIRED"
        if payload_matches is False:
            return "FAIL_PAYLOAD_DRIFT"
        return "ATTESTATION_VERIFIED"

    return "FAIL_UNKNOWN_KIND"


def allowed_mainnet_enable(kind: str, verdict_code: str, inp: Dict[str, Any]) -> bool:
    return (
        kind == "ATTESTATION"
        and verdict_code == "ATTESTATION_VERIFIED"
        and inp.get("TRACK_020_status") == "BLOCKED_PENDING_TRACK_019_RUNTIME_PROOF"
    )


def verify_candidate_hash(inp: Dict[str, Any]) -> Tuple[bool, str | None]:
    artifact_path = inp.get("artifact_path")
    expected = inp.get("artifact_sha256")
    if not artifact_path or not expected:
        return True, None
    actual = sha256_file(artifact_path)
    return actual == expected, actual


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify TRACK_020 replay state classification and verdict.")
    parser.add_argument("input", help="JSON input describing git/chain state")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON")
    args = parser.parse_args()

    inp = load_json(args.input)
    kind = classify(inp)
    hash_ok, actual_artifact_sha256 = verify_candidate_hash(inp)

    if kind not in VALID_KINDS:
        verdict_code = "FAIL_UNKNOWN_KIND"
    elif not hash_ok:
        verdict_code = "FAIL_ARTIFACT_HASH_MISMATCH"
    else:
        verdict_code = verdict(kind, inp)

    out = {
        "artifact": "TRACK_020_REPLAY_STATE_VERIFIER_OUTPUT_V1",
        "input_file": args.input,
        "classification": kind,
        "verdict_code": verdict_code,
        "artifact_sha256_observed": actual_artifact_sha256,
        "mainnet_enable_allowed": allowed_mainnet_enable(kind, verdict_code, inp),
        "no_ghost_anchor": verdict_code in {
            "CANDIDATE_ONLY",
            "REGISTERED_SCHEMA_ONLY",
            "MAINNET_ACTIVATION_BLOCKED",
            "ATTESTATION_VERIFIED",
        },
    }

    print(json.dumps(out, indent=2 if args.pretty else None, sort_keys=True))

    hard_fail = verdict_code.startswith("FAIL_")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
