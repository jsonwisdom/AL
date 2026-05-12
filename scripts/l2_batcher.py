#!/usr/bin/env python3
"""
l2_batcher.py

Local-only L2 batcher scaffold for AL witness replay outputs.

Non-negotiables:
- Does not touch chain.
- Does not mutate witnesses.
- Produces deterministic JSON with sorted keys and compact UTF-8 bytes.
- Computes batch_hash with batch_hash excluded from the hash preimage.
- Verifies each witness by hash and, when available, by the existing Node witness verifier.

Commands:
  create  -> build a deterministic batch_manifest.json from witness JSON files
  verify  -> verify batch_manifest.json and emit replay_report.json
  eas     -> build an offline EAS payload draft from a verified manifest; no broadcast
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ZERO_PREV_BATCH_HASH = "sha256:" + ("0" * 64)
MANIFEST_SCHEMA = "alms/l2_batch_manifest@v1"
REPORT_SCHEMA = "alms/l2_batch_replay_report@v1"
EAS_PAYLOAD_SCHEMA = "alms/eas_integrity_witness_payload@v1"


def die(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_prefixed(data: bytes) -> str:
    return "sha256:" + sha256_hex(data)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        die(f"failed to read JSON {path}: {exc}")


def write_canonical_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(obj) + b"\n")


def batch_hash_preimage(manifest: Dict[str, Any]) -> Dict[str, Any]:
    clone = dict(manifest)
    clone.pop("batch_hash", None)
    return clone


def compute_batch_hash(manifest: Dict[str, Any]) -> str:
    return sha256_prefixed(canonical_bytes(batch_hash_preimage(manifest)))


def strict_witness_entry(path: Path, repo_root: Path) -> Dict[str, Any]:
    witness = read_json(path)
    if witness.get("schema") != "alms/witness@v1":
        die(f"witness schema mismatch: {path}")
    uid = witness.get("uid")
    envelope = witness.get("envelope", {})
    event_payload_hash = envelope.get("event_payload_hash")
    if not isinstance(uid, str) or not uid.startswith("uid:"):
        die(f"missing/invalid witness uid: {path}")
    if not isinstance(event_payload_hash, str) or not event_payload_hash.startswith("sha256:"):
        die(f"missing/invalid event_payload_hash: {path}")

    raw = path.read_bytes()
    try:
        rel = path.relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    witness_hash = sha256_prefixed(raw)
    return {
        "event_payload_hash": event_payload_hash,
        "replay_hash": witness_hash,
        "witness_id": uid,
        "witness_path": rel,
        "witness_sha256": witness_hash,
    }


def load_witnesses(witness_dir: Path, repo_root: Path) -> List[Dict[str, Any]]:
    if not witness_dir.exists():
        die(f"witness directory not found: {witness_dir}")
    files = sorted(witness_dir.glob("uid:*.json"))
    if not files:
        die(f"no witness files found in {witness_dir}")
    entries = [strict_witness_entry(path, repo_root) for path in files]
    entries.sort(key=lambda item: item["witness_id"])
    return entries


def create_manifest(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_root).resolve()
    witness_dir = (repo_root / args.witness_dir).resolve()
    out = (repo_root / args.out).resolve()
    entries = load_witnesses(witness_dir, repo_root)

    manifest: Dict[str, Any] = {
        "schema": MANIFEST_SCHEMA,
        "version": 1,
        "repo": "jsonwisdom/AL",
        "witness_replay_tag": args.witness_replay_tag,
        "prev_batch_hash": args.prev_batch_hash,
        "witness_count": len(entries),
        "witnesses": entries,
    }
    manifest["batch_hash"] = compute_batch_hash(manifest)
    write_canonical_json(out, manifest)
    print(f"BATCH_MANIFEST_WRITTEN {out}")
    print(f"BATCH_HASH {manifest['batch_hash']}")


def run_node_verifier(repo_root: Path, witness_path: Path) -> Tuple[bool, str]:
    package_json = repo_root / "package.json"
    verifier = repo_root / "src" / "verifier.ts"
    if not package_json.exists() or not verifier.exists():
        return False, "node verifier unavailable"
    cmd = ["npm", "run", "witness:verify", "--", witness_path.as_posix()]
    proc = subprocess.run(
        cmd,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode == 0 and "REPLAY_OK uid:" in proc.stdout, proc.stdout.strip()


def verify_manifest(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_root).resolve()
    manifest_path = (repo_root / args.manifest).resolve()
    report_path = (repo_root / args.report).resolve()
    manifest = read_json(manifest_path)

    recorded_batch_hash = manifest.get("batch_hash")
    computed_batch_hash = compute_batch_hash(manifest)
    batch_hash_ok = recorded_batch_hash == computed_batch_hash

    witnesses = manifest.get("witnesses", [])
    sort_order_ok = witnesses == sorted(witnesses, key=lambda item: item.get("witness_id", ""))
    witness_count_ok = manifest.get("witness_count") == len(witnesses)
    prev_batch_hash = manifest.get("prev_batch_hash")
    prev_batch_hash_ok = isinstance(prev_batch_hash, str) and prev_batch_hash.startswith("sha256:") and len(prev_batch_hash) == 71

    witness_reports: List[Dict[str, Any]] = []
    for entry in witnesses:
        rel_path = entry.get("witness_path")
        witness_id = entry.get("witness_id")
        witness_path = repo_root / rel_path if isinstance(rel_path, str) else repo_root / "__missing__"
        exists = witness_path.exists()
        raw_hash = sha256_prefixed(witness_path.read_bytes()) if exists else None
        witness_hash_ok = exists and raw_hash == entry.get("witness_sha256") == entry.get("replay_hash")
        node_ok = False
        node_output = "not run"
        if exists:
            node_ok, node_output = run_node_verifier(repo_root, witness_path)
        witness_reports.append(
            {
                "witness_id": witness_id,
                "witness_path": rel_path,
                "exists": exists,
                "witness_hash_ok": bool(witness_hash_ok),
                "node_replay_ok": bool(node_ok),
                "node_output": node_output,
            }
        )

    all_witnesses_ok = all(item["exists"] and item["witness_hash_ok"] and item["node_replay_ok"] for item in witness_reports)
    overall_pass = bool(batch_hash_ok and sort_order_ok and witness_count_ok and prev_batch_hash_ok and all_witnesses_ok)

    report = {
        "schema": REPORT_SCHEMA,
        "version": 1,
        "manifest_path": manifest_path.relative_to(repo_root).as_posix() if manifest_path.is_relative_to(repo_root) else manifest_path.as_posix(),
        "batch_hash_recorded": recorded_batch_hash,
        "batch_hash_computed": computed_batch_hash,
        "batch_hash_ok": batch_hash_ok,
        "sort_order_ok": sort_order_ok,
        "witness_count_ok": witness_count_ok,
        "prev_batch_hash_ok": prev_batch_hash_ok,
        "all_witnesses_ok": all_witnesses_ok,
        "overall_pass": overall_pass,
        "witnesses": witness_reports,
    }
    write_canonical_json(report_path, report)
    print(f"REPLAY_REPORT_WRITTEN {report_path}")
    print("BATCH_REPLAY_PASS" if overall_pass else "BATCH_REPLAY_FAIL")
    raise SystemExit(0 if overall_pass else 1)


def build_eas_payload(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_root).resolve()
    manifest_path = (repo_root / args.manifest).resolve()
    out = (repo_root / args.out).resolve()
    manifest = read_json(manifest_path)
    batch_hash = manifest.get("batch_hash")
    if compute_batch_hash(manifest) != batch_hash:
        die("manifest batch_hash does not verify; refusing EAS payload")
    payload = {
        "schema": EAS_PAYLOAD_SCHEMA,
        "version": 1,
        "anchor_purpose": "integrity_witness_only",
        "batchHash": batch_hash,
        "witnessReplayTag": manifest.get("witness_replay_tag"),
        "witnessCount": manifest.get("witness_count"),
        "prevBatchHash": manifest.get("prev_batch_hash"),
        "manifestURI": args.manifest_uri,
        "broadcast": False,
    }
    write_canonical_json(out, payload)
    print(f"EAS_PAYLOAD_DRAFT_WRITTEN {out}")
    print("NO_CHAIN_BROADCAST")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local deterministic L2 batcher scaffold")
    parser.add_argument("--repo-root", default=".")
    sub = parser.add_subparsers(dest="cmd", required=True)

    create = sub.add_parser("create")
    create.add_argument("--witness-dir", default=".runtime/witnesses")
    create.add_argument("--out", default="_truth/batches/batch_manifest.json")
    create.add_argument("--witness-replay-tag", default="witness-replay-green-v1")
    create.add_argument("--prev-batch-hash", default=ZERO_PREV_BATCH_HASH)
    create.set_defaults(func=create_manifest)

    verify = sub.add_parser("verify")
    verify.add_argument("--manifest", default="_truth/batches/batch_manifest.json")
    verify.add_argument("--report", default="_truth/batches/replay_report.json")
    verify.set_defaults(func=verify_manifest)

    eas = sub.add_parser("eas")
    eas.add_argument("--manifest", default="_truth/batches/batch_manifest.json")
    eas.add_argument("--out", default="_truth/batches/eas_payload.draft.json")
    eas.add_argument("--manifest-uri", default="")
    eas.set_defaults(func=build_eas_payload)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
