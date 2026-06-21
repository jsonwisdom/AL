#!/usr/bin/env python3
import json
import hashlib
import sys
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_receipt(receipt_path: Path) -> dict:
    with receipt_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def decode_public_key(public_key_str: str) -> Ed25519PublicKey:
    if not public_key_str.startswith("ed25519:"):
        raise ValueError("public_key must start with ed25519:")
    key_hex = public_key_str.split(":", 1)[1]
    return Ed25519PublicKey.from_public_bytes(bytes.fromhex(key_hex))


def load_signature(receipt: dict, receipt_path: Path) -> bytes:
    inline_hex = receipt.get("signature")
    if not inline_hex:
        raise ValueError("missing inline signature field")

    inline_sig = bytes.fromhex(inline_hex)
    cose_path = receipt_path.with_suffix(".cose")

    if cose_path.exists():
        detached_sig = cose_path.read_bytes()
        if detached_sig != inline_sig:
            print("⚠ detached .cose signature differs from inline signature; using inline signature")
    else:
        print("⚠ detached .cose file not found; using inline signature only")

    return inline_sig


def verify_signature(receipt: dict, receipt_path: Path) -> bool:
    public_key = decode_public_key(receipt["public_key"])
    signature = load_signature(receipt, receipt_path)
    replay_status = receipt.get("replay_status")

    payloads = []

    if replay_status == "PASS":
        if "normalized_data" not in receipt:
            raise ValueError("PASS receipt missing normalized_data")
        payloads.append(("normalized_data", canonical_json(receipt["normalized_data"])))
    else:
        # Committed intake signs the full failure receipt before adding signature.
        failure_full = dict(receipt)
        failure_full.pop("signature", None)
        payloads.append(("failure_receipt_without_signature", canonical_json(failure_full)))

        # Fallback for older/verifier-draft receipts that signed only the minimal failure claim.
        minimal_failure = {
            "target_date": receipt.get("target_date"),
            "replay_status": receipt.get("replay_status"),
            "reason": receipt.get("reason"),
        }
        payloads.append(("minimal_failure_claim", canonical_json(minimal_failure)))

    for payload_name, payload in payloads:
        try:
            public_key.verify(signature, payload)
            print(f"✓ signature verifies over {payload_name}")
            return True
        except InvalidSignature:
            continue

    raise InvalidSignature("signature did not verify against any accepted payload mode")


def verify_pass_hashes(receipt: dict, receipt_path: Path) -> None:
    normalized = receipt.get("normalized_data")
    if normalized is None:
        raise ValueError("PASS receipt missing normalized_data")

    computed_norm_hash = sha256_hex(canonical_json(normalized))
    expected_norm_hash = receipt.get("normalized_receipt_hash")
    if computed_norm_hash != expected_norm_hash:
        raise ValueError(f"normalized_receipt_hash mismatch: expected {expected_norm_hash}, got {computed_norm_hash}")
    print("✓ normalized receipt hash matches")

    raw_path = receipt_path.parent / "raw_snapshot.json"
    raw_hash_path = receipt_path.parent / "raw_snapshot.hash"
    if not raw_path.exists():
        raise ValueError("raw_snapshot.json missing for PASS receipt")
    if not raw_hash_path.exists():
        raise ValueError("raw_snapshot.hash missing for PASS receipt")

    computed_raw_hash = sha256_hex(raw_path.read_bytes())
    expected_raw_hash = raw_hash_path.read_text(encoding="utf-8").strip()
    receipt_raw_hash = receipt.get("raw_snapshot_hash")

    if computed_raw_hash != expected_raw_hash:
        raise ValueError(f"raw_snapshot.hash mismatch: expected {expected_raw_hash}, got {computed_raw_hash}")
    if computed_raw_hash != receipt_raw_hash:
        raise ValueError(f"receipt raw_snapshot_hash mismatch: expected {receipt_raw_hash}, got {computed_raw_hash}")
    print("✓ raw snapshot hash matches")

    if not receipt.get("normalizer_code_hash"):
        raise ValueError("normalizer_code_hash missing")
    print("✓ normalizer_code_hash present")


def verify_parent_chain(receipt: dict, receipt_path: Path) -> None:
    parent = receipt.get("parent_receipt_hash")
    if parent is None:
        print("✓ parent_receipt_hash is GENESIS/null")
        return

    if not isinstance(parent, str) or not parent.startswith("sha256:"):
        raise ValueError("parent_receipt_hash must be null or sha256:<hex>")

    print("✓ parent_receipt_hash present")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python verify_receipt.py receipts/YYYY-MM-DD/normalized_receipt.json")
        return 2

    receipt_path = Path(sys.argv[1])
    receipt = load_receipt(receipt_path)

    replay_status = receipt.get("replay_status")
    authority = receipt.get("authority_level")
    print(f"Status: {replay_status} | Authority: {authority}")

    if not receipt.get("public_key"):
        raise ValueError("public_key missing")
    decode_public_key(receipt["public_key"])
    print("✓ public key decodes")

    verify_signature(receipt, receipt_path)
    verify_parent_chain(receipt, receipt_path)

    if replay_status == "PASS":
        verify_pass_hashes(receipt, receipt_path)
        print("SHADOW_AUDIT ready")
    else:
        print("✓ failure receipt verified")
        print("OBSERVATION_ONLY preserved")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"✗ verification failed: {e}")
        raise SystemExit(1)
