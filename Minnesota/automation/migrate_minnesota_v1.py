#!/usr/bin/env python3
"""Receipt-first migration of Minnesota material into the canonical Minnesota/ root."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

POLICY_PATH = Path("Minnesota/MIGRATION_POLICY_V1.json")
MANIFEST_PATH = Path("Minnesota/manifests/MN_CORPUS_MANIFEST_V1.json")
RECEIPT_DIR = Path("Minnesota/receipts/migration")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_id(value: str | None) -> str:
    raw = value or os.environ.get("GITHUB_RUN_ID") or utc_now()
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", raw).strip("-")


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=check)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def under_prefix(path: str, prefix: str) -> bool:
    path = path.strip("/")
    prefix = prefix.strip("/")
    return path == prefix or path.startswith(prefix + "/")


def excluded(path: str, policy: dict) -> bool:
    return any(under_prefix(path, prefix) for prefix in policy["exclude_prefixes"])


def iter_files(root: Path, policy: dict):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = rel(path, root)
        if relative.startswith(".git/") or excluded(relative, policy):
            continue
        yield path


def safe_class(path: str, policy: dict) -> str | None:
    for prefix in policy["safe_prefixes"]:
        if under_prefix(path, prefix):
            return f"safe_prefix:{prefix}"
    for pattern in policy["safe_globs"]:
        if fnmatch.fnmatch(path, pattern):
            return f"safe_glob:{pattern}"
    return None


def discover(root: Path, policy: dict) -> tuple[list[dict], list[dict]]:
    destination_root = root / policy["destination_root"]
    moves: list[dict] = []
    safe_sources: set[str] = set()

    for source in iter_files(root, policy):
        source_rel = rel(source, root)
        classification = safe_class(source_rel, policy)
        if classification is None:
            continue
        destination = destination_root / source_rel
        digest = sha256_file(source)
        status = "READY"
        if destination.exists():
            status = "DUPLICATE_ALREADY_PRESENT" if sha256_file(destination) == digest else "DESTINATION_CONFLICT"
        moves.append({
            "source": source_rel,
            "destination": rel(destination, root),
            "sha256": digest,
            "size_bytes": source.stat().st_size,
            "classification": classification,
            "status": status,
        })
        safe_sources.add(source_rel)

    review: list[dict] = []
    text_extensions = set(policy["text_extensions"])
    path_markers = [marker.casefold() for marker in policy["review_path_markers"]]
    content_markers = policy["review_content_markers"]
    protected = {
        POLICY_PATH.as_posix(),
        "Minnesota/automation/migrate_minnesota_v1.py",
        ".github/workflows/minnesota-canonical-migration.yml",
    }

    for path in iter_files(root, policy):
        path_rel = rel(path, root)
        if path_rel in safe_sources or path_rel in protected:
            continue
        reasons = [f"path:{m}" for m in path_markers if m in path_rel.casefold()]
        if path.suffix.lower() in text_extensions and path.stat().st_size <= int(policy["max_content_scan_bytes"]):
            try:
                folded = path.read_text(encoding="utf-8").casefold()
            except (UnicodeDecodeError, OSError):
                folded = ""
            reasons += [f"content:{m}" for m in content_markers if m.casefold() in folded]
        if reasons:
            review.append({
                "path": path_rel,
                "reasons": sorted(set(reasons)),
                "size_bytes": path.stat().st_size,
            })

    return sorted(moves, key=lambda x: x["source"]), sorted(review, key=lambda x: x["path"])


def is_tracked(root: Path, path: Path) -> bool:
    result = git(root, "ls-files", "--error-unmatch", rel(path, root), check=False)
    return result.returncode == 0


def move_one(root: Path, source: Path, destination: Path, duplicate: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if duplicate:
        if is_tracked(root, source):
            git(root, "rm", "-f", rel(source, root))
        else:
            source.unlink()
        return
    if is_tracked(root, source):
        git(root, "mv", rel(source, root), rel(destination, root))
    else:
        shutil.move(str(source), str(destination))


def mutable_text(path_rel: str, policy: dict) -> bool:
    if any(under_prefix(path_rel, prefix) for prefix in policy["immutable_destination_prefixes"]):
        return False
    return any(fnmatch.fnmatch(path_rel, pattern) for pattern in policy["rewrite_globs"])


def rewrite_references(root: Path, policy: dict, moves: list[dict]) -> list[dict]:
    replacements = {item["source"]: item["destination"] for item in moves}
    for prefix in policy["safe_prefixes"]:
        replacements[prefix] = f'{policy["destination_root"]}/{prefix}'
    keys = sorted(replacements, key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(key) for key in keys)) if keys else None
    changes: list[dict] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        path_rel = rel(path, root)
        if not mutable_text(path_rel, policy):
            continue
        if path.stat().st_size > int(policy["max_content_scan_bytes"]):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if pattern is None:
            continue
        applied = sorted(set(pattern.findall(original)))
        updated = pattern.sub(lambda match: replacements[match.group(0)], original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changes.append({"path": path_rel, "replacements": applied})
    return changes


def build_manifest(root: Path) -> dict:
    entries: list[dict] = []
    mn_root = root / "Minnesota"
    for path in sorted(mn_root.rglob("*")):
        if not path.is_file():
            continue
        path_rel = rel(path, root)
        if path_rel == MANIFEST_PATH.as_posix() or path_rel.startswith(RECEIPT_DIR.as_posix() + "/"):
            continue
        entries.append({
            "path": path_rel,
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })
    aggregate = hashlib.sha256()
    for item in entries:
        aggregate.update((item["path"] + "\0" + item["sha256"] + "\n").encode("utf-8"))
    return {
        "schema": "MN_CORPUS_MANIFEST_V1",
        "generated_at": utc_now(),
        "entry_count": len(entries),
        "aggregate_sha256": aggregate.hexdigest(),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "apply"), default="dry-run")
    parser.add_argument("--confirm", default="")
    parser.add_argument("--run-id")
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").stdout.strip())
    policy = json.loads((root / POLICY_PATH).read_text(encoding="utf-8"))
    branch = git(root, "branch", "--show-current").stdout.strip()
    before_commit = git(root, "rev-parse", "HEAD").stdout.strip()
    moves, review = discover(root, policy)
    conflicts = [item for item in moves if item["status"] == "DESTINATION_CONFLICT"]

    result = {
        "schema": "MN_CANONICAL_MIGRATION_RECEIPT_V1",
        "run_id": safe_id(args.run_id),
        "generated_at": utc_now(),
        "mode": args.mode,
        "branch": branch,
        "before_commit": before_commit,
        "policy_id": policy["policy_id"],
        "policy_version": policy["version"],
        "move_count": len(moves),
        "review_count": len(review),
        "conflict_count": len(conflicts),
        "moves": moves,
        "review_queue": review,
        "governance": policy["governance"],
        "status": "DRY_RUN_COMPLETE",
    }

    if args.mode == "apply":
        if args.confirm != policy["apply_confirmation"]:
            raise SystemExit("APPLY_BLOCKED: exact confirmation phrase required")
        if branch in {"main", "master"}:
            raise SystemExit("APPLY_BLOCKED: direct default-branch mutation forbidden")
        if conflicts:
            raise SystemExit(f"APPLY_BLOCKED: {len(conflicts)} destination conflicts")

        for item in moves:
            source = root / item["source"]
            destination = root / item["destination"]
            if not source.exists():
                continue
            move_one(root, source, destination, item["status"] == "DUPLICATE_ALREADY_PRESENT")

        pre_rewrite_failures: list[dict] = []
        for item in moves:
            destination = root / item["destination"]
            if not destination.exists() or sha256_file(destination) != item["sha256"]:
                pre_rewrite_failures.append(item)

        old_paths_remaining = [item["source"] for item in moves if (root / item["source"]).exists()]
        if pre_rewrite_failures or old_paths_remaining:
            result["status"] = "VERIFY_FAILED_BEFORE_REWRITE"
            result["verification_failures"] = pre_rewrite_failures
            result["old_paths_remaining"] = old_paths_remaining
            raise SystemExit(json.dumps(result, indent=2))

        rewrites = rewrite_references(root, policy, moves)
        immutable_failures: list[dict] = []
        mutable_hashes: list[dict] = []
        for item in moves:
            destination = root / item["destination"]
            post_hash = sha256_file(destination)
            if mutable_text(item["destination"], policy):
                mutable_hashes.append({
                    "path": item["destination"],
                    "source_sha256": item["sha256"],
                    "post_rewrite_sha256": post_hash,
                })
            elif post_hash != item["sha256"]:
                immutable_failures.append(item)

        if immutable_failures:
            result["status"] = "IMMUTABLE_BYTES_CHANGED"
            result["verification_failures"] = immutable_failures
            raise SystemExit(json.dumps(result, indent=2))

        manifest = build_manifest(root)
        write_json(root / MANIFEST_PATH, manifest)
        result.update({
            "status": "APPLY_VERIFIED",
            "rewrite_count": len(rewrites),
            "rewrites": rewrites,
            "mutable_post_rewrite_hashes": mutable_hashes,
            "manifest_path": MANIFEST_PATH.as_posix(),
            "manifest_aggregate_sha256": manifest["aggregate_sha256"],
        })
        receipt_path = root / RECEIPT_DIR / f'{result["run_id"]}.json'
        write_json(receipt_path, result)
        write_json(root / RECEIPT_DIR / "latest.json", result)

    if args.output:
        write_json(Path(args.output), result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or str(exc), file=sys.stderr)
        raise SystemExit(exc.returncode or 1)
