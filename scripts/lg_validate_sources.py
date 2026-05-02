#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "law/ingest/law_sources.json"

def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    data = json.loads(REGISTRY.read_text())
    errors = []

    for src in data.get("sources", []):
        sid = src.get("id", "<missing>")
        canon = src.get("normalization", {}).get("canonicalization", {})
        spec = canon.get("spec")
        expected = canon.get("spec_hash")

        if not spec:
            errors.append(f"{sid}: missing canonicalization.spec")
            continue

        spec_path = ROOT / spec
        if not spec_path.exists():
            errors.append(f"{sid}: missing spec file {spec}")
            continue

        actual = "sha256:" + sha256_file(spec_path)

        if not expected:
            print(f"TO_FIX {sid}: spec_hash should be {actual}")
            errors.append(f"{sid}: missing canonicalization.spec_hash")
            continue

        if actual != expected:
            print(f"TO_FIX {sid}: spec_hash should be {actual}")
            errors.append(f"{sid}: spec_hash mismatch expected={expected} actual={actual}")

    if errors:
        print("LG_SOURCE_REGISTRY_INVALID")
        for e in errors:
            print("FAIL:", e)
        return 1

    print("LG_SOURCE_REGISTRY_VALID")
    return 0

if __name__ == "__main__":
    sys.exit(main())
