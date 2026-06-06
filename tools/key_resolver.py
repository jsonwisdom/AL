#!/usr/bin/env python3
"""Minimal key resolver for Replay Loop V1.

Supports the V1 verifier contract while keeping DID expansion isolated from
`verify_fixture.py`. Real did:key multibase/multicodec decoding is intentionally
reserved for a later commit.
"""


def is_hex_32_bytes(value: str) -> bool:
    if not isinstance(value, str):
        return False
    if len(value) != 64:
        return False
    try:
        bytes.fromhex(value)
        return True
    except ValueError:
        return False


def resolve_did_key(did: str) -> tuple[bytes | None, str | None]:
    """Resolve a did:key value into raw Ed25519 public-key bytes.

    Returns:
        (pub_key_bytes, error_message)
    """
    if not did or not isinstance(did, str):
        return None, "FAIL: did resolution failed"
    if not did.startswith("did:key:"):
        return None, "FAIL: did resolution unsupported"

    # Placeholder for real multibase decoding, e.g. did:key:z6Mk...
    return None, "FAIL: did resolution unsupported"


def resolve_public_key_from_proof(proof: dict) -> tuple[bytes | None, str | None]:
    """Resolve V1 proof key material.

    Resolution order:
    1. proof.public_key
    2. proof.did
    3. FAIL: public key missing
    """
    if "public_key" in proof and proof.get("public_key"):
        pk_hex = proof["public_key"].strip()
        if pk_hex == "V1_PUBLIC_KEY_HEX_PENDING":
            return None, "FAIL: public key missing"
        if is_hex_32_bytes(pk_hex):
            return bytes.fromhex(pk_hex), None
        return None, "FAIL: public key invalid"

    if "did" in proof and proof.get("did"):
        did = proof["did"].strip()
        if did == "did:key:V1_DID_KEY_PENDING":
            return None, "FAIL: did resolution unsupported"
        return resolve_did_key(did)

    return None, "FAIL: public key missing"
