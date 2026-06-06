#!/usr/bin/env python3
import sys
import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

V0_TEST_KEY_HEX = "37e9edc1ca6c423ec0955156b9bd318e7581ef4492b28a92235ee900d53174cc"


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def canonical_json(obj):
    """Deterministic canonical JSON for signing (RFC8785-like via sort_keys + compact)."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')


def is_hex_32_bytes(value):
    if not isinstance(value, str):
        return False
    if len(value) != 64:
        return False
    try:
        bytes.fromhex(value)
        return True
    except ValueError:
        return False


def resolve_did_key(did):
    """Minimal V1 DID resolver stub.

    V1 only defines deterministic failure modes for now. Real did:key
    multicodec/multibase decoding is intentionally deferred.
    """
    if not isinstance(did, str) or not did:
        return None, "FAIL: did resolution failed"
    if did.startswith("did:key:"):
        return None, "FAIL: did resolution unsupported"
    return None, "FAIL: did resolution unsupported"


def resolve_public_key(receipt):
    """Resolve Ed25519 public key bytes.

    V1 order:
    1. proof.public_key
    2. proof.did
    3. FAIL: public key missing

    V0 compatibility:
    - V0 receipts may fall back to the fixed conformance key.
    """
    proof = receipt.get("proof", {})
    receipt_type = receipt.get("receipt_type")

    public_key_hex = proof.get("public_key")
    if public_key_hex:
        if public_key_hex == "V1_PUBLIC_KEY_HEX_PENDING":
            return None, "FAIL: public key missing"
        if not is_hex_32_bytes(public_key_hex):
            return None, "FAIL: public key invalid"
        return bytes.fromhex(public_key_hex), None

    did = proof.get("did")
    if did:
        if did == "did:key:V1_DID_KEY_PENDING":
            return None, "FAIL: did resolution unsupported"
        return resolve_did_key(did)

    if receipt_type == "AGENT_DELEGATION_RECEIPT_V0":
        return bytes.fromhex(V0_TEST_KEY_HEX), None

    return None, "FAIL: public key missing"


def verify_signature(receipt):
    """V0 + V1 Ed25519 verification."""
    try:
        proof = receipt.get("proof", {})
        sig_str = proof.get("signature", "")
        if not sig_str.startswith("ed25519:"):
            return False, "FAIL: signature mismatch"

        sig_hex = sig_str[8:]
        signature = bytes.fromhex(sig_hex)

        receipt_for_signing = {k: v for k, v in receipt.items()}
        receipt_for_signing["proof"] = {k: v for k, v in proof.items() if k != "signature"}
        message = canonical_json(receipt_for_signing)

        public_key_bytes, error = resolve_public_key(receipt)
        if error:
            return False, error

        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature, message)
        return True, None
    except InvalidSignature:
        return False, "FAIL: signature mismatch"
    except ValueError:
        return False, "FAIL: public key invalid"
    except Exception:
        return False, "FAIL: signature mismatch"


def verify(receipt_path, binding_path, policy_path):
    try:
        receipt = load_json(receipt_path)
        binding = load_json(binding_path)
        policy = load_json(policy_path)

        receipt_type = receipt.get("receipt_type")
        receipt_version = receipt.get("receipt_version")

        if receipt_type not in ["AGENT_DELEGATION_RECEIPT_V0", "AGENT_DELEGATION_RECEIPT_V1"]:
            return "FAIL: schema invalid - wrong receipt_type"
        if receipt_type == "AGENT_DELEGATION_RECEIPT_V0" and receipt_version != "0.0.1":
            return "FAIL: schema invalid - wrong receipt_version"
        if receipt_type == "AGENT_DELEGATION_RECEIPT_V1" and receipt_version != "1.0.0":
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

        sig_valid, error = verify_signature(receipt)
        if not sig_valid:
            return error

        if binding.get("receipt_digest") != proof.get("digest"):
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
