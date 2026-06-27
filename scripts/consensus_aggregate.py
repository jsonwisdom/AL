#!/usr/bin/env python3
"""ALMS v2.8 witness consensus aggregator.

Sprint 1 strict mode: every submitted configured witness attestation must be
PASS, authority=false, and all submitted state_roots must match the replay
manifest state_root. The witness allow-list comes from the committed witness
config, not from the manifest being evaluated.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


class ConsensusError(SystemExit):
    """Explicit halt for non-consensus states."""


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def norm_root(value: str) -> str:
    value = value.strip()
    if not value.startswith("0x"):
        value = "0x" + value
    if len(value) != 66:
        raise ValueError(f"invalid state_root length: {value}")
    int(value[2:], 16)
    return value.lower()


def configured_witness_ids(witness_config: dict[str, Any]) -> set[str]:
    witnesses = witness_config.get("witnesses", [])
    ids = [w["id"] for w in witnesses]
    if len(ids) != len(set(ids)):
        raise ConsensusError("HALT_ON_MISMATCH: duplicate configured witness id")
    return set(ids)


def manifest_status_ok(manifest: dict[str, Any]) -> None:
    if manifest.get("status") != "PASS":
        raise ConsensusError("HALT_ON_MISMATCH: manifest status is not PASS")
    if manifest.get("authority") is not False:
        raise ConsensusError("HALT_ON_MISMATCH: manifest authority is not false")


def aggregate(manifest: dict[str, Any], witness_config: dict[str, Any]) -> dict[str, Any]:
    manifest_status_ok(manifest)

    consensus = manifest["consensus"]
    threshold = int(consensus["threshold"])
    attestations = consensus["attestations"]
    configured_ids = configured_witness_ids(witness_config)
    manifest_root = norm_root(manifest["state_root"])

    if threshold != int(witness_config.get("threshold", threshold)):
        raise ConsensusError("HALT_ON_MISMATCH: manifest threshold differs from witness config")
    if threshold < 2:
        raise ConsensusError("HALT_ON_MISMATCH: threshold must be >= 2")
    if len(configured_ids) < threshold:
        raise ConsensusError("HALT_ON_MISMATCH: threshold exceeds configured witnesses")

    seen_witness_ids: set[str] = set()
    seen_uids: set[str] = set()
    valid: list[dict[str, Any]] = []

    for item in attestations:
        witness_id = item.get("witness_id")
        uid = item.get("uid")

        if witness_id not in configured_ids:
            raise ConsensusError(f"HALT_ON_MISMATCH: unknown witness_id {witness_id}")
        if witness_id in seen_witness_ids:
            raise ConsensusError(f"HALT_ON_MISMATCH: duplicate witness_id {witness_id}")
        if uid in seen_uids:
            raise ConsensusError(f"HALT_ON_MISMATCH: duplicate uid {uid}")

        seen_witness_ids.add(witness_id)
        seen_uids.add(uid)

        if item.get("status") != "PASS":
            raise ConsensusError(f"HALT_ON_MISMATCH: non-PASS status from {witness_id}")
        if item.get("authority") is not False:
            raise ConsensusError(f"HALT_ON_MISMATCH: authority claim from {witness_id}")

        witness_root = norm_root(item["state_root"])
        if witness_root != manifest_root:
            raise ConsensusError(f"HALT_ON_MISMATCH: state_root mismatch from {witness_id}")

        valid.append({**item, "state_root": witness_root})

    if len(valid) < threshold:
        raise ConsensusError(
            f"HALT_ON_MISMATCH: valid={len(valid)}, threshold={threshold}"
        )

    by_root: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in valid:
        by_root[item["state_root"]].append(item)

    if len(by_root) != 1:
        raise ConsensusError(f"HALT_ON_MISMATCH: root_groups={len(by_root)}")

    state_root, matched = next(iter(by_root.items()))
    if state_root != manifest_root:
        raise ConsensusError("HALT_ON_MISMATCH: consensus root differs from manifest root")
    if len(matched) < threshold:
        raise ConsensusError(
            f"HALT_ON_MISMATCH: matched={len(matched)}, threshold={threshold}"
        )

    return {
        "framework": "WITNESS_CONSENSUS_V2_8",
        "consensusId": manifest.get("consensusId", manifest.get("consensus_id", "")),
        "repo": manifest.get("repo", "jsonwisdom/AL"),
        "tag": manifest.get("tag", "v2.8-live"),
        "threshold": threshold,
        "witnessCount": len(configured_ids),
        "stateRoot": state_root,
        "matchedWitnesses": ",".join(a["witness_id"] for a in matched),
        "witnessUids": ",".join(a["uid"] for a in matched),
        "replayCid": manifest.get("replayCid", manifest.get("replay_cid", "")),
        "authority": False,
        "status": "PASS"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="v2.8 replay manifest JSON")
    parser.add_argument(
        "--witness-config",
        default="config/witnesses.v2.8.json",
        help="committed witness allow-list JSON"
    )
    parser.add_argument("--out", default="consensus-output.v2.8.json")
    args = parser.parse_args()

    result = aggregate(load_json(args.manifest), load_json(args.witness_config))
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
