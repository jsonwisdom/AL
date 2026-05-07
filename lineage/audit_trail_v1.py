#!/usr/bin/env python3
"""
Lineage Audit Trail v1

Audits lineage/asset_lineage_events.jsonl as a tamper-evident append-only log.

Genesis rule:
  Event 0 MUST use GENESIS_PREV_FILE_HASH.

Core law:
  If history cannot be replayed, sovereignty is only narrative.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


GENESIS_PREV_FILE_HASH = "sha256:" + ("0" * 64)

AUDIT_PASS = "AUDIT_PASS"
LINEAGE_TAMPER_DETECTED = "LINEAGE_TAMPER_DETECTED"
EVENT_INDEX_GAP = "EVENT_INDEX_GAP"
EVENT_INDEX_DUPLICATE = "EVENT_INDEX_DUPLICATE"
HASH_REBIND_DETECTED = "HASH_REBIND_DETECTED"
MALFORMED_EVENT = "MALFORMED_EVENT"

REQUIRED_FIELDS = {
    "event_type",
    "event_index",
    "prev_file_hash",
    "asset_id",
    "asset_hash",
    "hash_algorithm",
    "branch_id",
    "manifest_hash",
    "cbre_trace_hash",
    "timestamp_utc",
    "signature",
}


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_line(event: dict[str, Any]) -> bytes:
    """Canonical JSONL line used for replaying file-state hashes."""
    return (json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events

    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if raw.strip() == "":
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
        if not isinstance(event, dict):
            raise ValueError(f"line {line_no}: event is not an object")
        missing = REQUIRED_FIELDS.difference(event)
        if missing:
            raise ValueError(f"line {line_no}: missing fields: {sorted(missing)}")
        events.append(event)
    return events


def audit_events(events: list[dict[str, Any]]) -> tuple[str, list[str]]:
    messages: list[str] = []
    seen_indexes: set[int] = set()
    asset_bindings: dict[str, str] = {}
    file_state = b""

    for expected_index, event in enumerate(events):
        event_index = event.get("event_index")
        if not isinstance(event_index, int):
            return (MALFORMED_EVENT, [f"event {expected_index}: event_index is not integer"])

        if event_index in seen_indexes:
            return (EVENT_INDEX_DUPLICATE, [f"event_index duplicated: {event_index}"])
        seen_indexes.add(event_index)

        if event_index != expected_index:
            return (EVENT_INDEX_GAP, [f"expected event_index {expected_index}, got {event_index}"])

        expected_prev = GENESIS_PREV_FILE_HASH if expected_index == 0 else sha256_hex(file_state)
        actual_prev = event.get("prev_file_hash")
        if actual_prev != expected_prev:
            return (
                LINEAGE_TAMPER_DETECTED,
                [
                    f"event_index {event_index}: prev_file_hash mismatch",
                    f"expected {expected_prev}",
                    f"actual   {actual_prev}",
                ],
            )

        asset_id = event.get("asset_id")
        asset_hash = event.get("asset_hash")
        if not isinstance(asset_id, str) or not isinstance(asset_hash, str):
            return (MALFORMED_EVENT, [f"event_index {event_index}: asset_id/asset_hash malformed"])

        prior_hash = asset_bindings.get(asset_id)
        if prior_hash is not None and prior_hash != asset_hash:
            return (
                HASH_REBIND_DETECTED,
                [
                    f"asset_id {asset_id}: hash rebind detected",
                    f"prior {prior_hash}",
                    f"new   {asset_hash}",
                    f"event_index {event_index}",
                ],
            )
        asset_bindings[asset_id] = asset_hash

        file_state += canonical_line(event)

    messages.append(f"events={len(events)}")
    messages.append(f"asset_ids={len(asset_bindings)}")
    messages.append(f"final_file_hash={sha256_hex(file_state)}")
    return (AUDIT_PASS, messages)


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("lineage/asset_lineage_events.jsonl")
    try:
        events = load_events(path)
        status, messages = audit_events(events)
    except ValueError as exc:
        status, messages = MALFORMED_EVENT, [str(exc)]

    print(status)
    for message in messages:
        print(message)
    return 0 if status == AUDIT_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
