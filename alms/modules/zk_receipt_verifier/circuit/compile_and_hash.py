#!/usr/bin/env python3
"""
compile_and_hash.py — deterministic Noir compile + manifest pinning helper.

This script runs from alms/modules/zk_receipt_verifier/circuit/ and updates
../MODULE.json with reproducible artifact hashes when artifacts exist.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
from datetime import datetime, timezone
from typing import Iterable

ROOT = pathlib.Path(__file__).resolve().parent
TARGET = ROOT / "target"
MODULE_JSON = ROOT.parent / "MODULE.json"


class CompileError(RuntimeError):
    pass



def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()



def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()



def canonical_json_hash(obj) -> str:
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(canonical)



def run(cmd: list[str], allow_missing: bool = False) -> str:
    try:
        completed = subprocess.run(
            cmd,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return (completed.stdout or completed.stderr).strip()
    except FileNotFoundError:
        if allow_missing:
            return "missing"
        raise CompileError(f"command not found: {cmd[0]}")
    except subprocess.CalledProcessError as exc:
        raise CompileError(
            f"command failed: {' '.join(cmd)}\nSTDOUT:\n{exc.stdout}\nSTDERR:\n{exc.stderr}"
        ) from exc



def first_existing(candidates: Iterable[pathlib.Path]) -> pathlib.Path | None:
    for path in candidates:
        if path.exists() and path.is_file():
            return path
    return None



def discover_acir_json() -> pathlib.Path:
    if not TARGET.exists():
        raise CompileError("target/ does not exist after compilation")

    json_files = sorted(TARGET.glob("*.json"))
    if not json_files:
        raise CompileError("no ACIR JSON artifacts found in target/")

    preferred = first_existing([
        TARGET / "zk_receipt_verifier.json",
        TARGET / "main.json",
        TARGET / "circuit.json",
    ])
    return preferred or json_files[0]



def discover_key_file(kind: str) -> pathlib.Path | None:
    patterns = {
        "verification": [
            "verification_key",
            "verification_key.bin",
            "vk",
            "vk.bin",
            "*.vk",
            "*verification*key*",
        ],
        "proving": [
            "proving_key",
            "proving_key.bin",
            "pk",
            "pk.bin",
            "*.pk",
            "*proving*key*",
        ],
    }[kind]

    for pattern in patterns:
        matches = sorted(TARGET.glob(pattern))
        for match in matches:
            if match.exists() and match.is_file():
                return match
    return None



def main() -> int:
    print("Compiling Noir circuit...")
    print(run(["nargo", "compile"]))

    noir_version = run(["nargo", "--version"], allow_missing=True)
    backend_version = run(["bb", "--version"], allow_missing=True)

    acir_file = discover_acir_json()
    with acir_file.open("r", encoding="utf-8") as f:
        acir_json = json.load(f)

    circuit_hash = canonical_json_hash(acir_json)

    verification_key = discover_key_file("verification")
    proving_key = discover_key_file("proving")

    verification_key_hash = sha256_file(verification_key) if verification_key else "sha256:missing"
    proving_key_hash = sha256_file(proving_key) if proving_key else "sha256:missing"

    manifest = json.loads(MODULE_JSON.read_text(encoding="utf-8"))

    manifest["status"] = "CIRCUIT_COMPILED"
    manifest["compiled_at"] = datetime.now(timezone.utc).isoformat()
    manifest["circuit_artifact"] = str(acir_file.relative_to(ROOT))
    manifest["circuit_hash"] = circuit_hash
    manifest["verification_key_artifact"] = str(verification_key.relative_to(ROOT)) if verification_key else "missing"
    manifest["verification_key_hash"] = verification_key_hash
    manifest["proving_key_artifact"] = str(proving_key.relative_to(ROOT)) if proving_key else "missing"
    manifest["proving_key_hash"] = proving_key_hash
    manifest["noir_version"] = noir_version
    manifest["backend_version"] = backend_version

    receipt_basis = {
        "module_id": manifest.get("module_id"),
        "circuit_hash": circuit_hash,
        "verification_key_hash": verification_key_hash,
        "proving_key_hash": proving_key_hash,
        "noir_version": noir_version,
        "backend_version": backend_version,
    }
    manifest["build_receipt_hash"] = canonical_json_hash(receipt_basis)

    MODULE_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "COMPILED",
        "circuit_artifact": manifest["circuit_artifact"],
        "circuit_hash": circuit_hash,
        "verification_key_artifact": manifest["verification_key_artifact"],
        "verification_key_hash": verification_key_hash,
        "proving_key_artifact": manifest["proving_key_artifact"],
        "proving_key_hash": proving_key_hash,
        "noir_version": noir_version,
        "backend_version": backend_version,
        "build_receipt_hash": manifest["build_receipt_hash"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
