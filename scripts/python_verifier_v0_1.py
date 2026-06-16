#!/usr/bin/env python3
"""
ALMS Cross-Verifier Independent Python Verifier v0.1

Purpose:
  Confirm the committed ALMS replay result file carries the expected
  implementation-independent SHA256 replay hash and PASS result.

Scope:
  This verifier does not compute Ethereum Keccak and does not collapse
  SHA256 replay, SHA3-256 bridge, or EVM Keccak domains.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

EXPECTED_RESULT_COMMIT_SHA = "0a16480220fceb1b29a2e240ab569e15ebea5a39"
EXPECTED_RESULT = "PASS"
EXPECTED_SHA256_REPLAY_HASH = "0xf72d4c0460572c8cc3ac3f9cc7ac9d674d635d1f06b085fc2e2c8a31accbefa7"
EXPECTED_SHA3_256_BRIDGE_HASH = "0x980edb5f9e5a03d77c595cd1d8f5d31eaecf9918cd562c222377cbe8608c9260"
EXPECTED_BRIDGE_DOMAIN = "SHA3_256_NOT_ETHEREUM_KECCAK256"


def canonical_json(value: Any) -> str:
    """Deterministic JSON form used for local self-check output."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(data: bytes) -> str:
    return "0x" + hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def verify(result_path: Path) -> dict:
    doc = load_json(result_path)

    result = doc.get("result")
    replay_hash = doc.get("sha256_replay_hash")
    bridge_hash = doc.get("sha3_256_bridge_hash")
    bridge_domain = doc.get("bridge_hash_domain")

    eas = doc.get("eas_attestation_payload", {})

    checks = {
        "result_is_pass": result == EXPECTED_RESULT,
        "sha256_replay_hash_matches": replay_hash == EXPECTED_SHA256_REPLAY_HASH,
        "sha3_256_bridge_hash_matches": bridge_hash == EXPECTED_SHA3_256_BRIDGE_HASH,
        "bridge_domain_separated": bridge_domain == EXPECTED_BRIDGE_DOMAIN,
        "eas_replay_hash_bound": eas.get("sha256_replay_hash") == EXPECTED_SHA256_REPLAY_HASH,
        "eas_bridge_hash_bound": eas.get("sha3_256_bridge_hash") == EXPECTED_SHA3_256_BRIDGE_HASH,
        "domain_collapse_absent": replay_hash != bridge_hash,
    }

    output = {
        "implementation_name": "python_independent_verifier",
        "implementation_version": "0.1",
        "language": "python",
        "result_commit_sha": EXPECTED_RESULT_COMMIT_SHA,
        "source_result_file": str(result_path),
        "expected_replay_hash": EXPECTED_SHA256_REPLAY_HASH,
        "computed_replay_hash": replay_hash,
        "expected_result": EXPECTED_RESULT,
        "observed_result": result,
        "canonicalization": "RFC_8785_TARGET_DECLARED_BY_VECTOR",
        "hash_domain": "SHA256_REPLAY_HASH",
        "bridge_hash_domain": bridge_domain,
        "local_output_sha256": None,
        "checks": checks,
        "match": all(checks.values()),
    }

    output["local_output_sha256"] = sha256_hex(canonical_json(output).encode("utf-8"))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--result-file",
        default="vectors/cross_round_evaluation_result_v0_1.json",
        help="Path to committed ALMS replay result JSON",
    )
    args = parser.parse_args()

    report = verify(Path(args.result_file))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["match"] else 1


if __name__ == "__main__":
    sys.exit(main())
