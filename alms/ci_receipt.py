"""CI receipt primitives for #175/#176.

Constitutional rule:
- Reported results are not constitutional evidence until receipted.
- A CI receipt must extend the canonical cumulative tip.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict
import hashlib
import json
import time


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class CIReceipt:
    """A green gauntlet run as commit-bound constitutional evidence."""

    run_id: str
    commit_sha: str
    workflow_sha: str
    suite: str
    replay_result: Dict[str, Any]
    fuzz_stats: Dict[str, Any]
    artifact_hashes: Dict[str, str]
    timestamp_ns: int
    parent_cumulative_root: str

    def __post_init__(self) -> None:
        if not self.parent_cumulative_root:
            raise ValueError("parent_cumulative_root is required")
        if not self.commit_sha:
            raise ValueError("commit_sha is required")
        if not self.workflow_sha:
            raise ValueError("workflow_sha is required")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def compute_hash(self) -> str:
        return _sha256_text(canonical_json(self.to_dict()))


class CIReceiptManager:
    """Append CI receipts to the canonical ALMS log.

    This class does not activate jurisdiction by itself. Activation still requires
    successful independent verification and, when configured, EAS attestation.
    """

    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.log_path = self.storage_path / "alms_log.jsonl"

    def ensure_genesis(self) -> str:
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            genesis = {
                "type": "GENESIS",
                "root": "genesis",
                "timestamp_ns": time.time_ns(),
            }
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(canonical_json(genesis) + "\n")
            return "genesis"
        return self.current_tip()

    def current_tip(self) -> str:
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            return "genesis"
        last = ""
        with self.log_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last = line.strip()
        if not last:
            return "genesis"
        return hashlib.sha256(last.encode("utf-8")).hexdigest()

    def record(self, receipt: CIReceipt) -> str:
        receipt_hash = receipt.compute_hash()
        entry = {
            "type": "CI_RECEIPT",
            "receipt_hash": receipt_hash,
            "data": receipt.to_dict(),
        }
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(canonical_json(entry) + "\n")
        return receipt_hash
