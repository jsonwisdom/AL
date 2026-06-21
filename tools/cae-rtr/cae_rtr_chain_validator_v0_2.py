#!/usr/bin/env python3
"""
CAAE-RTR Chain Validator v0.2

Validates remediation receipt windows with:
- service-scoped hash chaining
- canonical receipt hashes
- Merkle root over receipt_hash values
- scoped duplicate finding guard
- logical sequence monotonicity
- Boss Lock remediation audit
- optional Ed25519 signature verification over the Merkle root

Doctrine: Discovery creates debt. Replay-verified remediation closes debt. Everything else is narrative.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

HASH_PREFIX = "sha256:"
PASS_EXPLOIT_BLOCKED = "PASS_EXPLOIT_BLOCKED"
PASS_REPLAY = "PASS"
REMEDIATED = "REMEDIATION_RECEIPTED"
DEBT = "DEBT_ACCUMULATING"

DERIVED_FIELDS = {
    "receipt_hash",
    "ledger_signature",
    "window_merkle_root",
    "window_signature",
}

INTEGRITY_FAILURE_STATUSES = {
    "LEDGER_CHAIN_BROKEN",
    "LEDGER_INTEGRITY_ERROR",
    "MERKLE_ROOT_MISMATCH",
    "LEDGER_SIGNATURE_INVALID",
    "DUPLICATE_FINDING_ATTEMPT",
    "RECEIPT_HASH_MISMATCH",
    "SEQUENCE_REGRESSION",
}


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(data: bytes) -> str:
    return HASH_PREFIX + hashlib.sha256(data).hexdigest()


def canonical_receipt_material(receipt: Dict[str, Any]) -> Dict[str, Any]:
    material = copy.deepcopy(receipt)
    for field in DERIVED_FIELDS:
        material.pop(field, None)
    return material


def compute_receipt_hash(receipt: Dict[str, Any]) -> str:
    material = canonical_json(canonical_receipt_material(receipt)).encode("utf-8")
    return sha256_hex(material)


def merkle_root(leaves: Iterable[str]) -> str:
    layer = [leaf if leaf.startswith(HASH_PREFIX) else sha256_hex(leaf.encode("utf-8")) for leaf in leaves]
    if not layer:
        return sha256_hex(b"")
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        next_layer = []
        for left, right in zip(layer[0::2], layer[1::2]):
            payload = (left + right).encode("utf-8")
            next_layer.append(sha256_hex(payload))
        layer = next_layer
    return layer[0]


def parse_utc_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp_utc must include timezone")
    return parsed.astimezone(timezone.utc)


def verify_ed25519_signature(public_key_hex: str, signature_hex: str, message: str) -> Tuple[bool, str]:
    """Verify Ed25519 signature over UTF-8 message.

    Uses cryptography when available. If a signature is supplied but the dependency
    is missing, fail closed rather than fake-greening the signature check.
    """
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except Exception as exc:  # pragma: no cover - dependency may not exist in minimal runtimes
        return False, f"cryptography dependency unavailable: {exc}"

    try:
        public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))
        public_key.verify(bytes.fromhex(signature_hex), message.encode("utf-8"))
        return True, "signature verified"
    except Exception as exc:
        return False, f"signature invalid: {exc}"


def boss_lock_status(receipt: Dict[str, Any]) -> str:
    if receipt.get("severity") != "critical":
        return receipt.get("status", "UNVERIFIED_FINDING")
    if (
        receipt.get("post_patch_replay") == PASS_EXPLOIT_BLOCKED
        and receipt.get("replay_verdict") == PASS_REPLAY
        and receipt.get("status") == REMEDIATED
    ):
        return REMEDIATED
    return DEBT


def validate_receipts(
    receipts: List[Dict[str, Any]],
    expected_merkle_root: Optional[str] = None,
    public_key_hex: Optional[str] = None,
    signature_hex: Optional[str] = None,
    strict_timestamps: bool = False,
) -> Dict[str, Any]:
    audited: List[Dict[str, Any]] = []
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []
    by_service: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for raw in receipts:
        receipt = copy.deepcopy(raw)
        receipt_hash = compute_receipt_hash(receipt)
        claimed_hash = receipt.get("receipt_hash")
        if claimed_hash and claimed_hash != receipt_hash:
            receipt["status"] = "RECEIPT_HASH_MISMATCH"
            errors.append({
                "status": "RECEIPT_HASH_MISMATCH",
                "service": str(receipt.get("service")),
                "finding_hash": str(receipt.get("finding_hash")),
            })
        receipt["computed_receipt_hash"] = receipt_hash
        receipt["receipt_hash"] = claimed_hash or receipt_hash
        by_service[str(receipt.get("service"))].append(receipt)

    for service, service_receipts in by_service.items():
        service_receipts.sort(key=lambda r: (r.get("sequence", -1), r.get("receipt_hash", "")))
        previous_hash: Optional[str] = None
        previous_sequence: Optional[int] = None
        seen_findings: Dict[str, str] = {}
        previous_transition_ts: Optional[datetime] = None

        for receipt in service_receipts:
            sequence = receipt.get("sequence")
            if not isinstance(sequence, int):
                receipt["status"] = "LEDGER_INTEGRITY_ERROR"
                errors.append({"status": "LEDGER_INTEGRITY_ERROR", "service": service, "detail": "sequence must be integer"})
            elif previous_sequence is not None and sequence <= previous_sequence:
                receipt["status"] = "SEQUENCE_REGRESSION"
                errors.append({"status": "SEQUENCE_REGRESSION", "service": service, "detail": f"sequence {sequence} after {previous_sequence}"})
            previous_sequence = sequence if isinstance(sequence, int) else previous_sequence

            expected_prev = previous_hash
            claimed_prev = receipt.get("prev_receipt_hash")
            if expected_prev is None:
                if claimed_prev not in (None, "", "GENESIS"):
                    receipt["status"] = "LEDGER_CHAIN_BROKEN"
                    errors.append({"status": "LEDGER_CHAIN_BROKEN", "service": service, "detail": "genesis receipt has non-empty previous hash"})
            elif claimed_prev != expected_prev:
                receipt["status"] = "LEDGER_CHAIN_BROKEN"
                errors.append({"status": "LEDGER_CHAIN_BROKEN", "service": service, "detail": "prev_receipt_hash mismatch"})

            finding_hash = receipt.get("finding_hash")
            if finding_hash:
                first_seen = seen_findings.get(finding_hash)
                first_seen_ptr = receipt.get("first_seen_receipt_hash")
                if first_seen and first_seen_ptr != first_seen:
                    receipt["status"] = "DUPLICATE_FINDING_ATTEMPT"
                    errors.append({"status": "DUPLICATE_FINDING_ATTEMPT", "service": service, "finding_hash": finding_hash})
                seen_findings.setdefault(finding_hash, receipt.get("receipt_hash"))

            for transition in receipt.get("transition_timestamps", []) or []:
                try:
                    ts = parse_utc_timestamp(transition["timestamp_utc"])
                except Exception as exc:
                    receipt["status"] = "LEDGER_INTEGRITY_ERROR"
                    errors.append({"status": "LEDGER_INTEGRITY_ERROR", "service": service, "detail": f"bad timestamp: {exc}"})
                    continue
                if previous_transition_ts and ts < previous_transition_ts:
                    entry = {"status": "TIMESTAMP_REGRESSION", "service": service, "detail": transition.get("state", "unknown")}
                    if strict_timestamps:
                        receipt["status"] = "LEDGER_INTEGRITY_ERROR"
                        errors.append(entry)
                    else:
                        warnings.append(entry)
                previous_transition_ts = ts

            if receipt.get("status") not in INTEGRITY_FAILURE_STATUSES:
                receipt["status"] = boss_lock_status(receipt)
            previous_hash = receipt.get("receipt_hash")
            audited.append(receipt)

    receipt_hashes = [r["receipt_hash"] for r in sorted(audited, key=lambda r: (str(r.get("service")), int(r.get("sequence", -1))))]
    computed_root = merkle_root(receipt_hashes)
    if expected_merkle_root and expected_merkle_root != computed_root:
        errors.append({"status": "MERKLE_ROOT_MISMATCH", "detail": "expected window root does not match computed root"})

    if public_key_hex or signature_hex:
        if not public_key_hex or not signature_hex:
            errors.append({"status": "LEDGER_SIGNATURE_INVALID", "detail": "public key and signature are both required"})
        else:
            ok, detail = verify_ed25519_signature(public_key_hex, signature_hex, computed_root)
            if not ok:
                errors.append({"status": "LEDGER_SIGNATURE_INVALID", "detail": detail})

    critical_findings = sum(1 for r in audited if r.get("severity") == "critical")
    verified_remediations = sum(
        1 for r in audited
        if r.get("severity") == "critical" and r.get("status") == REMEDIATED
    )
    debt = sum(1 for r in audited if r.get("status") == DEBT)

    integrity_failed = bool(errors)
    if integrity_failed:
        rtr = 0.0
        governor_status = "LEDGER_INTEGRITY_INCIDENT"
        rtr_reason = "LEDGER_INTEGRITY_FAILURE"
    elif critical_findings == 0:
        if verified_remediations == 0:
            rtr = 1.0
            governor_status = "STABLE_EMPTY_WINDOW"
            rtr_reason = "NO_CRITICAL_FINDINGS"
        else:
            rtr = 0.0
            governor_status = "LEDGER_INTEGRITY_INCIDENT"
            rtr_reason = "REMEDIATIONS_WITHOUT_FINDINGS"
    else:
        rtr = verified_remediations / critical_findings
        if rtr < 1.0:
            governor_status = "FEATURE_FREEZE_REQUIRED"
            rtr_reason = "REMEDIATION_DEBT"
        else:
            governor_status = "STABLE"
            rtr_reason = "RTR_OK"

    return {
        "schema": "CAAE_RTR_WINDOW_VERIFICATION_V0_2",
        "window_merkle_root": computed_root,
        "critical_findings": critical_findings,
        "verified_remediations": verified_remediations,
        "debt_accumulating_count": debt,
        "rtr": round(rtr, 4),
        "rtr_reason": rtr_reason,
        "governor_status": governor_status,
        "errors": errors,
        "warnings": warnings,
        "audited_receipts": audited,
    }


def load_receipts(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("receipts"), list):
        return data["receipts"]
    raise ValueError("input must be a JSON list or an object with receipts[]")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a CAAE-RTR v0.2 remediation receipt window")
    parser.add_argument("input_json", help="JSON list of receipts or object with receipts[]")
    parser.add_argument("--expected-merkle-root", default=None)
    parser.add_argument("--public-key-hex", default=None)
    parser.add_argument("--signature-hex", default=None)
    parser.add_argument("--strict-timestamps", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        result = validate_receipts(
            load_receipts(args.input_json),
            expected_merkle_root=args.expected_merkle_root,
            public_key_hex=args.public_key_hex,
            signature_hex=args.signature_hex,
            strict_timestamps=args.strict_timestamps,
        )
    except Exception as exc:
        print(json.dumps({"status": "VALIDATOR_ERROR", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 1 if result["governor_status"] == "LEDGER_INTEGRITY_INCIDENT" else 0


if __name__ == "__main__":
    raise SystemExit(main())
