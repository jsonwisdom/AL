#!/usr/bin/env python3
"""
ALMS Article I Section 8 full verifier.

Reads all 18 committed clause span files from _truth/us/constitution,
computes UTF-8 byte counts and SHA-256 from repo bytes, and emits JSONL.
No chat-reported hashes are trusted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_REL_PREFIX = Path("_truth/us/constitution")
OUT = ROOT / "constitution_span_audit.jsonl"

TARGETS = [
    (f"USC-A1-S8-C{i}", ROOT / f"a1_s8_c{i}_span.txt")
    for i in range(1, 19)
]


def rel(path: Path) -> str:
    return str(REPO_REL_PREFIX / path.name)


def audit_record(identifier: str, path: Path) -> dict:
    if not path.exists():
        return {"id": identifier, "path": rel(path), "status": "MISSING"}
    data = path.read_bytes()
    return {
        "id": identifier,
        "path": rel(path),
        "status": "OK",
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> int:
    records = [audit_record(identifier, path) for identifier, path in TARGETS]
    OUT.write_text("\n".join(json.dumps(r, separators=(",", ":")) for r in records) + "\n", encoding="utf-8")
    for record in records:
        print(json.dumps(record, separators=(",", ":")))
    return 1 if any(r.get("status") != "OK" for r in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
