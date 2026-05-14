#!/usr/bin/env python3
"""
Lapis replay demo verifier.

Local-first forensic gate for the Lapis Protocol:
- validates a replay object against the v0.1 JSON Schema
- verifies L0 content bytes against l0_vault.content_sha256
- verifies repository chronology by checking the referenced genesis commit exists
- emits REPLAY_SUMMARY.json

No Base/EAS settlement should occur before this local replay gate passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


DEFAULT_SCHEMA = Path("schemas/lapis/replayable_audit_demo.v0.1.schema.json")
DEFAULT_SAMPLE = Path("examples/lapis/replayable_audit_demo.sample.json")
DEFAULT_OUTPUT = Path("REPLAY_SUMMARY.json")
GENESIS_COMMIT = "edcec6f55adbd65913f3e6b28c79c81d73ef84b6"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit_exists(commit_sha: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def validate_schema(sample: dict[str, Any], schema: dict[str, Any]) -> tuple[bool, str | None]:
    if jsonschema is None:
        return False, "Missing dependency: jsonschema. Install with `python -m pip install jsonschema`."

    try:
        jsonschema.Draft202012Validator(schema).validate(sample)
        return True, None
    except jsonschema.ValidationError as exc:
        return False, exc.message


def infer_local_artifact_path(sample: dict[str, Any]) -> Path:
    artifact_id = sample.get("artifact_id", "")

    if artifact_id == "lapis-genesis-commit-edcec6f":
        return Path("docs/LAPIS_PROTOCOL_STEWARDSHIP_INVARIANT.md")

    object_path = sample.get("l0_vault", {}).get("object_path")
    if object_path:
        candidate = Path(object_path)
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Could not infer local artifact path. Add artifact-specific path handling or fetch the L0 object first."
    )


def run_audit(sample_path: Path, schema_path: Path, output_path: Path) -> dict[str, Any]:
    sample = load_json(sample_path)
    schema = load_json(schema_path)

    schema_pass, schema_error = validate_schema(sample, schema)

    artifact_path: Path | None = None
    artifact_exists = False
    actual_sha256: str | None = None
    content_pass = False

    try:
        artifact_path = infer_local_artifact_path(sample)
        artifact_exists = artifact_path.exists()
        if artifact_exists:
            actual_sha256 = sha256_file(artifact_path)
            content_pass = actual_sha256.lower() == sample["l0_vault"]["content_sha256"].lower()
    except Exception as exc:
        artifact_path_error = str(exc)
    else:
        artifact_path_error = None

    chronology_commit = GENESIS_COMMIT if sample.get("artifact_id") == "lapis-genesis-commit-edcec6f" else None
    chronology_pass = git_commit_exists(chronology_commit) if chronology_commit else False

    witness_present = bool(sample.get("witness", {}).get("identity"))
    replay_path_present = bool(sample.get("replay", {}).get("instructions"))

    verdict = "PASS" if all(
        [
            schema_pass,
            artifact_exists,
            content_pass,
            chronology_pass,
            witness_present,
            replay_path_present,
        ]
    ) else "FAIL"

    summary = {
        "schema_version": sample.get("schema_version"),
        "audit_id": f"replay-{sample.get('artifact_id', 'unknown')}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "lapis_filter": {
            "schema_valid": schema_pass,
            "schema_error": schema_error,
            "chronology_present": chronology_pass,
            "texture_present": artifact_exists and content_pass,
            "witness_present": witness_present,
            "replay_path_present": replay_path_present,
            "silent_overwrite_detected": artifact_exists and not content_pass,
        },
        "forensics": {
            "artifact_id": sample.get("artifact_id"),
            "artifact_path": str(artifact_path) if artifact_path else None,
            "artifact_path_error": artifact_path_error,
            "expected_content_sha256": sample.get("l0_vault", {}).get("content_sha256"),
            "actual_content_sha256": actual_sha256,
            "content_match": content_pass,
            "chronology_commit": chronology_commit,
            "chronology_commit_exists": chronology_pass,
        },
        "stewardship": {
            "root_identity": sample.get("root_identity"),
            "witness_identity": sample.get("witness", {}).get("identity"),
            "operating_posture": "recoverability_over_invulnerability",
            "rule": "No L2 settlement before L0 replay validation passes.",
        },
    }

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Lapis replay demo artifact.")
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summary = run_audit(args.sample, args.schema, args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
