#!/usr/bin/env python3
"""
AL Doctrine Linter v1

Enforces baseline doctrine file, verification-envelope, separation, and hash
invariants. Output is deterministic YAML when PyYAML is available and
canonical JSON otherwise.

Supported input layouts:

1. Structured doctrine directory
   envelope.yaml
   sovereign.md
   civic.md                 # optional unless required by envelope

2. Monolithic Markdown doctrine
   A single .md file. This mode validates readability, explicit doctrine
   identity, and sovereign/civic terminology but cannot certify separation or
   envelope hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - deterministic fallback
    yaml = None


PASS = "PASS"
FAIL = "FAIL"
INDETERMINATE = "INDETERMINATE"


def compute_sha256(file_path: Path) -> str:
    """Return the lowercase SHA-256 digest of a file's exact bytes."""
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read envelope.yaml")
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError("envelope.yaml root must be a mapping")
    return loaded


def emit(result: Dict[str, Any]) -> str:
    """Serialize with stable key ordering and a trailing newline."""
    if yaml is not None:
        return yaml.safe_dump(result, sort_keys=True, allow_unicode=True)
    return json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def check_separation_hygiene(
    sovereign_path: Path, civic_path: Path | None
) -> Tuple[str, str]:
    sovereign = sovereign_path.read_text(encoding="utf-8")

    accepted_sovereign_markers = (
        "## SOVEREIGN RECORD",
        "### The sovereign record",
        "## The Sovereign Record",
    )
    if not any(marker in sovereign for marker in accepted_sovereign_markers):
        return FAIL, "Missing explicit sovereign-record marker"

    if civic_path is None or not civic_path.exists():
        accepted_civic_markers = (
            "## CIVIC RECORD",
            "### The civic record",
            "## The Civic Record",
        )
        if any(marker in sovereign for marker in accepted_civic_markers):
            return INDETERMINATE, (
                "Sovereign and civic concepts are declared in one artifact; "
                "file-level separation cannot be certified"
            )
        return INDETERMINATE, "No civic.md artifact available for boundary review"

    civic = civic_path.read_text(encoding="utf-8")
    if not civic.strip():
        return FAIL, "civic.md is empty"

    return PASS, "Explicit sovereign and civic artifacts are present"


def structured_lint(doctrine_dir: Path) -> Dict[str, Any]:
    envelope_path = doctrine_dir / "envelope.yaml"
    sovereign_path = doctrine_dir / "sovereign.md"
    civic_path = doctrine_dir / "civic.md"

    missing = [
        path.name
        for path in (envelope_path, sovereign_path)
        if not path.exists()
    ]
    if missing:
        return {
            "details": f"Missing required files: {', '.join(sorted(missing))}",
            "doctrine_path": doctrine_dir.as_posix(),
            "lint_status": FAIL,
            "mode": "structured",
            "recommendation": "Create required artifacts before sealing",
        }

    try:
        envelope = load_yaml(envelope_path)
    except (OSError, RuntimeError, ValueError) as exc:
        return {
            "details": str(exc),
            "doctrine_path": doctrine_dir.as_posix(),
            "lint_status": FAIL,
            "mode": "structured",
            "recommendation": "Repair envelope.yaml and replay",
        }

    contract = envelope.get("verification_contract", {})
    if not isinstance(contract, dict):
        return {
            "details": "verification_contract must be a mapping",
            "doctrine_path": doctrine_dir.as_posix(),
            "lint_status": FAIL,
            "mode": "structured",
            "recommendation": "Repair envelope structure and replay",
        }

    expected_hash = contract.get("sovereign_hash")
    actual_hash = compute_sha256(sovereign_path)
    if not expected_hash:
        return {
            "actual_sovereign_hash": actual_hash,
            "details": "verification_contract.sovereign_hash is absent",
            "doctrine_id": contract.get("doctrine_id"),
            "doctrine_path": doctrine_dir.as_posix(),
            "lint_status": INDETERMINATE,
            "mode": "structured",
            "recommendation": "Record the exact sovereign.md SHA-256 and replay",
        }

    if actual_hash != expected_hash:
        return {
            "actual_sovereign_hash": actual_hash,
            "details": "sovereign_hash mismatch",
            "doctrine_id": contract.get("doctrine_id"),
            "doctrine_path": doctrine_dir.as_posix(),
            "expected_sovereign_hash": expected_hash,
            "lint_status": FAIL,
            "mode": "structured",
            "recommendation": "Isolate drift, correct the boundary, and re-seal",
        }

    hygiene_status, details = check_separation_hygiene(
        sovereign_path, civic_path if civic_path.exists() else None
    )
    return {
        "actual_sovereign_hash": actual_hash,
        "details": details,
        "doctrine_id": contract.get("doctrine_id"),
        "doctrine_path": doctrine_dir.as_posix(),
        "lint_status": hygiene_status,
        "mode": "structured",
        "recommendation": (
            "Merge with atomic receipt"
            if hygiene_status == PASS
            else "Resolve the reported boundary and replay"
        ),
        "replay_manifest_ref": contract.get("replay_manifest_ref"),
    }


def monolithic_lint(markdown_path: Path) -> Dict[str, Any]:
    try:
        text = markdown_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {
            "details": str(exc),
            "doctrine_path": markdown_path.as_posix(),
            "lint_status": FAIL,
            "mode": "monolithic",
            "recommendation": "Restore a readable UTF-8 doctrine artifact",
        }

    failures = []
    if not text.lstrip().startswith("#"):
        failures.append("missing Markdown title")
    if "DOCTRINE" not in text.upper():
        failures.append("missing explicit doctrine identity")

    has_sovereign = "sovereign record" in text.lower()
    has_civic = "civic record" in text.lower()
    if not has_sovereign:
        failures.append("missing sovereign-record terminology")
    if not has_civic:
        failures.append("missing civic-record terminology")

    digest = compute_sha256(markdown_path)
    if failures:
        return {
            "artifact_hash": digest,
            "details": "; ".join(failures),
            "doctrine_path": markdown_path.as_posix(),
            "lint_status": FAIL,
            "mode": "monolithic",
            "recommendation": "Correct doctrine markers and replay",
        }

    return {
        "artifact_hash": digest,
        "details": (
            "Monolithic doctrine markers pass; envelope integrity and file-level "
            "sovereign/civic separation remain unverified"
        ),
        "doctrine_path": markdown_path.as_posix(),
        "lint_status": INDETERMINATE,
        "mode": "monolithic",
        "recommendation": (
            "Create envelope.yaml, sovereign.md, and civic.md for a sealable replay"
        ),
        "replay_manifest_ref": None,
    }


def lint_doctrine(target: Path) -> Dict[str, Any]:
    if not target.exists():
        return {
            "details": "Target does not exist",
            "doctrine_path": target.as_posix(),
            "lint_status": FAIL,
            "mode": "unknown",
            "recommendation": "Provide an existing doctrine file or directory",
        }
    if target.is_dir():
        return structured_lint(target)
    if target.is_file() and target.suffix.lower() == ".md":
        return monolithic_lint(target)
    return {
        "details": "Unsupported target; expected a doctrine directory or .md file",
        "doctrine_path": target.as_posix(),
        "lint_status": FAIL,
        "mode": "unknown",
        "recommendation": "Use a supported doctrine layout",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint an AL doctrine artifact")
    parser.add_argument("target", type=Path, help="Doctrine directory or Markdown file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = lint_doctrine(args.target)
    sys.stdout.write(emit(result))
    return 0 if result["lint_status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
