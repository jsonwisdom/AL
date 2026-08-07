from __future__ import annotations

import json
from pathlib import Path

from qwen_replay.canonicalize import sha256_file

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
MANIFEST = ROOT / "fixture_manifest.json"


def fail(code: str) -> None:
    raise SystemExit(code)


def main() -> None:
    if not MANIFEST.exists():
        fail("MANIFEST_MISSING")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    declared = manifest.get("vectors", {})
    actual_files = {p.name for p in FIXTURES.glob("qv_*.json")}
    declared_files = {v["file"] for v in declared.values()}
    if actual_files - declared_files:
        fail("UNDECLARED_FIXTURE")
    if declared_files - actual_files:
        fail("FIXTURE_MISSING")
    for item in declared.values():
        path = FIXTURES / item["file"]
        if sha256_file(str(path)) != item["sha256"]:
            fail("HASH_MISMATCH")
    print("MANIFEST_VERIFIED")


if __name__ == "__main__":
    main()
