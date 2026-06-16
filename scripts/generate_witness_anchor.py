#!/usr/bin/env python3
"""Generate the Replay Court Genesis witness anchor manifest.

v0 rules:
- hash protected core files and telemetry heads
- sort records by file_path ascending
- canonicalize JSON with sorted keys and compact separators
- witness_root = sha256(canonical records bytes)
- write anchors/genesis/anchor-manifest.json

No signing. No x402. No settlement activation.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = "jsonwisdom/AL"
SCHEMA_VERSION = "0.1.0"
ANCHOR_ID = "genesis_replay_court_witness_root"
PREVIOUS_WITNESS_ROOT = "GENESIS"
REASON = "Genesis Replay Court witness root"

PROTECTED_CORE_FILES = [
    "GAME_MECHANICS.md",
    "AGENT_PLAYBOOK.md",
    "COMPUTER_WISDOM.md",
    "replay-court/PROCESS.md",
    "replay-court/SELF-AUDIT.md",
    "replay-court/VALIDATOR.md",
    "replay-court/REPAIR-LEDGER.md",
    "replay-court/CONTRADICTION-STORE.md",
    "replay-court/AUTHORITY-BOUNDS.md",
    "replay-court/WITNESS-ANCHOR.md",
    "replay-court/BOOTSTRAP-REPLAY.md",
    "replay-court/SCORE-LEDGER.md",
    "replay-court/CONSTITUTIONAL-MAP.md",
    "replay-court/REPORT-TEMPLATE.md",
    "replay-court/receipt-schema.json",
]

TELEMETRY_HEADS = [
    "artifacts/public/latest/level1-output.txt",
    "artifacts/public/latest/verifier-current-tip.txt",
    "artifacts/public/latest/oath.json",
    "replay-court/example-report/README.md",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def make_record(file_path: str, category: str) -> dict[str, str]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Required witness file missing: {file_path}")
    return {
        "category": category,
        "file_path": file_path,
        "sha256": sha256_file(path),
    }


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main() -> int:
    repo_commit = run_git(["rev-parse", "HEAD"])

    protected_records = [make_record(p, "protected_core") for p in PROTECTED_CORE_FILES]
    telemetry_records = [make_record(p, "telemetry_head") for p in TELEMETRY_HEADS]

    all_records = sorted(protected_records + telemetry_records, key=lambda r: r["file_path"])
    witness_root = f"sha256:{hashlib.sha256(canonical_bytes(all_records)).hexdigest()}"

    manifest = {
        "anchor_id": ANCHOR_ID,
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repo": REPO,
        "repo_commit": repo_commit,
        "previous_witness_root": PREVIOUS_WITNESS_ROOT,
        "reason": REASON,
        "protected_core_files": sorted(protected_records, key=lambda r: r["file_path"]),
        "telemetry_heads": sorted(telemetry_records, key=lambda r: r["file_path"]),
        "witness_root": witness_root,
    }

    out = Path("anchors/genesis/anchor-manifest.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"witness_root: {witness_root}")
    print(f"repo_commit: {repo_commit}")
    print(f"manifest: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
