#!/usr/bin/env python3
"""
ALMS Constitution span verifier.

Repo-bound verification only:
- Reads committed span files from _truth/us/constitution/
- Computes UTF-8 byte count and SHA-256 from repository bytes
- Emits JSONL proof records suitable for Merkle inclusion

No chat-reported hashes are trusted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "constitution_span_audit.jsonl"

TARGETS = [
    ("USC-A1-S8-C1", ROOT / "a1_s8_c1_span.txt"),
    ("USC-A1-S8-C2", ROOT / "a1_s8_c2_span.txt"),
    ("USC-A1-S8-C3", ROOT / "a1_s8_c3_span.txt"),
    ("USC-A1-S8-C14", ROOT / "a1_s8_c14_span.txt"),
    ("USC-A1-S8-C15", ROOT / "a1_s8_c15_span.txt"),
    ("USC-A1-S8-C16", ROOT / "a1_s8_c16_span.txt"),
    ("USC-A1-S8-C17", ROOT / "a1_s8_c17_span.txt"),
    ("USC-A1-S8-C18", ROOT / "a1_s8_c18_span.txt"),
]


def audit_record(identifier: str, path: Path) -> dict:
    if not path.exists():
        return {
            "id": identifier,
            "path": str(path.relative_to(ROOT.parent.parent.parent)),
            "status": "MISSING",
        }
    data = path.read_bytes()
    return {
        "id": identifier,
        "path": str(path.relative_to(ROOT.parent.parent.parent)),
        "status": "OK",
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> int:
    records = [audit_record(identifier, path) for identifier, path in TARGETS]
    OUT.write_text("\n".join(json.dumps(r, separators=(",", ":")) for r in records) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT.parent.parent.parent))
    for record in records:
        print(json.dumps(record, separators=(",", ":")))
    return 1 if any(r.get("status") != "OK" for r in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
