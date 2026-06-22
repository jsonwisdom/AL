#!/usr/bin/env python3
"""Dry-run validator for EAS_ZORA_1155_CONTINUITY_V0_1.

This script performs no network calls, no schema registration, no attestation,
and no mint. It validates local draft artifacts and emits deterministic hashes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path("docs/continuity/eas_zora_1155_schema_v0_1.json")
ACTIVE_LANES_PATH = Path("ACTIVE_LANES.json")
EXPECTED_SCHEMA_STRING = (
    "string tokenId,string zoraContract,string metadataURI,string continuityCommit,"
    "string receiptHash,string replayHash,string laneRoot,string zoraRef,"
    "bool isSoulbound,uint256 mintTimestamp"
)
EXPECTED_FIELD_ORDER = [
    "tokenId",
    "zoraContract",
    "metadataURI",
    "continuityCommit",
    "receiptHash",
    "replayHash",
    "laneRoot",
    "zoraRef",
    "isSoulbound",
    "mintTimestamp",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_json(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    active_lanes = load_json(ACTIVE_LANES_PATH)

    assert schema.get("status") == "DRAFT_ONLY_NOT_REGISTERED", schema.get("status")
    assert schema.get("authority") == "NONE", schema.get("authority")
    assert schema.get("schema_uid") is None
    assert schema.get("registry_tx_hash") is None
    assert schema.get("schema_string") == EXPECTED_SCHEMA_STRING

    fields = schema.get("fields")
    assert isinstance(fields, list), "fields must be a list"
    field_order = [field.get("name") for field in fields]
    assert field_order == EXPECTED_FIELD_ORDER, field_order

    lanes = active_lanes.get("lanes")
    assert isinstance(lanes, list), "ACTIVE_LANES.json must contain lanes"

    lane_root = sha256_json(lanes)
    replay_payload = {
        "schema_name": schema.get("schema_name"),
        "schema_string": schema.get("schema_string"),
        "field_order": field_order,
        "active_lanes_schema_version": active_lanes.get("schema_version"),
        "lane_root": lane_root,
        "no_fake_green": schema.get("no_fake_green") is True,
    }
    replay_hash = sha256_json(replay_payload)

    receipt = {
        "dry_run": "EAS_ZORA_1155_CONTINUITY_V0_1",
        "status": "DRY_RUN_PASS",
        "network_calls": 0,
        "on_chain_actions": 0,
        "schema_uid": None,
        "registry_tx_hash": None,
        "lane_root": lane_root,
        "replay_hash": replay_hash,
        "delta_h": 0,
        "no_fake_green": True,
    }

    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
