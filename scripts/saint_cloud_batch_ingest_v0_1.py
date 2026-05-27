#!/usr/bin/env python3
"""
Saint Cloud Batch Ingest v0.1

Corpus-level wrapper for saint_cloud_minutes_hunter_v0_2.py.

Authority: none.
LLM role: advisory only.
Invariant: one corpus, one command, one combined contradiction table.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CSV_FIELDS = [
    "document_date",
    "agenda_item_id",
    "source_doc_id",
    "source_url",
    "source_page",
    "source_line_number",
    "required_field",
    "observed_value",
    "expected_value",
    "classification",
    "extraction_confidence",
    "receipt_hash",
    "commit_hash",
    "source_text_excerpt",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_manifest(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"sources": []}
    return json.loads(path.read_text(encoding="utf-8"))


def source_lookup(manifest: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for source in manifest.get("sources", []):
        for key in ("local_path", "source_id"):
            value = source.get(key)
            if value:
                out[str(value)] = source
        source_id = source.get("source_id")
        if source_id:
            out[str(source_id) + ".txt"] = source
    return out


def iter_inputs(input_dir: Path) -> Iterable[Path]:
    for path in sorted(input_dir.glob("*.txt")):
        if path.is_file():
            yield path


def run_hunter(script: Path, input_path: Path, commit_hash: str, meeting_date: Optional[str], source_url: Optional[str]) -> List[Dict[str, str]]:
    cmd = [
        sys.executable,
        str(script),
        str(input_path),
        "--commit-hash",
        commit_hash,
        "--output-mode",
        "contradiction_rows",
    ]
    if meeting_date:
        cmd.extend(["--meeting-date", meeting_date])
    if source_url:
        cmd.extend(["--source-url", source_url])

    proc = subprocess.run(cmd, check=True, text=True, capture_output=True)
    rows = list(csv.DictReader(proc.stdout.splitlines()))
    return rows


def validate_row(row: Dict[str, str], commit_hash: str) -> None:
    missing = [field for field in CSV_FIELDS if field not in row]
    if missing:
        raise ValueError(f"row missing CSV fields: {missing}")
    if row["commit_hash"] != commit_hash:
        raise ValueError("row commit_hash does not match batch commit hash")
    if not row["receipt_hash"].startswith("sha256:") or len(row["receipt_hash"]) != 71:
        raise ValueError("row receipt_hash must be sha256:<64 hex>")


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-ingest Saint Cloud minutes text files into one contradiction table")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--commit-hash", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--hunter", type=Path, default=Path("scripts/saint_cloud_minutes_hunter_v0_2.py"))
    args = parser.parse_args()

    if not COMMIT_RE.fullmatch(args.commit_hash):
        raise SystemExit("--commit-hash must be a 40-character lowercase hex commit hash")
    if not args.input_dir.exists():
        raise SystemExit(f"input directory not found: {args.input_dir}")
    if not args.hunter.exists():
        raise SystemExit(f"hunter script not found: {args.hunter}")

    manifest = load_manifest(args.manifest)
    lookup = source_lookup(manifest)
    all_rows: List[Dict[str, str]] = []
    chain_of_custody: List[Dict[str, Any]] = []

    for input_path in iter_inputs(args.input_dir):
        source = lookup.get(str(input_path)) or lookup.get(input_path.name) or {}
        meeting_date = source.get("meeting_date")
        source_url = source.get("source_url")
        rows = run_hunter(args.hunter, input_path, args.commit_hash, meeting_date, source_url)
        for row in rows:
            validate_row(row, args.commit_hash)
        all_rows.extend(rows)
        chain_of_custody.append({
            "input_file": str(input_path),
            "input_sha256": sha256_file(input_path),
            "meeting_date": meeting_date,
            "source_url": source_url,
            "row_count": len(rows),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    custody_path = args.output.with_suffix(".chain_of_custody.json")
    custody_payload = {
        "authority": False,
        "llm_role": "ADVISORY_ONLY",
        "commit_hash": args.commit_hash,
        "manifest": str(args.manifest),
        "output": str(args.output),
        "output_sha256": sha256_file(args.output),
        "sources": chain_of_custody,
        "row_count": len(all_rows),
    }
    custody_path.write_text(json.dumps(custody_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(custody_payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
