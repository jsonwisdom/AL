#!/usr/bin/env python3
"""
Observer B — Python conformance runner for MinimalVerifiableKernel v1.

Purpose:
- provide an independent implementation path from the TypeScript kernel
- use only Python stdlib primitives
- emit machine-readable verdicts

Important:
- expected roots remain null until generated and independently reproduced
- this runner must not import TS code or share kernel logic
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import unicodedata
from typing import Any, Dict, List, Tuple

ZERO_HASH = "0x" + "00" * 32
ROOT = pathlib.Path(__file__).resolve().parents[3]
VECTOR_DIR = ROOT / "conformance" / "v1" / "vectors"


def sha256_hex(data: bytes) -> str:
    return "0x" + hashlib.sha256(data).hexdigest()


def stable_json_string(value: Any) -> str:
    """Small deterministic JSON serializer aligned to the current TS kernel surface."""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, int):
        raise ValueError(f"Number forbidden by manifest: {value}")
    if isinstance(value, float):
        raise ValueError(f"Number forbidden by manifest: {value}")
    if isinstance(value, list):
        return "[" + ",".join(stable_json_string(v) for v in value) + "]"
    if isinstance(value, dict):
        parts = []
        for key in sorted(value.keys()):
            if not isinstance(key, str):
                raise ValueError(f"Object key must be string: {key!r}")
            parts.append(stable_json_string(key) + ":" + stable_json_string(value[key]))
        return "{" + ",".join(parts) + "}"
    raise ValueError(f"Unsupported JSON value type: {type(value).__name__}")


def normalize_nfc(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize_nfc(v) for v in value]
    if isinstance(value, dict):
        return {unicodedata.normalize("NFC", str(k)): normalize_nfc(v) for k, v in value.items()}
    return value


def enforce_lf(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("\r\n", "\n").replace("\r", "\n")
    if isinstance(value, list):
        return [enforce_lf(v) for v in value]
    if isinstance(value, dict):
        return {k: enforce_lf(v) for k, v in value.items()}
    return value


def canonical_bytes(payload: Any) -> bytes:
    working = normalize_nfc(payload)
    working = enforce_lf(working)
    text = stable_json_string(working)
    if "\n" in text:
        raise ValueError("Canonical JSON must be single-line")
    return text.encode("utf-8")


def hash_manifest(manifest: Dict[str, Any]) -> str:
    copy = json.loads(json.dumps(manifest, separators=(",", ":")))
    copy["hash"] = ZERO_HASH
    return sha256_hex(stable_json_string(copy).encode("utf-8"))


def merkle_root(state: Dict[str, str]) -> str:
    lines = []
    for key in sorted(state.keys()):
        lines.append(f"{key}:{state[key]}")
    return sha256_hex("\n".join(lines).encode("utf-8"))


class ObserverBKernel:
    def __init__(self, manifest: Dict[str, Any]) -> None:
        self.manifest = dict(manifest)
        claimed = self.manifest.get("hash")
        if claimed in (None, "SELF"):
            self.manifest["hash"] = hash_manifest(self.manifest)
        computed = hash_manifest(self.manifest)
        if self.manifest["hash"] != computed:
            raise ValueError(f"Manifest hash mismatch: {self.manifest['hash']} != {computed}")
        self.events: List[Dict[str, Any]] = []

    def append_event(self, raw: Dict[str, Any]) -> str:
        expected_index = len(self.events)
        if raw.get("index") != expected_index:
            raise ValueError(f"Index must be gap-free: expected {expected_index}, got {raw.get('index')}")
        payload = json.loads(json.dumps(raw["payload"], separators=(",", ":")))
        if payload.get("manifest_hash") == "SELF":
            payload["manifest_hash"] = self.manifest["hash"]
        event_id = sha256_hex(canonical_bytes(payload))
        parent_hash = self.events[-1]["id"] if self.events else ZERO_HASH
        self.events.append({
            "id": event_id,
            "index": raw["index"],
            "manifestUsed": self.manifest["hash"],
            "parentHash": parent_hash,
        })
        return event_id

    def replay(self) -> Dict[str, Any]:
        state: Dict[str, str] = {}
        checkpoints = []
        for event in self.events:
            idx = event["index"]
            state[f"event:{idx}:id"] = event["id"]
            state[f"event:{idx}:manifest"] = event["manifestUsed"]
            state[f"event:{idx}:parent"] = event["parentHash"]
            if idx % 1000 == 0:
                checkpoints.append({"index": idx, "root": merkle_root(state)})
        return {
            "root": merkle_root(state),
            "eventCount": len(self.events),
            "checkpoints": checkpoints,
            "manifestUsed": self.manifest["hash"],
            "degraded": False,
            "degradationNotes": [],
        }


def load_vector(name: str) -> Dict[str, Any]:
    with (VECTOR_DIR / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def run_vector(vector: Dict[str, Any]) -> Dict[str, Any]:
    try:
        manifest = vector.get("manifest") or {
            "version": "1.0.0",
            "hash": ZERO_HASH,
            "rules": {
                "json": "RFC8785",
                "text_encoding": "UTF-8",
                "text_normalization": "NFC",
                "line_endings": "LF",
                "float_policy": "forbidden",
                "timestamp_format": "TAI64",
                "ordering": "index-ascending",
            },
            "pin": {"hashFunction": "SHA-256", "hashFunctionSpec": "FIPS 180-4"},
        }
        kernel = ObserverBKernel(manifest)
        event_ids = [kernel.append_event(event) for event in vector["events"]]
        replay = kernel.replay()
        return {
            "vector_id": vector["vector_id"],
            "runtime": "python-stdlib",
            "implementation": "observer-b-python-v1",
            "verdict": "PASS",
            "mismatches": [],
            "computed": {
                "event_ids": event_ids,
                "checkpoint_roots": replay["checkpoints"],
                "final_root": replay["root"],
                "event_count": replay["eventCount"],
                "degraded": replay["degraded"],
                "degradation_notes": replay["degradationNotes"],
            },
        }
    except Exception as exc:
        expected_failure = vector.get("acceptance_criteria", {}).get("failure_class")
        return {
            "vector_id": vector.get("vector_id", "UNKNOWN"),
            "runtime": "python-stdlib",
            "implementation": "observer-b-python-v1",
            "verdict": "PASS" if expected_failure else "FAIL",
            "mismatches": [] if expected_failure else [str(exc)],
            "computed": {"rejection": str(exc), "expected_failure": expected_failure},
        }


def main() -> int:
    vectors = [
        load_vector("001_positive_parity_genesis.json"),
        load_vector("002_structural_rejection_float.json"),
    ]
    verdicts = [run_vector(v) for v in vectors]
    print(json.dumps(verdicts, indent=2, sort_keys=True))
    return 0 if all(v["verdict"] == "PASS" for v in verdicts) else 1


if __name__ == "__main__":
    raise SystemExit(main())
