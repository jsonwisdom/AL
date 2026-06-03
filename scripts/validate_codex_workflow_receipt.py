#!/usr/bin/env python3
"""Minimal validator for Codex workflow receipts - Issue #284."""

import json
import re
import sys
from pathlib import Path

HASH_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
VALID_STATUSES = {"DRAFT", "VERIFIED", "REFUSED", "STALE", "SUPERSEDED"}
VALID_RECEIPT_TYPE = "CODEX_WORKFLOW_RECEIPT_V0_1"


def validate_hash(hash_value):
    """Validate sha256:<64 lowercase hex> format."""
    return isinstance(hash_value, str) and HASH_RE.match(hash_value) is not None


def require_string(obj, path, errors):
    """Require a non-empty string at path in obj."""
    cur = obj
    for key in path.split("."):
        if not isinstance(cur, dict) or key not in cur:
            errors.append(f"{path} is required")
            return None
        cur = cur[key]
    if not isinstance(cur, str) or not cur:
        errors.append(f"{path} must be a non-empty string")
        return None
    return cur


def validate_receipt(receipt_path):
    """Validate a single receipt JSON against the committed v0.1 rules."""
    errors = []

    try:
        with open(receipt_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON: {exc}"]
    except OSError as exc:
        return [f"Failed to read file: {exc}"]

    if data.get("receipt_type") != VALID_RECEIPT_TYPE:
        errors.append(
            f"receipt_type must be {VALID_RECEIPT_TYPE}, got {data.get('receipt_type')!r}"
        )

    if data.get("authority") is not False:
        errors.append(f"authority must be false, got {data.get('authority')!r}")

    status = data.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"status must be one of {sorted(VALID_STATUSES)}, got {status!r}")

    require_string(data, "created_at", errors)
    require_string(data, "workflow.id", errors)
    require_string(data, "workflow.role", errors)
    require_string(data, "workflow.description", errors)
    require_string(data, "artifact.type", errors)
    require_string(data, "artifact.title", errors)

    artifact_hash = require_string(data, "artifact.hash", errors)
    if artifact_hash and not validate_hash(artifact_hash):
        errors.append(f"artifact.hash must match sha256:<64 lowercase hex>, got {artifact_hash!r}")

    artifact = data.get("artifact", {})
    locations = artifact.get("locations") if isinstance(artifact, dict) else None
    if not isinstance(locations, list) or not locations:
        errors.append("artifact.locations must be a non-empty array")
    else:
        for idx, location in enumerate(locations):
            if not isinstance(location, str) or not location:
                errors.append(f"artifact.locations[{idx}] must be a non-empty string")

    evidence_refs = data.get("evidence_refs", [])
    if not isinstance(evidence_refs, list):
        errors.append("evidence_refs must be an array")
        evidence_refs = []
    for idx, evidence in enumerate(evidence_refs):
        if not isinstance(evidence, dict):
            errors.append(f"evidence_refs[{idx}] must be an object")
            continue
        for key in ("type", "description", "ref"):
            value = evidence.get(key)
            if not isinstance(value, str) or not value:
                errors.append(f"evidence_refs[{idx}].{key} is required")

    replay_steps = data.get("replay_steps", [])
    if not isinstance(replay_steps, list):
        errors.append("replay_steps must be an array")
        replay_steps = []

    if status == "VERIFIED":
        if not evidence_refs:
            errors.append("VERIFIED status requires non-empty evidence_refs")
        if not replay_steps:
            errors.append("VERIFIED status requires non-empty replay_steps")

    if status == "REFUSED":
        refusal_reasons = data.get("refusal_reasons", [])
        if not isinstance(refusal_reasons, list) or not refusal_reasons:
            errors.append("REFUSED status requires non-empty refusal_reasons")

    if status == "SUPERSEDED" and not data.get("successor_receipt_id"):
        errors.append("SUPERSEDED status requires successor_receipt_id")

    annotation_events = data.get("annotation_events", [])
    if not isinstance(annotation_events, list):
        errors.append("annotation_events must be an array")
        annotation_events = []
    for idx, annotation in enumerate(annotation_events):
        if not isinstance(annotation, dict):
            errors.append(f"annotation_events[{idx}] must be an object")
            continue
        for key in ("target", "instruction"):
            value = annotation.get(key)
            if not isinstance(value, str) or not value:
                errors.append(f"annotation_events[{idx}].{key} is required")
        for key in ("predecessor_artifact_hash", "successor_artifact_hash"):
            value = annotation.get(key)
            if not validate_hash(value):
                errors.append(
                    f"annotation_events[{idx}].{key} must match sha256:<64 lowercase hex>"
                )

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_codex_workflow_receipt.py <receipt1.json> [receipt2.json ...]")
        return 1

    all_passed = True
    for receipt_path in sys.argv[1:]:
        if not Path(receipt_path).exists():
            print(f"❌ File not found: {receipt_path}")
            all_passed = False
            continue

        errors = validate_receipt(receipt_path)
        if errors:
            print(f"❌ Validation failed for {receipt_path}:")
            for error in errors:
                print(f"   - {error}")
            all_passed = False
        else:
            print(f"✅ {receipt_path} valid")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
