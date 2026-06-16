import base58


class DidKeyError(ValueError):
    pass


def decode_did_key(did: str) -> bytes:
    """Decode did:key Ed25519 into a raw 32-byte public key.

    V1.1 decoder law:
    - DID must start with did:key:z
    - Payload must be base58btc
    - Decoded payload must be exactly 34 bytes
    - First two bytes must be ed01
    - Remaining 32 bytes are the Ed25519 public key
    """
    prefix = "did:key:z"

    if not isinstance(did, str):
        raise DidKeyError("did must be a string")

    if not did.startswith(prefix):
        raise DidKeyError("invalid did:key prefix")

    payload = did[len(prefix):]
    if not payload:
        raise DidKeyError("missing base58btc payload")

    try:
        data = base58.b58decode(payload)
    except Exception as exc:
        raise DidKeyError("invalid base58btc payload") from exc

    if len(data) != 34:
        raise DidKeyError("invalid multicodec length")

    if data[0] != 0xED or data[1] != 0x01:
        raise DidKeyError("invalid multicodec prefix")

    raw32 = data[2:]
    if len(raw32) != 32:
        raise DidKeyError("invalid key length")

    return raw32
