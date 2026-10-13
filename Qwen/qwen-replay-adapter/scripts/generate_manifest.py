from __future__ import annotations

import json
from pathlib import Path

from qwen_replay.canonicalize import sha256_file

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
MANIFEST = ROOT / "fixture_manifest.json"


def main() -> None:
    vectors = {}
    for path in sorted(FIXTURES.glob("qv_*.json")):
        vector_id = path.stem.split("_")[0].upper() + "_" + path.stem.split("_")[1]
        vectors[vector_id] = {"file": path.name, "sha256": sha256_file(str(path))}
    manifest = {
        "suite": "JSONWISDOM_QWEN_REPLAY_V0_1",
        "vectors": vectors,
        "canonicalizer": "PYTHON_JSON_NFC_V0_1",
        "cross_language_jcs": False,
        "generated_at": "2026-08-07T12:00:00Z",
        "status": "HARNESS_READY",
    }
    MANIFEST.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
