#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import sys

EPOCH_ID = "IL_COOK_CHICAGO_V0.1"

PATHS = {
    "baseline": "seeds/illinois/downstate-baseline-v0.1.json",
    "cook": "seeds/illinois/cook-delta-a-v0.1.json",
    "chicago": "seeds/illinois/chicago-delta-b-v0.1.json",
    "sovereignty_model": "core/overlays/MUNICIPAL_SOVEREIGNTY_CONFLICT_MODEL_V1.json",
    "effective_view": "views/illinois/chicago-effective-v0.1.json",
    "conflict_ledger": "logs/chicago_conflict_ledger_v0.1.jsonl"
}

SCRIPTS = [
    "scripts/validate_cook_delta_a.py",
    "scripts/validate_chicago_delta_b.py",
    "scripts/resolve_chicago_conflicts.py",
    "scripts/verify_chicago_replay.py"
]

MANIFEST_PATH = "attestation/governance_epoch_v0.1.json"
ROOT_PATH = "attestation/governance_epoch_root_v0.1.json"


def fail(code):
    print(f"ATTEST_GOVERNANCE_EPOCH_FAILED:{code}")
    sys.exit(1)


def run_script(path):
    result = subprocess.run([sys.executable, path], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"SCRIPT_FAILED:{path}")


def sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        fail(f"HASH_FAILED:{path}")


def h_concat(left, right):
    return hashlib.sha256((left + right).encode("utf-8")).hexdigest()


def compute_merkle_root(hashes):
    l1 = h_concat(hashes["baseline_sha256"], hashes["cook_sha256"])
    l2 = h_concat(hashes["chicago_sha256"], hashes["sovereignty_model_sha256"])
    l3 = h_concat(hashes["effective_view_sha256"], hashes["conflict_ledger_sha256"])
    i1 = h_concat(l1, l2)
    return h_concat(i1, l3)


def main():
    for script in SCRIPTS:
        run_script(script)

    hashes = {
        "baseline_sha256": sha256_file(PATHS["baseline"]),
        "cook_sha256": sha256_file(PATHS["cook"]),
        "chicago_sha256": sha256_file(PATHS["chicago"]),
        "sovereignty_model_sha256": sha256_file(PATHS["sovereignty_model"]),
        "effective_view_sha256": sha256_file(PATHS["effective_view"]),
        "conflict_ledger_sha256": sha256_file(PATHS["conflict_ledger"])
    }

    root = compute_merkle_root(hashes)

    manifest = {
        "epoch_id": EPOCH_ID,
        "inputs": {
            "baseline_path": PATHS["baseline"],
            "cook_overlay_path": PATHS["cook"],
            "chicago_overlay_path": PATHS["chicago"],
            "sovereignty_model_path": PATHS["sovereignty_model"]
        },
        "outputs": {
            "effective_view_path": PATHS["effective_view"],
            "conflict_ledger_path": PATHS["conflict_ledger"]
        },
        "hashes": hashes,
        "replay_verification": {
            "verify_script": "scripts/verify_chicago_replay.py",
            "verify_version": "v0.1",
            "verify_status": "VERIFY_CHICAGO_REPLAY_SUCCESS"
        }
    }

    root_doc = {
        "epoch_id": EPOCH_ID,
        "merkle_root_sha256": root,
        "leaf_hashes": hashes
    }

    os.makedirs("attestation", exist_ok=True)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(ROOT_PATH, "w", encoding="utf-8") as f:
        json.dump(root_doc, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"ATTEST_GOVERNANCE_EPOCH_SUCCESS:{EPOCH_ID}:{root}")
    sys.exit(0)


if __name__ == "__main__":
    main()
