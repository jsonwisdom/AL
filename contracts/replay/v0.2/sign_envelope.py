#!/usr/bin/env python3
"""
ALMS envelope signing helper v0.2.

Signs integrity.envelope_canonical_hash with an ECDSA P-256 private key and
injects an envelope-signature-v0.1 block.

Private keys must never be committed to the repository.
"""

from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict


ALGORITHM = "ECDSA_P256_SHA256_DER_V1"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sign_digest(private_key_path: Path, digest_hex: str) -> str:
    digest = bytes.fromhex(digest_hex)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        digest_path = tmp_path / "digest.bin"
        sig_path = tmp_path / "signature.der"
        digest_path.write_bytes(digest)
        subprocess.run(
            [
                "openssl",
                "pkeyutl",
                "-sign",
                "-inkey",
                str(private_key_path),
                "-in",
                str(digest_path),
                "-out",
                str(sig_path),
            ],
            check=True,
        )
        return base64.b64encode(sig_path.read_bytes()).decode("ascii")


def main() -> int:
    if len(sys.argv) != 5:
        print("usage: sign_envelope.py <envelope.json> <private_key.pem> <key_id> <output.json>", file=sys.stderr)
        return 2

    envelope_path = Path(sys.argv[1])
    private_key_path = Path(sys.argv[2])
    key_id = sys.argv[3]
    output_path = Path(sys.argv[4])

    envelope = load_json(envelope_path)
    envelope_hash = envelope.get("integrity", {}).get("envelope_canonical_hash")
    if not isinstance(envelope_hash, str) or not envelope_hash.startswith("sha256:"):
        print("missing integrity.envelope_canonical_hash", file=sys.stderr)
        return 1

    digest_hex = envelope_hash.split(":", 1)[1]
    signature_value = sign_digest(private_key_path, digest_hex)

    envelope["signature"] = {
        "signature_version": "envelope-signature-v0.1",
        "key_id": key_id,
        "algorithm": ALGORITHM,
        "signed_payload": {
            "field": "integrity.envelope_canonical_hash",
            "hash": envelope_hash,
        },
        "signature_encoding": "base64_der",
        "signature_value": signature_value,
    }

    output_path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
