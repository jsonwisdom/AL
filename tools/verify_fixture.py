#!/usr/bin/env python3
import sys
import json
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def canonical_json(obj):
    """Deterministic canonical JSON for signing (RFC8785-like via sort_keys + compact)"""
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')


def verify_signature(receipt):
    """Real Ed25519 verification for V0 test vector"""
    try:
        sig_str = receipt.get("signature", "")
        if not sig_str.startswith("ed25519:"):
            return False

        sig_hex = sig_str[8:]
        signature = bytes.fromhex(sig_hex)

        # Receipt without signature for signing
        receipt_for_signing = {k: v for k, v in receipt.items() if k != "signature"}
        message = canonical_json(receipt_for_signing)

        # V0 test vector public key (hardcoded for fixtures only)
        pub_key_hex = "e0b72d1d54cbf9ab369cc17425a87405541576972493adff635673050da0b7a1"
        pub_key_bytes = bytes.fromhex(pub_key_hex)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)

        public_key.verify(signature, message)
        return True
    except (InvalidSignature, ValueError, Exception):
        return False


def verify(receipt_path, binding_path, policy_path):
    try:
        receipt = load_json(receipt_path)
        binding = load_json(binding_path)
        policy = load_json(policy_path)

        # === SCHEMA ENFORCEMENT ===
        required_receipt = ["version", "issuer", "subject", "scope", "issued_at", "expires_at", "receipt_digest", "signature"]
        for field in required_receipt:
            if field not in receipt:
                return f"FAIL: schema invalid - missing {field} in receipt"

        if receipt.get("version") != "V0":
            return "FAIL: schema invalid - wrong version"

        required_binding = ["receipt_digest", "observed_files", "result_hash"]
        for field in required_binding:
            if field not in binding:
                return f"FAIL: schema invalid - missing {field} in binding"

        # Policy structure
        if not isinstance(policy.get("allowed_paths", []), list):
            return "FAIL: schema invalid - allowed_paths must be array"
        if not isinstance(policy.get("forbidden_paths", []), list):
            return "FAIL: schema invalid - forbidden_paths must be array"

        # === CRYPTO + REPLAY LOGIC ===
        if not verify_signature(receipt):
            return "FAIL: signature mismatch"

        # Expiration
        now = int(datetime.now().timestamp())
        if now > receipt.get("expires_at", 0):
            return "FAIL: receipt expired"

        # Binding digest match
        if binding.get("receipt_digest") != receipt.get("receipt_digest"):
            return "FAIL: receipt digest mismatch"

        # Policy enforcement
        observed = set(binding.get("observed_files", []))
        allowed = set(policy.get("allowed_paths", []))
        forbidden = set(policy.get("forbidden_paths", []))

        if observed & forbidden:
            forbidden_file = next(iter(observed & forbidden))
            return f"FAIL: forbidden file touched: {forbidden_file}"

        if not observed.issubset(allowed):
            return "FAIL: scope violation - unauthorized file touched"

        return "PASS"

    except Exception as e:
        return f"FAIL: error - {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python verify_fixture.py <receipt.json> <binding.json> <policy.json>")
        sys.exit(1)

    result = verify(sys.argv[1], sys.argv[2], sys.argv[3])
    print(result)
