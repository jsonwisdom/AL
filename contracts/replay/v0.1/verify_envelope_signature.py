#!/usr/bin/env python3
"""
Replay Envelope Signature Verifier v0.1

Verifies that a replay envelope signature block resolves to an active key in
contracts/keys/v0.1/registry.json and validates against the declared envelope
canonical hash.

This script intentionally performs no truth adjudication.
"""

from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[3]
KEY_REGISTRY = ROOT / "contracts" / "keys" / "v0.1" / "registry.json"


class SignatureRefusal(Exception):
    pass


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SignatureRefusal(message)


def find_key(registry: Dict[str, Any], key_id: str) -> Dict[str, Any]:
    for key in registry.get("keys", []):
        if key.get("key_id") == key_id:
            return key
    raise SignatureRefusal("key_id_not_found")


def verify_signature(envelope_path: Path) -> None:
    envelope = load_json(envelope_path)
    registry = load_json(KEY_REGISTRY)

    signature = envelope.get("signature")
    require(isinstance(signature, dict), "signature_block_missing")

    key_id = signature.get("key_id")
    algorithm = signature.get("algorithm")
    signed_payload = signature.get("signed_payload") or {}
    signature_value = signature.get("signature_value")

    require(isinstance(key_id, str), "key_id_missing")
    require(algorithm == "ECDSA_P256_SHA256_DER_V1", "algorithm_unsupported")
    require(isinstance(signature_value, str), "signature_value_missing")

    envelope_hash = envelope.get("integrity", {}).get("envelope_canonical_hash")
    signed_hash = signed_payload.get("hash")
    require(envelope_hash == signed_hash, "signed_payload_hash_mismatch")
    require(isinstance(envelope_hash, str) and envelope_hash.startswith("sha256:"), "invalid_envelope_hash")

    key = find_key(registry, key_id)
    require(key.get("active") is True, "key_inactive")
    require(key.get("algorithm") == algorithm, "key_algorithm_mismatch")

    try:
        signature_bytes = base64.b64decode(signature_value, validate=True)
    except Exception as exc:
        raise SignatureRefusal("signature_base64_malformed") from exc

    digest_hex = envelope_hash.split(":", 1)[1]
    digest_bytes = bytes.fromhex(digest_hex)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        public_key_path = tmp_path / "public_key.pem"
        digest_path = tmp_path / "envelope.sha256.bin"
        signature_path = tmp_path / "signature.der"

        public_key_path.write_text(key["public_key_pem"], encoding="utf-8")
        digest_path.write_bytes(digest_bytes)
        signature_path.write_bytes(signature_bytes)

        result = subprocess.run(
            [
                "openssl",
                "pkeyutl",
                "-verify",
                "-pubin",
                "-inkey",
                str(public_key_path),
                "-sigfile",
                str(signature_path),
                "-in",
                str(digest_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    if result.returncode != 0:
        raise SignatureRefusal("signature_verification_failed")


def main() -> int:
    if len(sys.argv) != 2:
        print("REPLAY_REFUSED: usage verify_envelope_signature.py <envelope.json>")
        return 2

    try:
        verify_signature(Path(sys.argv[1]))
    except SignatureRefusal as exc:
        print(f"REPLAY_REFUSED: envelope_signature_invalid reason={exc}")
        return 1

    print("ENVELOPE_SIGNATURE_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
