#!/usr/bin/env python3
"""Deterministic ALMS post-merge replay harness.

The runner does not simulate runtime behavior or signatures. It delegates each
failure injection to an external runtime adapter and delegates signing to an
external signer command. Missing or malformed adapters fail closed.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

BEDROCK_SHA = "59448d850d355854956cb5834ebef17f7f14c7dc"
ALLOWED_SIGNERS = {"CVD_DAEMON", "COURT_CLERK"}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def invoke_json(command: str, payload: Any, label: str) -> Any:
    argv = shlex.split(command)
    if not argv:
        raise RuntimeError(f"{label} command is empty")
    completed = subprocess.run(
        argv,
        input=canonical_bytes(payload),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"{label} failed with exit {completed.returncode}: {stderr}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{label} returned invalid JSON: {exc}") from exc


def require_runtime_result(raw: Any, failure_id: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise RuntimeError(f"runtime adapter result for {failure_id} is not an object")
    required = {
        "failure_id",
        "observed_state",
        "events",
        "counters_before",
        "counters_after",
    }
    missing = sorted(required - raw.keys())
    if missing:
        raise RuntimeError(f"runtime adapter result for {failure_id} missing: {missing}")
    if raw["failure_id"] != failure_id:
        raise RuntimeError(
            f"runtime adapter returned {raw['failure_id']!r}; expected {failure_id!r}"
        )
    if not isinstance(raw["events"], list) or not raw["events"]:
        raise RuntimeError(f"runtime adapter emitted no events for {failure_id}")
    before = raw["counters_before"]
    after = raw["counters_after"]
    if not isinstance(before, int) or isinstance(before, bool) or before < 0:
        raise RuntimeError(f"invalid counters_before for {failure_id}")
    if not isinstance(after, int) or isinstance(after, bool) or after < 0:
        raise RuntimeError(f"invalid counters_after for {failure_id}")
    return raw


def build_receipt(args: argparse.Namespace) -> dict[str, Any]:
    if args.replay_sha != BEDROCK_SHA:
        raise RuntimeError(
            f"replay SHA must equal constitutional Bedrock root {BEDROCK_SHA}"
        )

    matrix = load_json(args.matrix)
    if matrix.get("bedrock_sha") != BEDROCK_SHA:
        raise RuntimeError("failure matrix is not bound to the Bedrock root")
    vectors = matrix.get("vectors")
    if not isinstance(vectors, list) or [v.get("failure_id") for v in vectors] != [
        "F001",
        "F002",
        "F003",
        "F004",
        "F005",
        "F006",
    ]:
        raise RuntimeError("failure matrix must contain ordered F001-F006 vectors")

    results: list[dict[str, Any]] = []
    for vector in vectors:
        request = {
            "bedrock_sha": BEDROCK_SHA,
            "runtime_root": str(args.runtime_root.resolve()),
            "failure": vector,
        }
        raw = require_runtime_result(
            invoke_json(args.runtime_command, request, f"runtime adapter {vector['failure_id']}"),
            vector["failure_id"],
        )
        monotonic = raw["counters_after"] >= raw["counters_before"]
        passed = raw["observed_state"] == vector["expected_state"] and monotonic
        results.append(
            {
                "failure_id": vector["failure_id"],
                "vector": vector["name"],
                "injected": True,
                "observed_state": raw["observed_state"],
                "expected_state": vector["expected_state"],
                "passed": passed,
                "events": raw["events"],
                "counters_before": raw["counters_before"],
                "counters_after": raw["counters_after"],
                "recovery_action": vector["recovery_action"],
                "blast_radius": vector["blast_radius"],
            }
        )

    aggregate_before = results[0]["counters_before"]
    aggregate_after = results[-1]["counters_after"]
    monotonic = all(
        item["counters_after"] >= item["counters_before"] for item in results
    ) and all(
        results[index]["counters_before"] >= results[index - 1]["counters_after"]
        for index in range(1, len(results))
    )
    green = all(item["passed"] for item in results) and monotonic

    receipt: dict[str, Any] = {
        "cro_id": args.cro_id,
        "replay_root": BEDROCK_SHA,
        "bedrock_sha": BEDROCK_SHA,
        "replay_started_at": args.signed_at,
        "replay_completed_at": args.signed_at,
        "replay_verdict": {
            "status": "GREEN" if green else "RED",
            "reason": (
                "All F001-F006 vectors matched expected states and counters remained monotonic."
                if green
                else "One or more constitutional replay vectors or monotonic counter checks failed."
            ),
        },
        "failure_results": results,
        "monotonic_counters": {
            "before": aggregate_before,
            "after": aggregate_after,
            "monotonic": monotonic,
        },
        "signature_chain": [],
    }

    unsigned = dict(receipt)
    unsigned.pop("signature_chain")
    signature = invoke_json(args.signer_command, unsigned, "HSM signer")
    if not isinstance(signature, dict):
        raise RuntimeError("HSM signer response is not an object")
    signer = signature.get("signer")
    algorithm = signature.get("algorithm")
    value = signature.get("signature")
    if signer not in ALLOWED_SIGNERS:
        raise RuntimeError(f"inadmissible signer identity: {signer!r}")
    if not isinstance(algorithm, str) or not algorithm:
        raise RuntimeError("HSM signer omitted algorithm")
    if not isinstance(value, str) or not value:
        raise RuntimeError("HSM signer omitted signature")
    receipt["signature_chain"] = [
        {
            "signer": signer,
            "algorithm": algorithm,
            "signature": value,
            "signed_at": args.signed_at,
        }
    ]

    schema = load_json(args.schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(receipt), key=lambda error: list(error.path))
    if errors:
        formatted = "; ".join(
            f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise RuntimeError(f"CRO schema validation failed: {formatted}")
    return receipt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-sha", required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cro-id", required=True)
    parser.add_argument("--signed-at", required=True)
    parser.add_argument("--runtime-command", required=True)
    parser.add_argument("--signer-command", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        receipt = build_receipt(args)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(canonical_bytes(receipt))
        return 0 if receipt["replay_verdict"]["status"] == "GREEN" else 1
    except Exception as exc:  # fail closed with one bounded error surface
        print(f"ALMS_REPLAY_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
