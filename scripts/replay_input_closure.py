#!/usr/bin/env python3
"""
replay_input_closure.py

V2 design-phase closure generator.

Purpose:
- Build REPLAY_INPUT_CLOSURE_V1 from explicit replay surfaces plus recursively
  discovered local TypeScript and Python imports.
- Emit a canonical closure manifest and input_closure_hash.
- Produce a V2 gap report against a V1/surface-only baseline.

Doctrine:
- UNDECLARED_FILE_AUTHORITY = ZERO
- CACHED_INTERMEDIATE = UNDECLARED_INPUT unless included
- FRESH_GENERATED_INTERMEDIATE = OUTPUT and excluded
- STATIC_IMPORT_DISCOVERY = REQUIRED
- RUNTIME_TRACING = DIAGNOSTIC_ONLY
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

CLOSURE_SCHEMA = "alms/replay_input_closure@v1"
GAP_REPORT_SCHEMA = "alms/replay_input_closure_gap_report@v1"

TS_IMPORT_RE = re.compile(
    r"""(?:import\s+[^;]*?from\s+|export\s+[^;]*?from\s+|import\s*\()\s*['\"](\./[^'\"]+|\.\./[^'\"]+)['\"]""",
    re.MULTILINE,
)

PY_FROM_RE = re.compile(r"""^from\s+\.([\w.]*)\s+import\s+""", re.MULTILINE)
PY_IMPORT_RE = re.compile(r"""^import\s+\.([\w.]*)""", re.MULTILINE)

EXPLICIT_SURFACES = [
    "schemas/UID_V1.schema.json",
    "schemas/WITNESS_V1.schema.json",
    "src/emitter.ts",
    "src/verifier.ts",
    "scripts/l2_batcher.py",
    "scripts/replay_input_closure.py",
    ".github/workflows/witness-replay.yml",
    "tsconfig.json",
    "package.json",
    "package-lock.json",
]

TS_ENTRIES = ["src/emitter.ts", "src/verifier.ts"]
PY_ENTRIES = ["scripts/l2_batcher.py", "scripts/replay_input_closure.py"]


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def in_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolve_ts_candidate(candidate: Path) -> List[Path]:
    if candidate.suffix:
        return [candidate]
    return [
        Path(str(candidate) + ".ts"),
        Path(str(candidate) + ".tsx"),
        candidate / "index.ts",
        candidate / "index.tsx",
    ]


def discover_ts_imports(entry: Path, root: Path) -> Set[Path]:
    visited: Set[Path] = set()
    queue: List[Path] = [entry.resolve()]
    while queue:
        path = queue.pop()
        if path in visited or not path.exists() or not in_root(path, root):
            continue
        visited.add(path)
        text = path.read_text(encoding="utf-8")
        for match in TS_IMPORT_RE.finditer(text):
            raw = match.group(1)
            base = (path.parent / raw).resolve()
            for resolved in resolve_ts_candidate(base):
                if resolved.exists() and in_root(resolved, root):
                    queue.append(resolved.resolve())
    return visited


def resolve_py_candidate(path: Path, rel: str) -> List[Path]:
    base = path.parent / rel if rel else path.parent / "__init__"
    return [base.with_suffix(".py"), base / "__init__.py"]


def discover_py_imports(entry: Path, root: Path) -> Set[Path]:
    visited: Set[Path] = set()
    queue: List[Path] = [entry.resolve()]
    while queue:
        path = queue.pop()
        if path in visited or not path.exists() or not in_root(path, root):
            continue
        visited.add(path)
        text = path.read_text(encoding="utf-8")
        rels = []
        rels += [(m.group(1) or "").replace(".", "/") for m in PY_FROM_RE.finditer(text)]
        rels += [(m.group(1) or "").replace(".", "/") for m in PY_IMPORT_RE.finditer(text)]
        for rel in rels:
            for candidate in resolve_py_candidate(path, rel):
                if candidate.exists() and in_root(candidate, root):
                    queue.append(candidate.resolve())
    return visited


def existing_paths(root: Path, paths: Iterable[str]) -> Set[Path]:
    found: Set[Path] = set()
    for rel in paths:
        path = (root / rel).resolve()
        if path.exists():
            found.add(path)
    return found


def build_input_closure(root: Path) -> Dict[str, str]:
    explicit = existing_paths(root, EXPLICIT_SURFACES)
    discovered: Set[Path] = set()
    for rel in TS_ENTRIES:
        entry = root / rel
        if entry.exists():
            discovered |= discover_ts_imports(entry, root)
    for rel in PY_ENTRIES:
        entry = root / rel
        if entry.exists():
            discovered |= discover_py_imports(entry, root)
    all_paths = explicit | discovered
    closure: Dict[str, str] = {}
    for path in sorted(all_paths, key=lambda p: p.relative_to(root).as_posix()):
        closure[path.relative_to(root).as_posix()] = sha256_file(path)
    return closure


def v1_surface_baseline(root: Path) -> Dict[str, str]:
    return {p.relative_to(root).as_posix(): sha256_file(p) for p in sorted(existing_paths(root, EXPLICIT_SURFACES), key=lambda p: p.relative_to(root).as_posix())}


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(obj) + b"\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build REPLAY_INPUT_CLOSURE_V1")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="_truth/closures/replay_input_closure_v1.json")
    parser.add_argument("--gap-report", default="_truth/closures/replay_input_closure_gap_report_v1.json")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    closure = build_input_closure(root)
    closure_hash = sha256_bytes(canonical_bytes(closure))
    baseline = v1_surface_baseline(root)

    manifest = {
        "schema": CLOSURE_SCHEMA,
        "version": 1,
        "doctrine": {
            "UNDECLARED_FILE_AUTHORITY": "ZERO",
            "CACHED_INTERMEDIATE": "UNDECLARED_INPUT_PROHIBITED_UNLESS_INCLUDED",
            "FRESH_GENERATED_INTERMEDIATE": "OUTPUT_EXCLUDED_FROM_CLOSURE",
            "STATIC_IMPORT_DISCOVERY": "REQUIRED",
            "RUNTIME_TRACING": "DIAGNOSTIC_ONLY",
        },
        "input_closure_hash": closure_hash,
        "files": closure,
    }

    added = sorted(set(closure) - set(baseline))
    missing = sorted(set(baseline) - set(closure))
    changed = sorted(k for k in set(closure) & set(baseline) if closure[k] != baseline[k])
    gap_report = {
        "schema": GAP_REPORT_SCHEMA,
        "version": 1,
        "input_closure_hash": closure_hash,
        "baseline_file_count": len(baseline),
        "closure_file_count": len(closure),
        "auto_discovered_added": added,
        "baseline_missing_from_closure": missing,
        "hash_changed_vs_baseline": changed,
        "v2_gap_detected": bool(added or missing or changed),
    }

    write_json(root / args.out, manifest)
    write_json(root / args.gap_report, gap_report)
    print(f"INPUT_CLOSURE_HASH {closure_hash}")
    print(f"INPUT_CLOSURE_FILES {len(closure)}")
    print(f"V2_GAP_DETECTED {str(gap_report['v2_gap_detected']).lower()}")


if __name__ == "__main__":
    main()
