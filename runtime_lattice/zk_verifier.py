import hashlib
import json
import sqlite3
import time
from typing import Dict, Any, Optional


def now_ms() -> int:
    return int(time.time() * 1000)


def get_hybrid_time(block_timestamp: Optional[int] = None) -> int:
    if block_timestamp is not None:
        return block_timestamp
    return now_ms()


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def external_signature_checks(metadata: Dict[str, Any]) -> bool:
    return metadata.get("signature_valid", True)


def external_role_revocation_checks(metadata: Dict[str, Any]) -> bool:
    return not metadata.get("key_revoked", False)


def execute_primitive(primitive: str, context: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "executed",
        "primitive": primitive,
        "context": context,
    }


def _update_attempt_status(
    conn,
    nullifier: str,
    status: str,
    reason_code: Optional[str],
    metadata: Optional[Dict[str, Any]] = None,
):
    consumed = 1 if status in ("SUCCESS", "REJECTED") else 0

    conn.execute(
        """
        UPDATE consumption_registry
        SET consumed = ?,
            consumption_type = ?,
            attempt_status = ?,
            reason_code = ?,
            metadata = ?
        WHERE nullifier_hash = ?
        """,
        (
            consumed,
            f"zk_v1_{status.lower()}",
            status,
            reason_code,
            json.dumps(metadata or {}),
            nullifier,
        ),
    )
    conn.commit()



def log_zk_attempt(
    nullifier: str,
    result: str,
    reason_code: Optional[str],
    conn,
    metadata: Optional[Dict[str, Any]] = None,
):
    attempt_id = sha256(f"{nullifier}:{now_ms()}:{result}")

    conn.execute(
        """
        INSERT INTO attempt_log
        (attempt_id, promotion_id, timestamp_unix_ms, result,
         reason_code, verifier_identity_hash, metadata_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            attempt_id,
            f"zk_{nullifier[:16]}",
            now_ms(),
            result,
            reason_code,
            "zk_verifier_v1",
            json.dumps(metadata or {}),
        ),
    )
    conn.commit()
    return attempt_id


class ZKVerificationError(Exception):
    pass



def present_zk_visa(
    zk_proof,
    public_inputs,
    requested_primitive,
    registry_conn,
    noir_verifier,
):
    required_minimal = ["nullifier_hash", "promotion_id"]

    for field in required_minimal:
        if field not in public_inputs:
            return {
                "result": "REJECTED",
                "reason_code": "E009",
                "reason_text": f"MISSING_PUBLIC_INPUT_{field}",
            }

    nullifier = public_inputs["nullifier_hash"]

    try:
        registry_conn.execute(
            """
            INSERT INTO consumption_registry
            (promotion_id, consumed, nullifier_hash,
             consumption_type, last_attempt_at_unix_ms, attempt_status)
            VALUES (?, FALSE, ?, 'zk_pending', ?, 'reserved')
            """,
            (
                public_inputs["promotion_id"],
                nullifier,
                now_ms(),
            ),
        )
        registry_conn.commit()

    except sqlite3.IntegrityError:
        status = registry_conn.execute(
            "SELECT consumed, attempt_status FROM consumption_registry WHERE nullifier_hash = ?",
            (nullifier,),
        ).fetchone()

        if status and status[0]:
            log_zk_attempt(nullifier, "REJECTED", "E001", registry_conn)
            return {
                "result": "REJECTED",
                "reason_code": "E001",
                "reason_text": "ALREADY_CONSUMED",
            }

        log_zk_attempt(nullifier, "REJECTED", "E010", registry_conn)
        return {
            "result": "REJECTED",
            "reason_code": "E010",
            "reason_text": "ALREADY_RESERVED",
        }

    log_zk_attempt(nullifier, "ATTEMPT_STARTED", None, registry_conn)

    try:
        if not external_signature_checks(zk_proof.metadata):
            _update_attempt_status(
                registry_conn,
                nullifier,
                "REJECTED",
                "E002_BAD_SIGNATURE",
            )
            return {
                "result": "REJECTED",
                "reason_code": "E002_BAD_SIGNATURE",
                "reason_text": "Invalid signatures",
            }

        if not external_role_revocation_checks(zk_proof.metadata):
            _update_attempt_status(
                registry_conn,
                nullifier,
                "REJECTED",
                "E007",
            )
            return {
                "result": "REJECTED",
                "reason_code": "E007",
                "reason_text": "Revoked or invalid key",
            }

        proof_valid = noir_verifier.verify(
            zk_proof.proof_bytes,
            public_inputs,
        )

        if not proof_valid:
            _update_attempt_status(
                registry_conn,
                nullifier,
                "REJECTED",
                "E002_BAD_PROOF",
            )
            return {
                "result": "REJECTED",
                "reason_code": "E002_BAD_PROOF",
                "reason_text": "ZK proof invalid",
            }

        if requested_primitive != public_inputs.get("authorized_primitive"):
            _update_attempt_status(
                registry_conn,
                nullifier,
                "REJECTED",
                "E006",
            )
            return {
                "result": "REJECTED",
                "reason_code": "E006",
                "reason_text": "SCOPE_VIOLATION",
            }

        now = get_hybrid_time()

        if now < public_inputs.get("valid_from", 0):
            _update_attempt_status(
                registry_conn,
                nullifier,
                "REJECTED",
                "E005",
            )
            return {
                "result": "REJECTED",
                "reason_code": "E005",
                "reason_text": "NOT_YET_VALID",
            }

        if now > public_inputs.get("valid_until", float("inf")):
            _update_attempt_status(
                registry_conn,
                nullifier,
                "REJECTED",
                "E005",
            )
            return {
                "result": "REJECTED",
                "reason_code": "E005",
                "reason_text": "EXPIRED",
            }

        execution_result = execute_primitive(
            requested_primitive,
            {"nullifier": nullifier},
        )

        _update_attempt_status(
            registry_conn,
            nullifier,
            "SUCCESS",
            None,
        )

        return {
            "result": execution_result,
            "promotion_receipt_status": "CONSUMED",
            "nullifier_hash": nullifier,
            "consumption_type": "zk_v1",
        }

    except Exception as exc:
        _update_attempt_status(
            registry_conn,
            nullifier,
            "REJECTED",
            "E099",
            {"error": str(exc)},
        )

        return {
            "result": "REJECTED",
            "reason_code": "E099",
            "reason_text": f"Internal error: {exc}",
        }
