#!/usr/bin/env python3
"""Replay Court authority-bounds validator.

v0 scope:
- recompute current witness root from public protected files
- detect protected core modifications in a PR diff when possible
- require amendment metadata for protected-core changes
- enforce FAIL, not UNOBSERVED, for authority-bound violations
- emit deterministic JSON validation receipt

This validator rejects drift. It does not create truth, authorize payment,
erase contradiction, or replace replay.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1.0"
GENESIS_WITNESS_ROOT = "sha256:ea943c9c5a0515dc09c43f52543bfbb8d40c3a7c2d86a04cabacd1e9696c67d7"
GENESIS_COMMIT = "caa8e8f6cc5d085b101b1f3f83ef17768966119b"
OPERATIONAL_TIMELOCK_SECONDS = 48 * 60 * 60
STRUCTURAL_TIMELOCK_SECONDS = 7 * 24 * 60 * 60

PROTECTED_CORE_FILES = [
    "GAME_MECHANICS.md",
    "AGENT_PLAYBOOK.md",
    "COMPUTER_WISDOM.md",
    "replay-court/PROCESS.md",
    "replay-court/SELF-AUDIT.md",
    "replay-court/VALIDATOR.md",
    "replay-court/REPAIR-LEDGER.md",
    "replay-court/CONTRADICTION-STORE.md",
    "replay-court/AUTHORITY-BOUNDS.md",
    "replay-court/WITNESS-ANCHOR.md",
    "replay-court/BOOTSTRAP-REPLAY.md",
    "replay-court/SCORE-LEDGER.md",
    "replay-court/CONSTITUTIONAL-MAP.md",
    "replay-court/REPORT-TEMPLATE.md",
    "replay-court/receipt-schema.json",
]

TELEMETRY_HEADS = [
    "artifacts/public/latest/level1-output.txt",
    "artifacts/public/latest/verifier-current-tip.txt",
    "artifacts/public/latest/oath.json",
    "replay-court/example-report/README.md",
]

STRUCTURAL_SURFACES = {
    "GAME_MECHANICS.md",
    "replay-court/SELF-AUDIT.md",
    "replay-court/VALIDATOR.md",
    "replay-court/REPAIR-LEDGER.md",
    "replay-court/CONTRADICTION-STORE.md",
    "replay-court/AUTHORITY-BOUNDS.md",
    "replay-court/WITNESS-ANCHOR.md",
    "replay-court/BOOTSTRAP-REPLAY.md",
    "replay-court/SCORE-LEDGER.md",
    "replay-court/receipt-schema.json",
}

CONTRADICTION_RE = re.compile(r"Contradiction:\s+(sha256:[a-f0-9]{64}|contradiction_[A-Za-z0-9_\-]+)\s+-\s+.+")


def run(cmd: list[str], *, default: str | None = None) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError:
        if default is not None:
            return default
        raise


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def current_witness_root() -> str:
    records: list[dict[str, str]] = []
    for p in PROTECTED_CORE_FILES:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(f"missing protected core file: {p}")
        records.append({"category": "protected_core", "file_path": p, "sha256": sha256_file(path)})
    for p in TELEMETRY_HEADS:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(f"missing telemetry head: {p}")
        records.append({"category": "telemetry_head", "file_path": p, "sha256": sha256_file(path)})
    records = sorted(records, key=lambda r: r["file_path"])
    return f"sha256:{hashlib.sha256(canonical_bytes(records)).hexdigest()}"


def changed_files() -> list[str]:
    base_sha = os.environ.get("BASE_SHA") or os.environ.get("GITHUB_BASE_SHA")
    if not base_sha:
        base_sha = run(["git", "merge-base", "HEAD", "origin/master"], default="")
    if not base_sha:
        return []
    out = run(["git", "diff", "--name-only", f"{base_sha}...HEAD"], default="")
    return [line for line in out.splitlines() if line]


def read_pr_body() -> str:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not Path(event_path).exists():
        return os.environ.get("PR_BODY", "")
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    return event.get("pull_request", {}).get("body", "") or ""


def read_pr_meta() -> dict[str, Any]:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path and Path(event_path).exists():
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
        pr = event.get("pull_request", {})
        return {
            "proposal_id": str(pr.get("number") or os.environ.get("GITHUB_REF_NAME", "local")),
            "proposer": (pr.get("user") or {}).get("login") or os.environ.get("GITHUB_ACTOR", "unknown"),
            "created_at": pr.get("created_at"),
            "updated_at": pr.get("updated_at"),
        }
    return {
        "proposal_id": os.environ.get("PR_NUMBER", "local"),
        "proposer": os.environ.get("GITHUB_ACTOR", "local"),
        "created_at": os.environ.get("PROPOSAL_CREATED_AT"),
        "updated_at": os.environ.get("PROPOSAL_UPDATED_AT"),
    }


def amendment_class(body: str, protected_changed: list[str]) -> str:
    lowered = body.lower()
    if "amendment_class: structural" in lowered or "amendment: structural" in lowered:
        return "Structural"
    if "amendment_class: operational" in lowered or "amendment: operational" in lowered:
        return "Operational"
    if "amendment_class: minor" in lowered or "amendment: minor" in lowered:
        return "Minor"
    if any(p in STRUCTURAL_SURFACES for p in protected_changed):
        return "StructuralRequiredUndeclared"
    if protected_changed:
        return "OperationalRequiredUndeclared"
    return "None"


def contradiction_present(body: str) -> bool:
    return CONTRADICTION_RE.search(body) is not None


def parse_created_at(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def main() -> int:
    violations: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    inputs_observed: list[str] = []
    inputs_unobserved: list[str] = []

    try:
        root = current_witness_root()
        inputs_observed.append("current_witness_root")
    except Exception as exc:
        root = "UNOBSERVED"
        violations.append({"type": "WITNESS_ROOT_UNOBSERVED", "evidence": str(exc)})
        inputs_unobserved.append("current_witness_root")

    files = changed_files()
    protected_changed = [f for f in files if f in PROTECTED_CORE_FILES]
    body = read_pr_body()
    meta = read_pr_meta()
    klass = amendment_class(body, protected_changed)

    if protected_changed:
        inputs_observed.append("protected_core_change_detected")
        if klass.endswith("Undeclared"):
            violations.append({"type": "AMENDMENT_CLASS_UNDECLARED", "evidence": f"protected files changed: {protected_changed}"})
    else:
        inputs_observed.append("no_protected_core_change")

    if klass in {"Operational", "Structural"} or klass.endswith("Undeclared"):
        if not contradiction_present(body):
            violations.append({"type": "CONTRADICTION_REF_MISSING", "evidence": "Operational/Structural amendments require `Contradiction: <hash> - <summary>`"})

    if klass == "Operational":
        created = parse_created_at(meta.get("created_at"))
        if created is None:
            violations.append({"type": "TIMELOCK_PUBLICATION_TIME_UNOBSERVED", "evidence": "proposal created_at unavailable; authority-bounds violation is FAIL"})
        else:
            age = (now_utc() - created).total_seconds()
            if age < OPERATIONAL_TIMELOCK_SECONDS:
                violations.append({"type": "TIMELOCK_NOT_SATISFIED", "evidence": f"Operational amendment age={int(age)}s required={OPERATIONAL_TIMELOCK_SECONDS}s"})

    if klass == "Structural":
        created = parse_created_at(meta.get("created_at"))
        if created is None:
            violations.append({"type": "TIMELOCK_PUBLICATION_TIME_UNOBSERVED", "evidence": "proposal created_at unavailable; authority-bounds violation is FAIL"})
        else:
            age = (now_utc() - created).total_seconds()
            if age < STRUCTURAL_TIMELOCK_SECONDS:
                violations.append({"type": "TIMELOCK_NOT_SATISFIED", "evidence": f"Structural amendment age={int(age)}s required={STRUCTURAL_TIMELOCK_SECONDS}s"})

    if root != "UNOBSERVED" and protected_changed:
        warnings.append({"type": "WITNESS_ROOT_CHANGED_EXPECTED", "evidence": "protected core change recomputes current root; Genesis remains baseline"})

    verdict = "FAIL" if violations else "PASS"
    result = {
        "schema_version": SCHEMA_VERSION,
        "validator": "replay_court_authority_bounds_validator",
        "genesis_witness_root": GENESIS_WITNESS_ROOT,
        "genesis_commit": GENESIS_COMMIT,
        "current_witness_root": root,
        "proposal_id": meta.get("proposal_id"),
        "proposer": meta.get("proposer"),
        "amendment_class": klass,
        "protected_core_modified": bool(protected_changed),
        "protected_core_changed_files": protected_changed,
        "inputs_observed": sorted(inputs_observed),
        "inputs_unobserved": sorted(inputs_unobserved),
        "violations": violations,
        "warnings": warnings,
        "verdict": verdict,
        "guardrails": {
            "creates_truth": False,
            "authorizes_payment": False,
            "links_settlement": False,
            "erases_history": False,
            "replaces_replay": False,
        },
    }

    out_dir = Path("validation-receipts")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"PR-{meta.get('proposal_id', 'local')}.json"
    out_path.write_bytes(canonical_bytes(result) + b"\n")
    print(json.dumps(result, sort_keys=True, indent=2))
    print(f"validation_receipt: {out_path}")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
