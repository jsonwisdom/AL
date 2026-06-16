"""Independent receipt verifier for #176.

Constitutional rule:
RECEIPT_VERIFIED or NO_JURISDICTION.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import hashlib
import json

from .ci_receipt import canonical_json


class ReceiptVerifier:
    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.log_path = self.storage_path / "alms_log.jsonl"

    def _iter_receipts(self):
        if not self.log_path.exists():
            return
        with self.log_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if obj.get("type") == "CI_RECEIPT":
                    yield obj

    def verify_receipt_hash(self, receipt_hash: str) -> Dict[str, Any]:
        for entry in self._iter_receipts():
            data = entry["data"]
            recomputed = hashlib.sha256(
                canonical_json(data).encode("utf-8")
            ).hexdigest()

            if entry.get("receipt_hash") != recomputed:
                return {
                    "status": "INVALID",
                    "reason": "receipt hash mismatch in spine",
                }

            if recomputed == receipt_hash:
                return {
                    "status": "RECEIPT_VERIFIED",
                    "receipt_hash": recomputed,
                    "parent_cumulative_root": data["parent_cumulative_root"],
                    "commit_sha": data["commit_sha"],
                    "workflow_sha": data["workflow_sha"],
                }

        return {
            "status": "NO_JURISDICTION",
            "reason": "receipt hash not found",
        }
