#!/usr/bin/env python3
"""Consume sealed ALMS execution receipts into one hash-linked global ledger.

Rules:
- append-only; existing rows are verified before any append;
- idempotent by both receipt_id and receipt final_hash;
- conflicting duplicate identifiers fail closed;
- only valid sealed EXECUTION_RECEIPTs with authority=false are ingestible;
- every ledger entry validates against the locked v0.1 JSON Schema;
- the pending batch is fully validated before any new row is appended;
- no PASS is inferred from silence;
- deterministic compact sorted-key UTF-8 JSON hashing is used;
- RFC 8785 JCS compatibility is not claimed.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from jsonschema import Draft202012Validator, FormatChecker

RECEIPTS_DIR = Path("alms/execution_receipts")
LEDGER_PATH = Path("alms/JSONWISDOM_GLOBAL_EXECUTION_LEDGER.jsonl")
SCHEMA_PATH = Path("schemas/JSONWISDOM_GLOBAL_EXECUTION_LEDGER_V0_1.schema.json")
GENESIS = "genesis"
CANON_METHOD = "JSON_SORTED_KEYS_COMPACT_UTF8_V0_1"
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_json_text(obj: Any) -> str:
    return canonical_json_bytes(obj).decode("utf-8")


def sha256_prefixed(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_object(obj: Any) -> str:
    return sha256_prefixed(canonical_json_bytes(obj))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_schema_validator() -> Draft202012Validator:
    require(SCHEMA_PATH.exists(), f"missing ledger schema: {SCHEMA_PATH}")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_schema(entry: Dict[str, Any], validator: Draft202012Validator, label: str) -> None:
    errors = sorted(validator.iter_errors(entry), key=lambda err: list(err.path))
    if errors:
        rendered = "; ".join(
            f"{'.'.join(map(str, err.path)) or '<root>'}: {err.message}"
            for err in errors
        )
        raise ValueError(f"{label}: schema validation failed: {rendered}")


def verify_receipt(receipt: Dict[str, Any], path: Path) -> None:
    require(receipt.get("receipt_type") == "EXECUTION_RECEIPT", f"{path}: wrong receipt_type")
    require(bool(receipt.get("receipt_id")), f"{path}: missing receipt_id")
    require(receipt.get("authority") is False, f"{path}: authority must be false")
    require(receipt.get("proof_inferred") is False, f"{path}: proof_inferred must be false")
    require(receipt.get("no_fake_green") is True, f"{path}: no_fake_green must be true")

    canonicalization = receipt.get("canonicalization") or {}
    require(
        canonicalization.get("method") == CANON_METHOD,
        f"{path}: unsupported canonicalization method",
    )
    require(
        canonicalization.get("rfc8785_jcs_claimed") is False,
        f"{path}: RFC 8785 JCS must not be claimed by this v0.1 consumer",
    )

    final_hash = receipt.get("final_hash")
    require(
        isinstance(final_hash, str) and SHA256_RE.fullmatch(final_hash),
        f"{path}: invalid final_hash",
    )

    final_view = {k: v for k, v in receipt.items() if k != "final_hash"}
    calculated = sha256_object(final_view)
    require(calculated == final_hash, f"{path}: final_hash mismatch")

    execution = receipt.get("execution")
    require(isinstance(execution, dict), f"{path}: missing execution object")
    require(bool(execution.get("workflow_run_id")), f"{path}: missing workflow_run_id")
    require(bool(execution.get("repo")), f"{path}: missing repo")
    commit = str(execution.get("commit") or "")
    require(COMMIT_RE.fullmatch(commit) is not None, f"{path}: invalid commit SHA")
    require(
        isinstance(execution.get("runner_exit_code"), int),
        f"{path}: runner_exit_code must be int",
    )
    require(
        execution.get("verdict") in {"PASS", "FAIL", "INDETERMINATE", "ERROR"},
        f"{path}: invalid verdict",
    )
    require(
        execution.get("hard_gate_result") in {"PASS", "REJECT", "HOLD"},
        f"{path}: invalid hard_gate_result",
    )
    if execution.get("verdict") == "PASS":
        require(
            execution.get("runner_exit_code") == 0,
            f"{path}: PASS with non-zero exit",
        )
        require(
            execution.get("hard_gate_result") == "PASS",
            f"{path}: PASS verdict without PASS hard gate",
        )


def verify_ledger_entry(
    entry: Dict[str, Any],
    expected_seq: int,
    expected_prev: str,
    validator: Draft202012Validator,
) -> None:
    validate_schema(entry, validator, f"ledger seq {expected_seq}")
    require(
        entry.get("seq") == expected_seq,
        f"ledger: expected seq {expected_seq}",
    )
    require(
        entry.get("prev_tip") == expected_prev,
        f"ledger seq {expected_seq}: prev_tip mismatch",
    )

    entry_hash = entry.get("entry_hash")
    body = {k: v for k, v in entry.items() if k != "entry_hash"}
    require(
        sha256_object(body) == entry_hash,
        f"ledger seq {expected_seq}: entry_hash mismatch",
    )


def load_existing_ledger() -> Tuple[List[Dict[str, Any]], Set[str], Set[str], str]:
    validator = load_schema_validator()

    if not LEDGER_PATH.exists() or LEDGER_PATH.stat().st_size == 0:
        return [], set(), set(), GENESIS

    entries: List[Dict[str, Any]] = []
    seen_ids: Set[str] = set()
    seen_hashes: Set[str] = set()
    tip = GENESIS

    for line_number, raw_line in enumerate(
        LEDGER_PATH.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not raw_line.strip():
            continue
        try:
            entry = json.loads(raw_line)
        except Exception as exc:
            raise ValueError(
                f"ledger line {line_number}: invalid JSON: {exc}"
            ) from exc

        expected_seq = len(entries) + 1
        verify_ledger_entry(entry, expected_seq, tip, validator)

        receipt_id = entry["receipt_id"]
        final_hash = entry["receipt_final_hash"]
        require(
            receipt_id not in seen_ids,
            f"ledger seq {expected_seq}: duplicate receipt_id",
        )
        require(
            final_hash not in seen_hashes,
            f"ledger seq {expected_seq}: duplicate receipt_final_hash",
        )

        entries.append(entry)
        seen_ids.add(receipt_id)
        seen_hashes.add(final_hash)
        tip = entry["entry_hash"]

    return entries, seen_ids, seen_hashes, tip


def load_receipts() -> List[Tuple[Path, Dict[str, Any]]]:
    if not RECEIPTS_DIR.exists():
        return []

    loaded: List[Tuple[Path, Dict[str, Any]]] = []
    for path in sorted(RECEIPTS_DIR.glob("*.json")):
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
            verify_receipt(receipt, path)
            loaded.append((path, receipt))
        except Exception as exc:
            raise ValueError(f"receipt validation failed: {exc}") from exc
    return loaded


def make_entry(
    receipt: Dict[str, Any],
    path: Path,
    seq: int,
    prev_tip: str,
) -> Dict[str, Any]:
    execution = receipt["execution"]
    bindings = receipt.get("bindings") or {}

    body: Dict[str, Any] = {
        "type": "EXECUTION_RECEIPT",
        "ledger_version": "0.1",
        "seq": seq,
        "prev_tip": prev_tip,
        "canonicalization": {
            "method": CANON_METHOD,
            "hash_alg": "sha256",
            "rfc8785_jcs_claimed": False,
        },
        "receipt_id": receipt["receipt_id"],
        "receipt_final_hash": receipt["final_hash"],
        "receipt_path": path.as_posix(),
        "workflow_name": execution.get("workflow_name"),
        "workflow_run_id": str(execution.get("workflow_run_id")),
        "workflow_run_attempt": str(execution.get("workflow_run_attempt")),
        "repo": execution.get("repo"),
        "ref": execution.get("ref"),
        "commit": execution.get("commit"),
        "actor": execution.get("actor"),
        "event_name": execution.get("event_name"),
        "runner_exit_code": execution.get("runner_exit_code"),
        "verdict": execution.get("verdict"),
        "hard_gate_result": execution.get("hard_gate_result"),
        "items_requested": execution.get("items_requested"),
        "items_passed": execution.get("items_passed"),
        "items_failed": execution.get("items_failed"),
        "items_indeterminate": execution.get("items_indeterminate"),
        "alms_version": bindings.get("alms_version"),
        "receiptos_frame": bindings.get("receiptos_frame"),
        "ens_pointer": bindings.get("ens_pointer"),
        "requested_replay_parameter": receipt.get("requested_replay_parameter"),
        "source_hashes": receipt.get("source_hashes") or {},
        "authority": False,
        "proof_inferred": False,
        "no_fake_green": True,
        "ingested_at": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
    }
    body["entry_hash"] = sha256_object(body)
    return body


def main() -> int:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        validator = load_schema_validator()
        existing, seen_ids, seen_hashes, tip = load_existing_ledger()
        receipts = load_receipts()
    except Exception as exc:
        print(f"CONSUME_REJECT {exc}", file=sys.stderr)
        return 1

    id_to_hash = {
        entry["receipt_id"]: entry["receipt_final_hash"]
        for entry in existing
    }
    hash_to_id = {
        entry["receipt_final_hash"]: entry["receipt_id"]
        for entry in existing
    }

    seq = len(existing)
    pending: List[Dict[str, Any]] = []

    # Build and validate the complete candidate batch before mutating the ledger file.
    for path, receipt in receipts:
        receipt_id = receipt["receipt_id"]
        final_hash = receipt["final_hash"]

        if receipt_id in seen_ids:
            if id_to_hash.get(receipt_id) != final_hash:
                print(
                    f"CONFLICT receipt_id={receipt_id} final_hash changed",
                    file=sys.stderr,
                )
                return 1
            continue

        if final_hash in seen_hashes:
            if hash_to_id.get(final_hash) != receipt_id:
                print(
                    f"CONFLICT final_hash={final_hash} reused by another receipt_id",
                    file=sys.stderr,
                )
                return 1
            continue

        seq += 1
        entry = make_entry(receipt, path, seq, tip)
        try:
            validate_schema(entry, validator, f"new ledger seq {seq}")
        except Exception as exc:
            print(f"CONSUME_REJECT {exc}", file=sys.stderr)
            return 1

        pending.append(entry)
        tip = entry["entry_hash"]
        seen_ids.add(receipt_id)
        seen_hashes.add(final_hash)
        id_to_hash[receipt_id] = final_hash
        hash_to_id[final_hash] = receipt_id

    if pending:
        with LEDGER_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            for entry in pending:
                handle.write(canonical_json_text(entry) + "\n")
            handle.flush()

        for entry in pending:
            print(
                f"APPENDED seq={entry['seq']} "
                f"receipt_id={entry['receipt_id']} "
                f"tip={entry['entry_hash']}"
            )

    print(f"DONE new={len(pending)} total_seq={seq} tip={tip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
