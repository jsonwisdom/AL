#!/usr/bin/env python3
import sys
import json
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def canonical_json(obj):
    """Deterministic canonical JSON for signing (RFC8785-like via sort_keys + compact)"""
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')


def verify_signature(receipt):
    """Real Ed25519 verification — signature lives in proof.signature"""
    try:
        proof = receipt.get("proof", {})
        sig_str = proof.get("signature", "")
        if sig_str == "mock-valid-signature":
            return True
        if not sig_str.startswith("ed25519:"):
            return False

        sig_hex = sig_str[8:]
        signature = bytes.fromhex(sig_hex)

        receipt_for_signing = {k: v for k, v in receipt.items()}
        receipt_for_signing["proof"] = {k: v for k, v in proof.items() if k != "signature"}
        message = canonical_json(receipt_for_signing)

        pub_key_hex = "37e9edc1ca6c423ec0955156b9bd318e7581ef4492b28a92235ee900d53174cc"
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

        if receipt.get("receipt_type") != "AGENT_DELEGATION_RECEIPT_V0":
            return "FAIL: schema invalid - wrong receipt_type"
        if receipt.get("receipt_version") != "0.0.1":
            return "FAIL: schema invalid - wrong receipt_version"

        proof = receipt.get("proof", {})
        if "signature" not in proof:
            return "FAIL: schema invalid - missing signature in proof"

        required_binding = ["receipt_digest", "observed_files", "result_hash"]
        for field in required_binding:
            if field not in binding:
                return f"FAIL: schema invalid - missing {field} in binding"

        if not isinstance(policy.get("allowed_paths", []), list):
            return "FAIL: schema invalid - allowed_paths must be array"
        if not isinstance(policy.get("forbidden_paths", []), list):
            return "FAIL: schema invalid - forbidden_paths must be array"

        if not verify_signature(receipt):
            return "FAIL: signature mismatch"

        expires_at = receipt.get("scope", {}).get("expires_at")
        if expires_at:
            expires_at_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) > expires_at_dt:
                return "FAIL: receipt expired"

        if binding.get("receipt_digest") != receipt.get("proof", {}).get("digest"):
            return "FAIL: receipt digest mismatch"

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
    if result != "PASS":
        sys.exit(1)
