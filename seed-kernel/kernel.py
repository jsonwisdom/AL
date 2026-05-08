#!/usr/bin/env python3
"""
Seed Epistemic Kernel v0

Local-first primitives for forkable reasoning custody.

Claim      = epistemic state
Transform  = epistemic motion

The ledger records transformations, not the world.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = "kernel.db"


@dataclass(frozen=True)
class Claim:
    id: str
    body: str
    asserted_at: int
    asserted_by: str
    uncertainty: float
    tags: List[str]
    source_refs: List[str]
    branch: str


@dataclass(frozen=True)
class TransformReceipt:
    id: str
    timestamp: int
    input_claim_ids: List[str]
    output_claim_id: str
    operation: str
    operation_params: Dict[str, Any]
    policy: str
    signed_by: List[str]


class Kernel:
    def __init__(self, name: str, db_path: str = DB_PATH):
        self.name = name
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS claims (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS transforms (
                id TEXT PRIMARY KEY,
                output_claim_id TEXT NOT NULL,
                data TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_transforms_output_claim_id
                ON transforms(output_claim_id);
            """
        )
        self.conn.commit()

    @staticmethod
    def _canonical(obj: Dict[str, Any]) -> bytes:
        return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")

    @staticmethod
    def _hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def assert_claim(
        self,
        body: str,
        uncertainty: float = 0.0,
        tags: Optional[List[str]] = None,
        source_refs: Optional[List[str]] = None,
        branch: str = "main",
    ) -> str:
        payload = {
            "id": None,
            "body": body,
            "asserted_at": int(time.time()),
            "asserted_by": self.name,
            "uncertainty": float(uncertainty),
            "tags": tags or [],
            "source_refs": source_refs or [],
            "branch": branch,
        }
        claim_id = self._hash(self._canonical(payload))
        payload["id"] = claim_id
        data = self._canonical(payload).decode("utf-8")
        self.conn.execute("INSERT OR IGNORE INTO claims VALUES (?, ?)", (claim_id, data))
        self.conn.commit()
        print(f"✅ Claim asserted [{claim_id[:12]}...] by {self.name}")
        return claim_id

    def transform(
        self,
        input_ids: List[str],
        operation: str,
        policy: str,
        output_body: str,
        uncertainty: float = 0.1,
        params: Optional[Dict[str, Any]] = None,
        branch: str = "main",
    ) -> str:
        missing = [claim_id for claim_id in input_ids if not self.get_claim(claim_id)]
        if missing:
            raise ValueError(f"missing input claims: {missing}")

        output_id = self.assert_claim(
            output_body,
            uncertainty=uncertainty,
            tags=[operation],
            source_refs=input_ids,
            branch=branch,
        )

        payload = {
            "id": None,
            "timestamp": int(time.time()),
            "input_claim_ids": input_ids,
            "output_claim_id": output_id,
            "operation": operation,
            "operation_params": params or {},
            "policy": policy,
            "signed_by": [self.name],
        }
        transform_id = self._hash(self._canonical(payload))
        payload["id"] = transform_id
        data = self._canonical(payload).decode("utf-8")
        self.conn.execute(
            "INSERT OR IGNORE INTO transforms VALUES (?, ?, ?)",
            (transform_id, output_id, data),
        )
        self.conn.commit()
        print(f"🔄 Transform [{transform_id[:12]}...] | {operation} → {output_id[:12]}...")
        return output_id

    def get_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        row = self.conn.execute("SELECT data FROM claims WHERE id = ?", (claim_id,)).fetchone()
        return json.loads(row["data"]) if row else None

    def get_transform_for_output(self, claim_id: str) -> Optional[Dict[str, Any]]:
        row = self.conn.execute(
            "SELECT data FROM transforms WHERE output_claim_id = ? ORDER BY id LIMIT 1",
            (claim_id,),
        ).fetchone()
        return json.loads(row["data"]) if row else None

    def list_claims(self) -> List[Dict[str, Any]]:
        rows = self.conn.execute("SELECT data FROM claims ORDER BY id").fetchall()
        return [json.loads(row["data"]) for row in rows]

    def list_transforms(self) -> List[Dict[str, Any]]:
        rows = self.conn.execute("SELECT data FROM transforms ORDER BY id").fetchall()
        return [json.loads(row["data"]) for row in rows]

    def export_json(self, path: str) -> None:
        bundle = {
            "kernel_bundle": "SEED_EPISTEMIC_KERNEL_V0",
            "exported_by": self.name,
            "exported_at": int(time.time()),
            "claims": self.list_claims(),
            "transforms": self.list_transforms(),
        }
        Path(path).write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
        print(f"📦 Exported {len(bundle['claims'])} claims, {len(bundle['transforms'])} transforms → {path}")

    def import_json(self, path: str) -> None:
        bundle = json.loads(Path(path).read_text(encoding="utf-8"))
        for claim in bundle.get("claims", []):
            self.conn.execute(
                "INSERT OR IGNORE INTO claims VALUES (?, ?)",
                (claim["id"], self._canonical(claim).decode("utf-8")),
            )
        for transform in bundle.get("transforms", []):
            self.conn.execute(
                "INSERT OR IGNORE INTO transforms VALUES (?, ?, ?)",
                (
                    transform["id"],
                    transform["output_claim_id"],
                    self._canonical(transform).decode("utf-8"),
                ),
            )
        self.conn.commit()
        print(
            f"📥 Imported {len(bundle.get('claims', []))} claims, "
            f"{len(bundle.get('transforms', []))} transforms ← {path}"
        )
