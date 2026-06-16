#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import sys
import tempfile

BASELINE_PATH = "seeds/illinois/downstate-baseline-v0.1.json"
COOK_PATH = "seeds/illinois/cook-delta-a-v0.1.json"
CHICAGO_PATH = "seeds/illinois/chicago-delta-b-v0.1.json"
MODEL_PATH = "core/overlays/MUNICIPAL_SOVEREIGNTY_CONFLICT_MODEL_V1.json"
RECORDED_VIEW_PATH = "views/illinois/chicago-effective-v0.1.json"
RECORDED_LEDGER_PATH = "logs/chicago_conflict_ledger_v0.1.jsonl"
COOK_VALIDATOR = "scripts/validate_cook_delta_a.py"
CHICAGO_VALIDATOR = "scripts/validate_chicago_delta_b.py"
RESOLVER = "scripts/resolve_chicago_conflicts.py"


def fail(code):
    print(f"VERIFY_CHICAGO_REPLAY_FAILED:{code}")
    sys.exit(1)


def read_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        fail("MISSING_REQUIRED_ARTIFACT")
    except Exception:
        fail("INVALID_INPUT_JSON")


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        fail("MISSING_REQUIRED_ARTIFACT")
    except Exception:
        fail("INVALID_INPUT_JSON")


def load_jsonl(path):
    try:
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows
    except FileNotFoundError:
        fail("MISSING_REQUIRED_ARTIFACT")
    except Exception:
        fail("INVALID_INPUT_JSON")


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_json_hash(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256_bytes(raw)


def run_required(cmd, code):
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except Exception:
        fail(code)
    if result.returncode != 0:
        fail(code)
    return result


def compare_ledgers(a, b):
    if len(a) != len(b):
        fail("LEDGER_CONFLICT_SET_MISMATCH")
    sort_key = lambda x: (
        str(x.get("node_id")),
        str(x.get("key_path")),
        str(x.get("conflict_type")),
        str(x.get("resolution_rule")),
        str(x.get("winner")),
    )
    if sorted(a, key=sort_key) != sorted(b, key=sort_key):
        fail("LEDGER_RESOLUTION_MISMATCH")


def main():
    # LOAD_AND_HASH_INPUTS
    for path in [BASELINE_PATH, COOK_PATH, CHICAGO_PATH, MODEL_PATH]:
        load_json(path)
        sha256_bytes(read_bytes(path))

    recorded_view = load_json(RECORDED_VIEW_PATH)
    recorded_ledger = load_jsonl(RECORDED_LEDGER_PATH)

    # REBUILD_EFFECTIVE_VIEWS preconditions
    run_required([sys.executable, COOK_VALIDATOR], "COOK_NOT_VALIDATED")
    run_required([sys.executable, CHICAGO_VALIDATOR], "CHICAGO_NOT_VALIDATED")

    # Run resolver in a temp copy so recorded artifacts are not modified.
    with tempfile.TemporaryDirectory() as td:
        run_required(["cp", "-R", ".", td], "EFFECTIVE_VIEW_REBUILD_ERROR")
        result = subprocess.run(
            [sys.executable, RESOLVER],
            cwd=td,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            fail("SOVEREIGNTY_MODEL_DIVERGENCE_ON_REPLAY")

        replay_view_path = os.path.join(td, RECORDED_VIEW_PATH)
        replay_ledger_path = os.path.join(td, RECORDED_LEDGER_PATH)

        replay_view = load_json(replay_view_path)
        replay_ledger = load_jsonl(replay_ledger_path)

    # REPLAY_CONFLICT_ENUMERATION + REPLAY_RESOLUTION_AND_LEDGER
    compare_ledgers(recorded_ledger, replay_ledger)

    # COMPARE_E_CH
    if canonical_json_hash(recorded_view) != canonical_json_hash(replay_view):
        fail("E_CH_HASH_MISMATCH")

    print("VERIFY_CHICAGO_REPLAY_SUCCESS")
    sys.exit(0)


if __name__ == "__main__":
    main()
