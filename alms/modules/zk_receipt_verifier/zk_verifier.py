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


def _rollback_if_active(conn) -> None:
    try:
        conn.execute("ROLLBACK")
    except sqlite3.OperationalError:
        pass


def reserve_nullifier(registry_conn, promotion_id: str, nullifier: str):
    """Atomic nullifier reservation with BEGIN IMMEDIATE.

    Returns (reserved_nullifier, reason_code, reason_text).
    Exactly one caller may reserve a nullifier before proof verification.
    """
    registry_conn.execute("BEGIN IMMEDIATE")

    try:
        existing = registry_conn.execute(
            "SELECT consumed, attempt_status FROM consumption_registry WHERE nullifier_hash = ?",
            (nullifier,),
        ).fetchone()

        if existing:
            registry_conn.execute("ROLLBACK")
            if existing[0]:
                return None, "E001", "ALREADY_CONSUMED"
            return None, "E010", "ALREADY_RESERVED"

        registry_conn.execute(
            """
            INSERT INTO consumption_registry
            (promotion_id, consumed, nullifier_hash,
             consumption_type, last_attempt_at_unix_ms, attempt_status)
            VALUES (?, FALSE, ?, 'zk_pending', ?, 'reserved')
            """,
            (
                promotion_id,
                nullifier,
                now_ms(),
            ),
        )
        registry_conn.commit()
        return nullifier, None, None

    except Exception:
        _rollback_if_active(registry_conn)
        raise


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


def log_nullifier_lifecycle(
    nullifier: str,
    event_type: str,
    conn,
    metadata: Optional[Dict[str, Any]] = None,
):
    """Best-effort append-only lifecycle audit log.

    If the host schema does not include nullifier_lifecycle_log yet, skip without
    affecting verifier semantics.
    """
    try:
        conn.execute(
            """
            INSERT INTO nullifier_lifecycle_log
            (event_id, nullifier_hash, event_type, timestamp_unix_ms, metadata_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                sha256(f"{nullifier}:{event_type}:{now_ms()}"),
                nullifier,
                event_type,
                now_ms(),
                json.dumps(metadata or {}),
            ),
        )
        conn.commit()
    except sqlite3.OperationalError:
        pass


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
        _, err_code, err_text = reserve_nullifier(
            registry_conn,
            public_inputs["promotion_id"],
            nullifier,
        )
    except sqlite3.IntegrityError:
        log_zk_attempt(nullifier, "REJECTED", "E010", registry_conn)
        return {
            "result": "REJECTED",
            "reason_code": "E010",
            "reason_text": "ALREADY_RESERVED",
        }

    if err_code:
        log_zk_attempt(nullifier, "REJECTED", err_code, registry_conn)
        return {
            "result": "REJECTED",
            "reason_code": err_code,
            "reason_text": err_text,
        }

    log_nullifier_lifecycle(nullifier, "RESERVED", registry_conn)
    log_zk_attempt(nullifier, "ATTEMPT_STARTED", None, registry_conn)

    try:
        if not external_signature_checks(zk_proof.metadata):
            _update_attempt_status(
                registry_conn,
                nullifier,
                "REJECTED",
                "E002_BAD_SIGNATURE",
            )
            log_nullifier_lifecycle(nullifier, "REJECTED", registry_conn, {"reason_code": "E002_BAD_SIGNATURE"})
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
            log_nullifier_lifecycle(nullifier, "REJECTED", registry_conn, {"reason_code": "E007"})
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
            log_nullifier_lifecycle(nullifier, "REJECTED", registry_conn, {"reason_code": "E002_BAD_PROOF"})
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
            log_nullifier_lifecycle(nullifier, "REJECTED", registry_conn, {"reason_code": "E006"})
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
            log_nullifier_lifecycle(nullifier, "REJECTED", registry_conn, {"reason_code": "E005"})
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
            log_nullifier_lifecycle(nullifier, "REJECTED", registry_conn, {"reason_code": "E005"})
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
        log_nullifier_lifecycle(nullifier, "SUCCESS", registry_conn)

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
        log_nullifier_lifecycle(nullifier, "REJECTED", registry_conn, {"reason_code": "E099", "error": str(exc)})

        return {
            "result": "REJECTED",
            "reason_code": "E099",
            "reason_text": f"Internal error: {exc}",
        }
