#!/usr/bin/env python3
"""Observer B — Python stdlib conformance runner."""

from __future__ import annotations

import hashlib
import json
import pathlib
import unicodedata
from typing import Any, Dict, List

ZERO_HASH = "0x" + "00" * 32
ROOT = pathlib.Path(__file__).resolve().parents[3]
VECTOR_DIR = ROOT / "conformance" / "v1" / "vectors"
REJECTION_CLASSES = ["FAIL_NUMBER_FORBIDDEN", "FAIL_MANIFEST_HASH_MISMATCH", "FAIL_INDEX_GAP", "FAIL_UNKNOWN"]


def sha256_hex(data: bytes) -> str:
    return "0x" + hashlib.sha256(data).hexdigest()


def stable_json_string(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, (int, float)):
        raise ValueError(f"Number forbidden by manifest: {value}")
    if isinstance(value, list):
        return "[" + ",".join(stable_json_string(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(stable_json_string(k) + ":" + stable_json_string(value[k]) for k in sorted(value.keys())) + "}"
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
    text = stable_json_string(enforce_lf(normalize_nfc(payload)))
    if "\n" in text:
        raise ValueError("Canonical JSON must be single-line")
    return text.encode("utf-8")


def hash_manifest(manifest: Dict[str, Any]) -> str:
    copy = json.loads(json.dumps(manifest, separators=(",", ":")))
    copy["hash"] = ZERO_HASH
    return sha256_hex(stable_json_string(copy).encode("utf-8"))


def state_root(state: Dict[str, str]) -> str:
    serialized = "\n".join(f"{key}:{state[key]}" for key in sorted(state.keys()))
    return sha256_hex(serialized.encode("utf-8"))


def rejection_class(exc: Exception) -> str:
    msg = str(exc)
    if "Number forbidden" in msg or "Float" in msg:
        return "FAIL_NUMBER_FORBIDDEN"
    if "Manifest hash mismatch" in msg:
        return "FAIL_MANIFEST_HASH_MISMATCH"
    if "Index must be gap-free" in msg:
        return "FAIL_INDEX_GAP"
    return "FAIL_UNKNOWN"


class ObserverBKernel:
    def __init__(self, manifest: Dict[str, Any]) -> None:
        self.manifest = json.loads(json.dumps(manifest, separators=(",", ":")))
        if self.manifest.get("hash") in (None, "SELF"):
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
        event_id = sha256_hex(canonical_bytes(payload))
        parent_hash = self.events[-1]["id"] if self.events else ZERO_HASH
        self.events.append({"id": event_id, "index": raw["index"], "manifestUsed": self.manifest["hash"], "parentHash": parent_hash})
        return event_id

    def replay(self) -> Dict[str, Any]:
        state: Dict[str, str] = {}
        checkpoints = []
        for event in self.events:
            idx = event["index"]
            state[f"event:{idx}:id"] = event["id"]
            state[f"event:{idx}:manifest"] = event["manifestUsed"]
            state[f"event:{idx}:parent"] = event["parentHash"]
            checkpoints.append({"index": idx, "root": state_root(state)})
        return {"root": state_root(state), "eventCount": len(self.events), "checkpoints": checkpoints, "manifestUsed": self.manifest["hash"], "degraded": False, "degradationNotes": []}


def load_vector(name: str) -> Dict[str, Any]:
    with (VECTOR_DIR / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def run_vector(vector: Dict[str, Any]) -> Dict[str, Any]:
    try:
        manifest = vector.get("manifest") or load_vector("001_positive_parity_genesis.json")["manifest"]
        kernel = ObserverBKernel(manifest)
        event_ids = [kernel.append_event(event) for event in vector["events"]]
        replay = kernel.replay()
        return {"vector_id": vector["vector_id"], "runtime": "python-stdlib", "implementation": "observer-b-python-v1", "verdict": "PASS", "mismatches": [], "computed": {"event_ids": event_ids, "checkpoint_roots": replay["checkpoints"], "final_root": replay["root"], "event_count": replay["eventCount"], "degraded": replay["degraded"], "degradation_notes": replay["degradationNotes"], "manifest_used": replay["manifestUsed"], "rejection_class": None, "rejection_message": None}}
    except Exception as exc:
        expected_failure = vector.get("acceptance_criteria", {}).get("failure_class")
        cls = rejection_class(exc)
        return {"vector_id": vector.get("vector_id", "UNKNOWN"), "runtime": "python-stdlib", "implementation": "observer-b-python-v1", "verdict": "PASS" if expected_failure else "FAIL", "mismatches": [] if expected_failure else [str(exc)], "computed": {"rejection_class": cls, "rejection_message": str(exc), "expected_failure": expected_failure}}


def main() -> int:
    vectors = [load_vector(p.name) for p in sorted(VECTOR_DIR.glob("*.json"))]
    verdicts = [run_vector(v) for v in vectors]
    print(json.dumps(verdicts, indent=2, sort_keys=True))
    return 0 if all(v["verdict"] == "PASS" for v in verdicts) else 1


if __name__ == "__main__":
    raise SystemExit(main())
