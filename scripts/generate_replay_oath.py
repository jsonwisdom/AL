#!/usr/bin/env python3
"""
Level 3 Oath Generator v0
AL Issue #224

Generates a replay_oath JSON from:
  - receipt file
  - verifier stdout/log file
  - witness identity

Strict evidence recorder only.
No signatures. No settlement. No payment authorization.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


CONFIRMED_TOKEN = "RECEIPT_CONFIRMED"
REJECTED_TOKEN = "RECEIPT_REJECTED"
UNOBSERVED_TOKEN = "FULL_REPLAY_STATUS: UNOBSERVED"


def compute_sha256(file_path: Path) -> str:
    """Return sha256 hash of file content."""
    hash_sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha.update(chunk)
    return f"sha256:{hash_sha.hexdigest()}"


def parse_verifier_status(verifier_content: str) -> Tuple[str, List[str]]:
    """Strict token-based parsing only. No loose keyword matching."""
    content = verifier_content.upper()
    observed_tokens: List[str] = []

    if CONFIRMED_TOKEN in content:
        status = "confirmed"
        observed_tokens.append(CONFIRMED_TOKEN)
    elif REJECTED_TOKEN in content:
        status = "rejected"
        observed_tokens.append(REJECTED_TOKEN)
    elif UNOBSERVED_TOKEN in content:
        status = "unobserved"
        observed_tokens.append(UNOBSERVED_TOKEN)
    else:
        status = "unobserved"

    return status, observed_tokens


def generate_oath(
    receipt_path: Path,
    verifier_path: Path,
    witness_identity: str,
    verifier_mode: str = "current-tip",
) -> Dict[str, Any]:
    """Generate a replay oath from observed verifier output."""
    if not receipt_path.exists():
        raise FileNotFoundError(f"Receipt not found: {receipt_path}")
    if not verifier_path.exists():
        raise FileNotFoundError(f"Verifier output not found: {verifier_path}")
    if not witness_identity.strip():
        raise ValueError("Witness identity must not be empty")

    receipt_hash = compute_sha256(receipt_path)
    verifier_hash = compute_sha256(verifier_path)

    verifier_content = verifier_path.read_text(encoding="utf-8", errors="replace")
    replay_status, observed_tokens = parse_verifier_status(verifier_content)

    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return {
        "schema_version": "0.1.0",
        "oath_type": "replay_oath",
        "timestamp": timestamp,
        "witness": {
            "identity": witness_identity,
            "mode": "observer",
        },
        "source": {
            "receipt_path": str(receipt_path),
            "receipt_hash": receipt_hash,
            "verifier_output_hash": verifier_hash,
        },
        "observation": {
            "verifier_mode": verifier_mode,
            "replay_status": replay_status,
            "observed_tokens": observed_tokens,
        },
        "limits": {
            "creates_truth": False,
            "authorizes_payment": False,
            "links_settlement": False,
            "signature_present": False,
        },
    }


def main() -> int:
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print(
            "Usage: python3 scripts/generate_replay_oath.py "
            "<receipt.json> <verifier-output.txt> <witness-identity> [verifier-mode]",
            file=sys.stderr,
        )
        return 1

    receipt_path = Path(sys.argv[1])
    verifier_path = Path(sys.argv[2])
    witness_identity = sys.argv[3]
    verifier_mode = sys.argv[4] if len(sys.argv) == 5 else "current-tip"

    oath = generate_oath(receipt_path, verifier_path, witness_identity, verifier_mode)

    output_dir = Path("receipts/oaths")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp_slug = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = output_dir / f"{timestamp_slug}_replay_oath.json"

    output_path.write_text(json.dumps(oath, indent=2) + "\n", encoding="utf-8")
    print(f"Level 3 oath generated: {output_path}")
    print(f"replay_status: {oath['observation']['replay_status']}")
    print("creates_truth: false")
    print("authorizes_payment: false")
    print("links_settlement: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
