#!/usr/bin/env python3
"""ALMS v2.8 witness consensus aggregator.

Reads witness attestations from JSON, requires threshold matching state_root,
and emits a consensus packet. Posting the final EAS consensus attestation is
left explicit/off by default so CI cannot silently mint authority.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def norm_root(value: str) -> str:
    value = value.strip()
    if not value.startswith("0x"):
        value = "0x" + value
    if len(value) != 66:
        raise ValueError(f"invalid state_root length: {value}")
    return value.lower()


def aggregate(manifest: dict[str, Any]) -> dict[str, Any]:
    consensus = manifest["consensus"]
    threshold = int(consensus["threshold"])
    attestations = consensus["attestations"]

    valid = []
    for item in attestations:
        if item.get("status") != "PASS":
            continue
        if item.get("authority") is not False:
            continue
        valid.append({**item, "state_root": norm_root(item["state_root"])})

    counts = Counter(a["state_root"] for a in valid)
    if not counts:
        raise SystemExit("HALT_ON_MISMATCH: no valid PASS/authority=false attestations")

    state_root, count = counts.most_common(1)[0]
    if count < threshold:
        raise SystemExit(f"HALT_ON_MISMATCH: best={count}, threshold={threshold}")

    matched = [a for a in valid if a["state_root"] == state_root]
    return {
        "framework": "WITNESS_CONSENSUS_V2_8",
        "consensus_id": manifest.get("consensus_id", ""),
        "repo": manifest.get("repo", "jsonwisdom/AL"),
        "tag": manifest.get("tag", "v2.8-live"),
        "threshold": threshold,
        "witness_count": len(consensus.get("witnesses", [])),
        "state_root": state_root,
        "matched_witnesses": [a["witness_id"] for a in matched],
        "witness_uids": [a["uid"] for a in matched],
        "replay_cid": manifest.get("replay_cid", ""),
        "authority": False,
        "status": "PASS"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="v2.8 replay manifest JSON")
    parser.add_argument("--out", default="consensus-output.v2.8.json")
    args = parser.parse_args()

    result = aggregate(load_json(args.manifest))
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
