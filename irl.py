#!/usr/bin/env python3
"""Intel Receipts Ledger CLI.

Thin command wrapper for verifying ledger claim files.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft7Validator
except Exception:  # pragma: no cover
    Draft7Validator = None


EVIDENCE_TYPES = {
    "primary_document",
    "leaked_document",
    "on_record_statement",
    "anonymous_report",
    "news_report",
}
TERMINAL_STATES = {"CONFIRMED", "CONTRADICTED", "WITHDRAWN", "TIMEOUT"}
VALID_STATUSES = {"OPEN", *TERMINAL_STATES}


class GateError(Exception):
    def __init__(self, gate: str, message: str):
        super().__init__(message)
        self.gate = gate
        self.message = message


def _walk_forbidden_confidence(obj: Any, path: str = "$") -> None:
    if isinstance(obj, dict):
        if "confidence" in obj:
            raise GateError("business_logic_gate", f"confidence field is forbidden at {path}.confidence")
        for key, value in obj.items():
            _walk_forbidden_confidence(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            _walk_forbidden_confidence(value, f"{path}[{i}]")


def parse_json_gate(path: Path) -> dict:
    try:
        entry = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GateError("parse_json_gate", f"invalid JSON: {exc}") from exc
    if not isinstance(entry, dict):
        raise GateError("parse_json_gate", "top-level JSON must be an object")
    return entry


def schema_gate(entry: dict, schema_path: Path) -> None:
    if Draft7Validator is None:
        raise GateError("schema_gate", "jsonschema is not installed")
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GateError("schema_gate", f"invalid schema JSON: {exc}") from exc
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(entry), key=lambda e: list(e.path))
    if errors:
        err = errors[0]
        loc = "/".join(str(p) for p in err.path) or "$"
        raise GateError("schema_gate", f"{loc}: {err.message}")


def _validate_receipt(receipt: dict) -> None:
    rtype = receipt.get("type")
    supports = receipt.get("supports_claim")
    contradicts = receipt.get("contradicts_claim")

    if rtype == "timeout_policy":
        if supports is not False or contradicts is not False:
            raise GateError("business_logic_gate", "timeout_policy must have supports_claim=false and contradicts_claim=false")
        return

    if rtype == "retraction":
        if supports is not False:
            raise GateError("business_logic_gate", "retraction cannot support a claim")
        if contradicts not in (False, True):
            raise GateError("business_logic_gate", "retraction contradicts_claim must be boolean")
        return

    if rtype in EVIDENCE_TYPES:
        if supports == contradicts:
            raise GateError("business_logic_gate", f"{rtype} requires exactly one of supports_claim or contradicts_claim")
        return

    raise GateError("business_logic_gate", f"unknown receipt type: {rtype}")


def _expected_transition(receipt: dict) -> str | None:
    rtype = receipt.get("type")
    if rtype in {"primary_document", "leaked_document", "on_record_statement"}:
        if receipt.get("supports_claim") is True:
            return "CONFIRMED"
        if receipt.get("contradicts_claim") is True:
            return "CONTRADICTED"
    if rtype == "retraction":
        return "WITHDRAWN"
    if rtype == "timeout_policy":
        return "TIMEOUT"
    return None


def business_logic_gate(entry: dict) -> None:
    _walk_forbidden_confidence(entry)

    status = entry.get("status")
    if status not in VALID_STATUSES:
        raise GateError("business_logic_gate", f"invalid status: {status}")

    receipts = entry.get("receipts", [])
    if not isinstance(receipts, list):
        raise GateError("business_logic_gate", "receipts must be an array")

    receipt_ids = set()
    by_id = {}
    for receipt in receipts:
        _validate_receipt(receipt)
        rid = receipt.get("receipt_id")
        if rid:
            if rid in receipt_ids:
                raise GateError("business_logic_gate", f"duplicate receipt_id: {rid}")
            receipt_ids.add(rid)
            by_id[rid] = receipt

    history = entry.get("history", [])
    if history is None:
        history = []
    if not isinstance(history, list):
        raise GateError("business_logic_gate", "history must be an array")

    last_to = "OPEN"
    for h in history:
        rid = h.get("receipt_id")
        if rid not in by_id:
            raise GateError("business_logic_gate", f"history receipt_id not found in receipts: {rid}")
        frm = h.get("from")
        to = h.get("to")
        if frm != last_to:
            raise GateError("business_logic_gate", f"history transition from {frm} does not match prior state {last_to}")
        if frm in TERMINAL_STATES:
            raise GateError("business_logic_gate", f"terminal state cannot transition: {frm}")
        expected = _expected_transition(by_id[rid])
        if expected is not None and to != expected:
            raise GateError("business_logic_gate", f"receipt {rid} requires transition to {expected}, got {to}")
        last_to = to

    if history:
        if status != history[-1].get("to"):
            raise GateError("business_logic_gate", "status must equal last history transition target")
        if entry.get("last_transition_at") != history[-1].get("at"):
            raise GateError("business_logic_gate", "last_transition_at must equal latest history.at")


def verify_claim_file(path: Path, schema_path: Path) -> dict:
    entry = parse_json_gate(path)
    schema_gate(entry, schema_path)
    business_logic_gate(entry)
    return entry


def verify_ledger_dir(ledger_dir: Path, schema_path: Path) -> dict:
    files = sorted(ledger_dir.glob("*.json"))
    results = {}
    for path in files:
        try:
            entry = verify_claim_file(path, schema_path)
            results[str(path)] = {"ok": True, "status": entry.get("status")}
        except GateError as exc:
            results[str(path)] = {"ok": False, "gate": exc.gate, "error": exc.message}
    return results


def _print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="irl")
    sub = parser.add_subparsers(dest="command", required=True)

    vc = sub.add_parser("verify-claim")
    vc.add_argument("path")
    vc.add_argument("--schema", default="ledger_schema.json")

    vl = sub.add_parser("verify-ledger")
    vl.add_argument("dir")
    vl.add_argument("--schema", default="ledger_schema.json")

    args = parser.parse_args(argv)
    try:
        if args.command == "verify-claim":
            entry = verify_claim_file(Path(args.path), Path(args.schema))
            _print({"ok": True, "file": args.path, "status": entry.get("status")})
            return 0
        if args.command == "verify-ledger":
            results = verify_ledger_dir(Path(args.dir), Path(args.schema))
            failed = {k: v for k, v in results.items() if not v.get("ok")}
            _print({"ok": not failed, "validated_claims": len(results), "failed_claims": len(failed), "results": results})
            return 0 if not failed else 3
    except GateError as exc:
        _print({"ok": False, "gate": exc.gate, "error": exc.message})
        if exc.gate == "parse_json_gate":
            return 1
        if exc.gate == "schema_gate":
            return 2
        return 3
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
