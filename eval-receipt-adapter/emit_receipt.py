#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import yaml


def compute_sha256(path: str) -> str:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(path)

    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def main():
    parser = argparse.ArgumentParser(description="Replay CI receipt emitter")
    parser.add_argument("--config", default="adapter.config.yaml")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"REPLAY_DIVERGED: missing config -> {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    timestamp = int(time.time())

    system = config["system"]
    targets = config["pipeline_targets"]
    storage = config["storage"]

    try:
        dataset_hash = compute_sha256(targets["dataset_source"])
        prompt_hash = compute_sha256(targets["prompt_template"])
        output_hash = compute_sha256(targets["model_output"])
    except FileNotFoundError as e:
        print(f"REPLAY_DIVERGED: missing artifact -> {e}")
        sys.exit(1)

    state_payload = {
        "dataset_sha256": dataset_hash,
        "prompt_template_sha256": prompt_hash,
        "model_output_sha256": output_hash,
        "system_version": system["version"],
    }

    execution_hash = hashlib.sha256(
        canonical_json(state_payload).encode("utf-8")
    ).hexdigest()

    receipt = {
        "schema_version": "1.1.0",
        "receipt_id": f"rcpt_{timestamp}",
        "timestamp": timestamp,
        "identity": {
            "operator": system["operator"],
            "environment": system["environment"],
            "system_version": system["version"],
        },
        "provenance": state_payload,
        "execution_hash": execution_hash,
        "verification_decay_risk": "LOW",
        "reproducibility_scope": "input_surface",
    }

    receipt_hash = hashlib.sha256(
        canonical_json(receipt).encode("utf-8")
    ).hexdigest()

    receipt["receipt_hash"] = receipt_hash

    vault = Path(storage["l0_local_vault"])
    vault.mkdir(parents=True, exist_ok=True)

    output_path = vault / "eval-receipt.json"

    with open(output_path, "w") as out:
        json.dump(receipt, out, indent=2, sort_keys=True)
        out.write("\n")

    print(f"REPLAY_CONFIRMED: receipt emitted -> {output_path}")
    print(f"execution_hash={execution_hash}")
    print(f"receipt_hash={receipt_hash}")

    if storage.get("auto_upload_gcs"):
        print("INFO: GCS upload hook configured but not implemented in v1")

    if config.get("attestation", {}).get("auto_attest_base"):
        print("INFO: Base/EAS attestation hook configured but not implemented in v1")


if __name__ == "__main__":
    main()
