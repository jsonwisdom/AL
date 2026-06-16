#!/usr/bin/env python3
"""
ALMS attestation graph verifier.

Canonical read path:
  candidate -> claims ledger -> subject artifact -> validator

Scope:
- Verifies pre-attestation candidates only.
- Does not fetch external content.
- Does not attest, promote, or open gates.

Usage:
  python scripts/verify_attestation_graph.py --candidate _truth/anchors/ATTESTATION_CANDIDATE.json
"""

import argparse
import hashlib
import json
import re
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


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_ledger(ledger_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_claim_ledger.py", str(ledger_path)],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        raise RuntimeError("claim ledger validator failed")


def valid_git_sha(value: str) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def verify_candidate(candidate_path: Path, require_head_match: bool = False) -> int:
    if not candidate_path.exists():
        print(f"[FAIL] Candidate not found: {candidate_path}")
        return 1

    candidate = load_json(candidate_path)

    # 1. Candidate self-hash convention:
    #    If candidate_manifest_sha256 exists, null it before canonical hashing.
    expected_candidate_sha = candidate.get("candidate_manifest_sha256") or candidate.get("candidate_sha256")
    if expected_candidate_sha:
        candidate_for_hash = dict(candidate)
        if "candidate_manifest_sha256" in candidate_for_hash:
            candidate_for_hash["candidate_manifest_sha256"] = None
        if "candidate_sha256" in candidate_for_hash:
            candidate_for_hash["candidate_sha256"] = None
        actual_candidate_sha = canonical_sha256(candidate_for_hash)
        if actual_candidate_sha != expected_candidate_sha:
            print("[FAIL] CANDIDATE_SHA256 mismatch")
            print(f"  expected={expected_candidate_sha}")
            print(f"  actual  ={actual_candidate_sha}")
            return 1
    else:
        actual_candidate_sha = canonical_sha256(candidate)
        print("[WARN] Candidate has no stored candidate hash; computed canonical hash only")

    # 2. Ledger binding.
    ledger_path_raw = candidate.get("claims_ledger_path")
    expected_ledger_sha = candidate.get("claims_ledger_sha256")
    if not ledger_path_raw or not expected_ledger_sha:
        print("[FAIL] Candidate missing claims_ledger_path or claims_ledger_sha256")
        return 1

    ledger_path = Path(ledger_path_raw)
    if not ledger_path.exists():
        print(f"[FAIL] Claims ledger not found: {ledger_path}")
        return 1

    ledger = load_json(ledger_path)
    ledger_for_hash = dict(ledger)
    ledger_for_hash["ledger_manifest_sha256"] = None
    actual_ledger_sha = canonical_sha256(ledger_for_hash)
    if actual_ledger_sha != expected_ledger_sha:
        print("[FAIL] CLAIMS_LEDGER_SHA256 mismatch")
        print(f"  expected={expected_ledger_sha}")
        print(f"  actual  ={actual_ledger_sha}")
        return 1

    # 3. Ledger validity.
    try:
        validate_ledger(ledger_path)
    except Exception as exc:
        print(f"[FAIL] Ledger invalid: {exc}")
        return 1

    # 4. Subject binding.
    subject_path_raw = candidate.get("subject_artifact") or candidate.get("subject_path")
    expected_subject_sha = candidate.get("subject_sha256")
    if not subject_path_raw or not expected_subject_sha:
        print("[FAIL] Candidate missing subject_artifact/subject_path or subject_sha256")
        return 1

    subject_path = Path(subject_path_raw)
    if not subject_path.exists():
        print(f"[FAIL] Subject artifact not found: {subject_path}")
        return 1

    actual_subject_sha = file_sha256(subject_path)
    if actual_subject_sha != expected_subject_sha:
        print("[FAIL] SUBJECT_SHA256 mismatch")
        print(f"  expected={expected_subject_sha}")
        print(f"  actual  ={actual_subject_sha}")
        return 1

    # 5. Commit binding.
    commit = candidate.get("commit")
    if not valid_git_sha(commit):
        print("[FAIL] Candidate commit is missing or not a 40-char git SHA")
        return 1

    if require_head_match:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        if head != commit:
            print("[FAIL] Candidate commit does not match current HEAD")
            print(f"  candidate={commit}")
            print(f"  head     ={head}")
            return 1

    # 6. Pre-attestation sanity.
    if candidate.get("onchain_status") != "NOT_ATTESTED":
        print("[FAIL] Candidate is not pre-attestation: onchain_status != NOT_ATTESTED")
        return 1
    if candidate.get("eas_uid") is not None or candidate.get("tx_hash") is not None:
        print("[FAIL] Candidate contains EAS UID or tx hash; use post-attestation verifier")
        return 1
    if candidate.get("promotion") is not False or candidate.get("gate_status") != "CLOSED":
        print("[FAIL] Candidate promotion/gate state is not closed")
        return 1

    print("[OK] Attestation graph is internally consistent and bounded")
    print(f"  CANDIDATE_SHA256     = {actual_candidate_sha}")
    print(f"  CLAIMS_LEDGER_SHA256 = {actual_ledger_sha}")
    print(f"  SUBJECT_SHA256       = {actual_subject_sha}")
    print(f"  COMMIT               = {commit}")
    print("  ONCHAIN_STATUS       = NOT_ATTESTED")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, help="Path to attestation candidate JSON")
    parser.add_argument("--require-head-match", action="store_true", help="Require candidate commit to equal git HEAD")
    args = parser.parse_args()

    sys.exit(verify_candidate(Path(args.candidate), args.require_head_match))


if __name__ == "__main__":
    main()
