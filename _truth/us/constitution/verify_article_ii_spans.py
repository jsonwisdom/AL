#!/usr/bin/env python3
"""
Verify Article II span files currently anchored in the repo.

Outputs JSONL records with id, path, bytes, sha256, status.
Fails if any expected span is missing.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = [
    ("USC-A2-S1-C1", "a2_s1_c1_span.txt"),
    ("USC-A2-S1-C2", "a2_s1_c2_span.txt"),
    ("USC-A2-S1-C3", "a2_s1_c3_span.txt"),
    ("USC-A2-S1-C4", "a2_s1_c4_span.txt"),
    ("USC-A2-S1-C5", "a2_s1_c5_span.txt"),
    ("USC-A2-S1-C6", "a2_s1_c6_span.txt"),
    ("USC-A2-S1-C7", "a2_s1_c7_span.txt"),
    ("USC-A2-S1-C8", "a2_s1_c8_span.txt"),
    ("USC-A2-S2-C1", "a2_s2_c1_span.txt"),
    ("USC-A2-S2-C2", "a2_s2_c2_span.txt"),
    ("USC-A2-S2-C3", "a2_s2_c3_span.txt"),
    ("USC-A2-S3-C1", "a2_s3_c1_span.txt"),
]


def main() -> int:
    ok = True
    for artifact_id, filename in EXPECTED:
        path = ROOT / filename
        if not path.exists():
            print(json.dumps({
                "id": artifact_id,
                "path": str(path.relative_to(ROOT)),
                "status": "MISSING",
            }, sort_keys=True))
            ok = False
            continue
        data = path.read_bytes()
        print(json.dumps({
            "id": artifact_id,
            "path": str(path.relative_to(ROOT)),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "status": "OK",
        }, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
