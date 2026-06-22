#!/usr/bin/env python3
"""Generate ACTIVE_LANES.md from ACTIVE_LANES.json.

This script is intentionally a pure projection:
JSON in, Markdown out, no lane-status decisions made here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_SCHEMA_VERSION = "1.0"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_markdown(data: dict[str, Any]) -> str:
    schema_version = data.get("schema_version")
    assert schema_version == EXPECTED_SCHEMA_VERSION, (
        f"Unexpected schema version: {schema_version}"
    )

    lanes = data.get("lanes")
    if not isinstance(lanes, list):
        raise ValueError("ACTIVE_LANES.json must contain a 'lanes' array")

    lines: list[str] = [
        "# ACTIVE_LANES.md",
        "",
        f"Schema Version: `{schema_version}`",
        "",
        "> Generated from `ACTIVE_LANES.json`. Do not hand-edit this file.",
        "",
        "## Policy",
        "",
        "NO LANE STATUS WITHOUT RECEIPT.",
        "",
        "`GREEN` requires `status_source=VERIFIED_RECEIPT`, `receipt_ptr != null`, `replay_verdict=PASS`, and `delta_h=0`.",
        "",
        "## Lanes",
        "",
        "| LANE | STATUS | STATUS_SOURCE | RECEIPT_PTR | REPLAY_VERDICT | DELTA_H |",
        "| :--- | :--- | :--- | :--- | :--- | ---: |",
    ]

    for lane in lanes:
        receipt_ptr = lane.get("receipt_ptr")
        receipt_display = "NULL" if receipt_ptr is None else str(receipt_ptr)
        lines.append(
            "| {lane_id} | {status} | {status_source} | {receipt_ptr} | {replay_verdict} | {delta_h} |".format(
                lane_id=lane.get("lane_id", ""),
                status=lane.get("status", ""),
                status_source=lane.get("status_source", ""),
                receipt_ptr=receipt_display,
                replay_verdict=lane.get("replay_verdict", ""),
                delta_h=lane.get("delta_h", ""),
            )
        )

    lines.extend([
        "",
        "## Replay Note",
        "",
        "This file is a projection artifact. The admissible source is `ACTIVE_LANES.json`.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="ACTIVE_LANES.json")
    parser.add_argument("--output", default="ACTIVE_LANES.md")
    args = parser.parse_args()

    data = load_json(Path(args.input))
    output = render_markdown(data)
    Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
