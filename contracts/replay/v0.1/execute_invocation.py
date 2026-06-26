#!/usr/bin/env python3
"""
Replay Invocation Execution Handler v0.2

Fail-safe execution bridge for ./verify.sh --invocation <invocation.json>.

v0.2 adds replay_command + replay_args allowlist dispatch while preserving the
v0.1 execution surface for existing invocations.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[3]
REPLAY_BIN = Path("/usr/local/alms/bin/replay-bin")
SIGNATURE_VERIFIER = ROOT / "contracts" / "replay" / "v0.1" / "verify_envelope_signature.py"
ALLOWED_REPLAY_COMMANDS = {"echo_golden", "check_policy"}


class ReplayRefused(Exception):
    pass


class ReplayQuarantined(Exception):
    pass


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_json_without_invocation_id(invocation: Dict[str, Any]) -> bytes:
    clone = dict(invocation)
    clone.pop("invocation_id", None)
    return json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verify_invocation_id(invocation: Dict[str, Any]) -> None:
    expected = sha256_bytes(canonical_json_without_invocation_id(invocation))
    if invocation.get("invocation_id") != expected:
        raise ReplayRefused("INVOCATION_ID_MISMATCH")


def expected_stdout_hash(invocation: Dict[str, Any]) -> str:
    expected = invocation.get("expected_outputs")
    if not isinstance(expected, dict):
        raise ReplayQuarantined("MISSING_EXPECTED_OUTPUT_HASH")
    stdout_sha256 = expected.get("stdout_sha256")
    if not isinstance(stdout_sha256, str) or not stdout_sha256.startswith("sha256:"):
        raise ReplayQuarantined("MISSING_EXPECTED_OUTPUT_HASH")
    return stdout_sha256


def verify_envelope_reference(invocation: Dict[str, Any]) -> Path:
    envelope_ref = invocation.get("envelope_ref")
    envelope_sha256 = invocation.get("envelope_sha256")
    if not isinstance(envelope_ref, str) or not isinstance(envelope_sha256, str):
        raise ReplayRefused("ENVELOPE_REFERENCE_INVALID")

    envelope_path = ROOT / envelope_ref
    if not envelope_path.exists():
        raise ReplayRefused("ENVELOPE_NOT_FOUND")

    actual = sha256_bytes(envelope_path.read_bytes())
    if actual != envelope_sha256:
        raise ReplayRefused("ENVELOPE_SHA256_MISMATCH")

    return envelope_path


def verify_signature(envelope_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SIGNATURE_VERIFIER), str(envelope_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise ReplayRefused("SIGNATURE_INVALID")


def normalize_output_bytes(data: bytes) -> bytes:
    if data.endswith(b"\n"):
        data = data[:-1]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return unicodedata.normalize("NFC", text).encode("utf-8")


def sealed_env(invocation_id: str) -> Dict[str, str]:
    return {
        "PATH": "/usr/local/alms/bin:/usr/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONHASHSEED": "0",
        "ALMS_INVOCATION_ID": invocation_id,
    }


def replay_argv(invocation: Dict[str, Any]) -> List[str]:
    schema_version = invocation.get("schema_version")

    if schema_version == "invocation-v0.1":
        return [str(REPLAY_BIN)]

    command = invocation.get("replay_command")
    if command not in ALLOWED_REPLAY_COMMANDS:
        raise ReplayQuarantined("COMMAND_NOT_ALLOWED")

    args = invocation.get("replay_args", [])
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        raise ReplayQuarantined("REPLAY_ARGS_INVALID")

    return [str(REPLAY_BIN), command, *args]


def execute(invocation_path: Path) -> Dict[str, Any]:
    invocation = load_json(invocation_path)
    invocation_id = invocation.get("invocation_id")
    witness = invocation.get("witness", {}).get("target")
    command = invocation.get("replay_command") if invocation.get("schema_version") == "invocation-v0.2" else "default_v0.1"

    verify_invocation_id(invocation)
    expected_sha256 = expected_stdout_hash(invocation)
    envelope_path = verify_envelope_reference(invocation)
    verify_signature(envelope_path)

    if not REPLAY_BIN.exists():
        raise ReplayQuarantined("REPLAY_BIN_MISSING")

    result = subprocess.run(
        replay_argv(invocation),
        input=invocation_path.read_bytes(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=sealed_env(invocation_id),
    )

    if result.returncode != 0:
        raise ReplayQuarantined("NONZERO_EXIT")

    if result.stderr:
        raise ReplayQuarantined("STDERR_NOT_EMPTY")

    actual_sha256 = sha256_bytes(normalize_output_bytes(result.stdout))
    state = "REPLAY_CONVERGED" if actual_sha256 == expected_sha256 else "REPLAY_DIVERGED"

    return {
        "verdict_version": "replay-verdict-v0.1",
        "invocation_id": invocation_id,
        "envelope_sha256": invocation.get("envelope_sha256"),
        "witness": witness,
        "replay_command": command,
        "state": state,
        "actual_sha256": actual_sha256,
        "expected_sha256": expected_sha256,
        "actual_stdout_sha256": actual_sha256,
        "expected_stdout_sha256": expected_sha256,
        "reason": "OUTPUT_HASH_MATCH" if state == "REPLAY_CONVERGED" else "OUTPUT_HASH_MISMATCH",
    }


def verdict_from_failure(invocation_path: Path, state: str, reason: str) -> Dict[str, Any]:
    try:
        invocation = load_json(invocation_path)
    except Exception:
        invocation = {}
    expected = (invocation.get("expected_outputs") or {}).get("stdout_sha256")
    command = invocation.get("replay_command") if invocation.get("schema_version") == "invocation-v0.2" else None
    return {
        "verdict_version": "replay-verdict-v0.1",
        "invocation_id": invocation.get("invocation_id"),
        "envelope_sha256": invocation.get("envelope_sha256"),
        "witness": (invocation.get("witness") or {}).get("target"),
        "replay_command": command,
        "state": state,
        "actual_sha256": None,
        "expected_sha256": expected,
        "actual_stdout_sha256": None,
        "expected_stdout_sha256": expected,
        "reason": reason,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"state": "REPLAY_REFUSED", "reason": "USAGE"}, sort_keys=True))
        return 2

    invocation_path = Path(sys.argv[1])
    try:
        verdict = execute(invocation_path)
        print(json.dumps(verdict, sort_keys=True, separators=(",", ":")))
        return 0 if verdict["state"] == "REPLAY_CONVERGED" else 1
    except ReplayRefused as exc:
        print(json.dumps(verdict_from_failure(invocation_path, "REPLAY_REFUSED", str(exc)), sort_keys=True, separators=(",", ":")))
        return 1
    except ReplayQuarantined as exc:
        print(json.dumps(verdict_from_failure(invocation_path, "REPLAY_QUARANTINED", str(exc)), sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
