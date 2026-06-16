#!/usr/bin/env python3
"""
Manifest Verifier v1

Constitutional boundary:
  - Verifies manifest structure and attestor declaration
  - Does NOT perform adoption
  - Does NOT mutate lineage
  - Does NOT interpret SSD semantics
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

SCHEMA_VERSION = "1.0.0"
RECEIPT_TYPE = "MANIFEST_VERIFICATION_RECEIPT_V1"


def canonical_json(data: dict[str, Any]) -> bytes:
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")



def compute_manifest_id(manifest: dict[str, Any]) -> str:
    unsigned = dict(manifest)
    unsigned.pop("signature", None)
    manifest_id = unsigned.pop("manifest_id", None)

    digest = hashlib.sha256(canonical_json(unsigned)).hexdigest()
    computed = f"sha256:{digest}"

    if manifest_id is not None and manifest_id != computed:
        raise ValueError("MANIFEST_ID_MISMATCH")

    return computed



def verify_signature(manifest: dict[str, Any], keyring: dict[str, str]) -> bool:
    issuer_key_id = manifest["issuer_key_id"]
    signature = manifest["signature"]

    if issuer_key_id not in keyring:
        raise ValueError("UNKNOWN_ISSUER_KEY")

    expected = hashlib.sha256(
        (manifest["manifest_id"] + keyring[issuer_key_id]).encode("utf-8")
    ).hexdigest()

    return signature == expected



def verify_manifest(
    manifest: dict[str, Any],
    keyring: dict[str, str],
    linked_receipts: set[str] | None = None,
) -> dict[str, Any]:
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("BAD_SCHEMA_VERSION")

    computed_manifest_id = compute_manifest_id(manifest)

    if manifest["manifest_id"] != computed_manifest_id:
        raise ValueError("MANIFEST_ID_MISMATCH")

    if not verify_signature(manifest, keyring):
        raise ValueError("BAD_SIGNATURE")

    linked = manifest.get("linked_verifier_receipt")
    if linked is not None:
        if linked_receipts is None or linked not in linked_receipts:
            raise ValueError("LINKED_RECEIPT_NOT_FOUND")

    return {
        "receipt_type": RECEIPT_TYPE,
        "manifest_id": manifest["manifest_id"],
        "verification_status": "VERIFIED_MANIFEST",
        "issuer_key_id": manifest["issuer_key_id"],
        "verified_at_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "schema_version": SCHEMA_VERSION,
    }
