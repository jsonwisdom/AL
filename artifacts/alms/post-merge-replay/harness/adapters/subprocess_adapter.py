#!/usr/bin/env python3
"""Fail-closed subprocess adapter for the ALMS replay harness."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

BEDROCK_SHA = "59448d850d355854956cb5834ebef17f7f14c7dc"
EXPECTED_IDS = ["F001", "F002", "F003", "F004", "F005", "F006"]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_vector_subprocess(
    runtime: Path, failure: dict[str, Any], bedrock_sha: str
) -> dict[str, Any]:
    if bedrock_sha != BEDROCK_SHA:
        raise ValueError(f"bedrock SHA must equal {BEDROCK_SHA}")
    completed = subprocess.run(
        [
            str(runtime),
            "--vector",
            failure["failure_id"],
            "--sha",
            bedrock_sha,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"runtime exited {completed.returncode} for {failure['failure_id']}: "
            f"{completed.stderr.strip()}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"runtime returned invalid JSON for {failure['failure_id']}: {exc}"
        ) from exc
    if not isinstance(result, dict):
        raise RuntimeError("runtime result must be an object")
    return result


def run_all_vectors(
    matrix: list[dict[str, Any]],
    bedrock_sha: str,
    runtime: Path,
    protocol: dict[str, Any],
) -> dict[str, Any]:
    if bedrock_sha != BEDROCK_SHA:
        raise ValueError(f"bedrock SHA must equal {BEDROCK_SHA}")
    ids = [item.get("failure_id") for item in matrix]
    if ids != EXPECTED_IDS:
        raise ValueError("matrix must contain ordered F001-F006 vectors")

    vectors: list[dict[str, Any]] = []
    for failure in matrix:
        raw = run_vector_subprocess(runtime, failure, bedrock_sha)
        vector = {
            "failure_id": failure["failure_id"],
            "name": failure["name"],
            "injected": raw.get("injected"),
            "observed_state": raw.get("observed_state"),
            "expected_state": failure["expected_state"],
            "events": raw.get("events"),
            "counter_before": raw.get("counter_before"),
            "counter_after": raw.get("counter_after"),
        }
        vectors.append(vector)

    output = {
        "adapter_version": "1.0.0",
        "bedrock_sha": bedrock_sha,
        "vectors": vectors,
    }
    errors = sorted(
        Draft202012Validator(protocol).iter_errors(output),
        key=lambda error: list(error.path),
    )
    if errors:
        detail = "; ".join(
            f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise RuntimeError(f"adapter protocol validation failed: {detail}")

    observed_ids = [item["failure_id"] for item in vectors]
    if observed_ids != EXPECTED_IDS:
        raise RuntimeError("adapter output did not preserve ordered F001-F006 vectors")
    for vector in vectors:
        if vector["observed_state"] != vector["expected_state"]:
            raise RuntimeError(
                f"{vector['failure_id']} observed {vector['observed_state']!r}; "
                f"expected {vector['expected_state']!r}"
            )
        if vector["counter_after"] < vector["counter_before"]:
            raise RuntimeError(f"counter regression in {vector['failure_id']}")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--bedrock-sha", required=True)
    args = parser.parse_args()
    try:
        matrix_document = load_json(args.matrix)
        output = run_all_vectors(
            matrix_document["vectors"],
            args.bedrock_sha,
            args.runtime,
            load_json(args.protocol),
        )
        json.dump(output, sys.stdout, sort_keys=True, separators=(",", ":"))
        sys.stdout.write("\n")
        return 0
    except Exception as exc:
        print(f"ALMS_ADAPTER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
