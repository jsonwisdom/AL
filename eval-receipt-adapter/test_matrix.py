#!/usr/bin/env python3
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

ROOTS_PATH = Path("examples/expected_root.json")
FIXTURE_DIR = Path("examples/fixtures")


def normalize(value):
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, dict):
        return {k: normalize(value[k]) for k in sorted(value.keys())}
    return value


def canonical_json(value):
    return json.dumps(
        normalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    if not ROOTS_PATH.exists():
        print(f"REPLAY_DIVERGED: missing expected roots -> {ROOTS_PATH}")
        sys.exit(1)

    roots = json.loads(ROOTS_PATH.read_text())
    if not roots:
        print("REPLAY_DIVERGED: expected root registry empty")
        sys.exit(1)

    for fixture_id, entry in sorted(roots.items()):
        fixture_path = FIXTURE_DIR / f"{fixture_id.lower()}.json"
        if "fixture_path" in entry:
            fixture_path = Path(entry["fixture_path"])

        if not fixture_path.exists():
            print(f"REPLAY_DIVERGED: missing fixture -> {fixture_path}")
            sys.exit(1)

        payload = json.loads(fixture_path.read_text())
        actual_root = sha256_hex(canonical_json(payload))
        expected_root = entry["expected_root"]

        if actual_root != expected_root:
            print(f"REPLAY_DIVERGED: {fixture_id}")
            print(f"expected: {expected_root}")
            print(f"actual:   {actual_root}")
            sys.exit(1)

        print(f"{fixture_id}: MATCHED {actual_root}")

    print("REPLAY_CONFIRMED")


if __name__ == "__main__":
    main()
