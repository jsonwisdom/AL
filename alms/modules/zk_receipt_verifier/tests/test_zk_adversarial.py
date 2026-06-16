import sqlite3
import threading
from datetime import datetime, timedelta

import pytest

from runtime_lattice.zk_verifier import (
    present_zk_visa,
    get_hybrid_time,
)


class MockProof:
    def __init__(
        self,
        metadata_valid=True,
        revoked=False,
        corrupt_bytes=False,
    ):
        self.proof_bytes = b"mock_proof"
        if corrupt_bytes:
            self.proof_bytes = b"corrupt"

        self.metadata = {
            "signature_valid": metadata_valid,
            "key_revoked": revoked,
            "roles_ok": not revoked,
        }


class MockVerifier:
    def __init__(self, valid=True):
        self.valid = valid

    def verify(self, proof_bytes, public_inputs):
        return self.valid


@pytest.fixture

def registry():
    conn = sqlite3.connect(":memory:")

    conn.execute(
        """
        CREATE TABLE consumption_registry (
            promotion_id TEXT PRIMARY KEY,
            consumed BOOLEAN DEFAULT FALSE,
            nullifier_hash TEXT UNIQUE,
            consumption_type TEXT,
            attempt_status TEXT,
            reason_code TEXT,
            metadata TEXT,
            last_attempt_at_unix_ms INTEGER
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE attempt_log (
            attempt_id TEXT,
            promotion_id TEXT,
            timestamp_unix_ms INTEGER,
            result TEXT,
            reason_code TEXT,
            verifier_identity_hash TEXT,
            metadata_json TEXT
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE nullifier_lifecycle_log (
            event_id TEXT,
            nullifier_hash TEXT,
            event_type TEXT,
            timestamp_unix_ms INTEGER,
            metadata_json TEXT
        )
        """
    )

    return conn



def test_nullifier_replay(registry):
    nullifier = "0xdeadbeef"

    registry.execute(
        """
        INSERT INTO consumption_registry
        (promotion_id, consumed, nullifier_hash, attempt_status)
        VALUES (?, ?, ?, ?)
        """,
        ("promo_replay", 1, nullifier, "SUCCESS"),
    )
    registry.commit()

    result = present_zk_visa(
        zk_proof=MockProof(),
        public_inputs={
            "nullifier_hash": nullifier,
            "promotion_id": "promo_replay_2",
        },
        requested_primitive="TRANSFER",
        registry_conn=registry,
        noir_verifier=MockVerifier(valid=True),
    )

    assert result["reason_code"] == "E001"



def test_bad_proof_bytes(registry):
    nullifier = "0xbadproof"

    result = present_zk_visa(
        zk_proof=MockProof(corrupt_bytes=True),
        public_inputs={
            "nullifier_hash": nullifier,
            "promotion_id": "promo_badproof",
            "authorized_primitive": "TRANSFER",
        },
        requested_primitive="TRANSFER",
        registry_conn=registry,
        noir_verifier=MockVerifier(valid=False),
    )

    assert result["reason_code"] == "E002_BAD_PROOF"



def test_expired_proof_consumes(registry):
    nullifier = "0xexpired"
    past_time = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)

    result = present_zk_visa(
        zk_proof=MockProof(),
        public_inputs={
            "nullifier_hash": nullifier,
            "promotion_id": "promo_expired",
            "authorized_primitive": "TRANSFER",
            "valid_until": past_time,
            "valid_from": 0,
        },
        requested_primitive="TRANSFER",
        registry_conn=registry,
        noir_verifier=MockVerifier(valid=True),
    )

    assert result["reason_code"] == "E005"



def test_missing_public_input(registry):
    result = present_zk_visa(
        zk_proof=MockProof(),
        public_inputs={
            "nullifier_hash": "0xmissing",
        },
        requested_primitive="TRANSFER",
        registry_conn=registry,
        noir_verifier=MockVerifier(valid=True),
    )

    assert result["reason_code"] == "E009"



def test_revoked_key_metadata_fail(registry):
    nullifier = "0xrevoked"

    result = present_zk_visa(
        zk_proof=MockProof(revoked=True),
        public_inputs={
            "nullifier_hash": nullifier,
            "promotion_id": "promo_revoked",
            "authorized_primitive": "TRANSFER",
        },
        requested_primitive="TRANSFER",
        registry_conn=registry,
        noir_verifier=MockVerifier(valid=True),
    )

    assert result["reason_code"] == "E007"



def test_concurrent_double_submit_with_begin_immediate(tmp_path):
    """File-backed concurrency test for BEGIN IMMEDIATE reservation semantics."""
    db_path = tmp_path / "zk_registry.sqlite"

    bootstrap = sqlite3.connect(str(db_path), isolation_level=None)

    bootstrap.execute(
        """
        CREATE TABLE consumption_registry (
            promotion_id TEXT PRIMARY KEY,
            consumed BOOLEAN DEFAULT FALSE,
            nullifier_hash TEXT UNIQUE,
            consumption_type TEXT,
            attempt_status TEXT,
            reason_code TEXT,
            metadata TEXT,
            last_attempt_at_unix_ms INTEGER
        )
        """
    )

    bootstrap.execute(
        """
        CREATE TABLE attempt_log (
            attempt_id TEXT,
            promotion_id TEXT,
            timestamp_unix_ms INTEGER,
            result TEXT,
            reason_code TEXT,
            verifier_identity_hash TEXT,
            metadata_json TEXT
        )
        """
    )

    bootstrap.execute(
        """
        CREATE TABLE nullifier_lifecycle_log (
            event_id TEXT,
            nullifier_hash TEXT,
            event_type TEXT,
            timestamp_unix_ms INTEGER,
            metadata_json TEXT
        )
        """
    )
    bootstrap.close()

    nullifier = "0xrace_test"
    results = []
    errors = []
    lock = threading.Lock()

    def worker(worker_id):
        try:
            conn = sqlite3.connect(
                str(db_path),
                timeout=5.0,
                isolation_level=None,
            )

            result = present_zk_visa(
                zk_proof=MockProof(),
                public_inputs={
                    "nullifier_hash": nullifier,
                    "promotion_id": f"promo_{worker_id}",
                    "authorized_primitive": "TRANSFER",
                },
                requested_primitive="TRANSFER",
                registry_conn=conn,
                noir_verifier=MockVerifier(valid=True),
            )

            with lock:
                results.append(result)

            conn.close()

        except Exception as exc:
            with lock:
                errors.append(str(exc))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    successes = [r for r in results if r.get("result") != "REJECTED"]
    rejections = [r for r in results if r.get("result") == "REJECTED"]

    assert len(successes) == 1
    assert len(errors) == 0

    for rejected in rejections:
        assert rejected["reason_code"] in ("E001", "E010")
