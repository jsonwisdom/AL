#!/usr/bin/env python3
"""
ALMS attestation candidate generator.

Hard rule:
- No candidate is generated unless the claim ledger passes validation.
- Output remains NOT_ATTESTED until a real EAS UID / tx hash exists.

Usage:
  python scripts/generate_attestation_candidate.py \
    --ledger ledgers/claims/example.json \
    --subject _truth/status/QUIESCENT_HOLD_2026-05-05.json \
    --out _truth/anchors/ATTESTATION_CANDIDATE.json \
    --statement "Snapshot proven. Change detectable. Monitoring pending."
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def canonical_sha256(obj: dict) -> str:
    data = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def validate_ledger(ledger: Path) -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_claim_ledger.py", str(ledger)],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--statement", required=True)
    args = parser.parse_args()

    ledger_path = Path(args.ledger)
    subject_path = Path(args.subject)
    out_path = Path(args.out)

    if not ledger_path.exists():
        raise SystemExit(f"ledger not found: {ledger_path}")
    if not subject_path.exists():
        raise SystemExit(f"subject not found: {subject_path}")

    validate_ledger(ledger_path)

    with ledger_path.open("r", encoding="utf-8") as f:
        ledger = json.load(f)

    # Self-hash convention: null out ledger_manifest_sha256 before hashing.
    ledger_for_hash = dict(ledger)
    ledger_for_hash["ledger_manifest_sha256"] = None
    ledger_hash = canonical_sha256(ledger_for_hash)

    candidate = {
        "artifact": "ALMS_ATTESTATION_CANDIDATE",
        "repo": "jsonwisdom/AL",
        "commit": git_commit(),
        "subject_artifact": str(subject_path),
        "subject_sha256": file_sha256(subject_path),
        "claims_ledger_path": str(ledger_path),
        "claims_ledger_sha256": ledger_hash,
        "statement": args.statement,
        "onchain_status": "NOT_ATTESTED",
        "eas_uid": None,
        "tx_hash": None,
        "promotion": False,
        "gate_status": "CLOSED",
    }

    candidate["candidate_manifest_sha256"] = canonical_sha256(candidate)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"ATTESTATION_CANDIDATE_CREATED={out_path}")
    print(f"CLAIMS_LEDGER_SHA256={ledger_hash}")
    print(f"CANDIDATE_SHA256={candidate['candidate_manifest_sha256']}")


if __name__ == "__main__":
    main()
