#!/usr/bin/env python3
"""Replay Alabama Act 2025-251 from checked-in bytes only.

Doctrine: ANOMALY_LEAD_ONLY. Identify leads. Do not prove fraud.
No network fetch. No PASS flip. No public content claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CLAIM_TYPE = "ANOMALY_LEAD_ONLY"
PUBLIC_CONTENT_CLAIM = "BLOCKED_PENDING_HUMAN_REVIEW"
HASH_MATCH = "HASH_OBSERVED_MATCH"
HASH_MISMATCH = "HASH_MISMATCH"
SOURCE_MISSING = "SOURCE_BYTES_MISSING"
EXTRACTED = "EXTRACTED"
EXTRACT_BLOCKED = "EXTRACT_BLOCKED"

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def collapse_excerpt(text: str, limit: int = 420) -> str:
    return re.sub(r"\s+", " ", text).strip()[:limit]


def repo_rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_pdf_text(pdf_path: Path, out_txt: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        return EXTRACT_BLOCKED
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [pdftotext, "-layout", str(pdf_path), str(out_txt)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not out_txt.is_file() or out_txt.stat().st_size == 0:
        return EXTRACT_BLOCKED
    return EXTRACTED


def emit_lead(
    utc: str,
    lane: str,
    source_path: str,
    rule_id: str,
    severity: str,
    label: str,
    evidence: str,
) -> dict[str, Any]:
    return {
        "utc": utc,
        "lane": lane,
        "source_path": source_path,
        "rule_id": rule_id,
        "severity": severity,
        "label": label,
        "evidence_excerpt": collapse_excerpt(evidence),
        "claim_status": CLAIM_TYPE,
        "public_content_claim": PUBLIC_CONTENT_CLAIM,
        "human_review_required": True,
        "no_fake_green": True,
        "authority": False,
        "fraud_verdict": False,
    }


def scan_rules(utc: str, lane: str, source_path: str, text: str, rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    leads: list[dict[str, Any]] = []
    for rule in rules:
        pattern = rule["pattern"]
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        start = max(0, match.start() - 80)
        end = min(len(text), match.end() + 160)
        leads.append(
            emit_lead(
                utc,
                lane,
                source_path,
                rule["id"],
                rule["severity"],
                rule["label"],
                text[start:end],
            )
        )
    return leads


def evidence_chain_leads(
    utc: str,
    claim: dict[str, Any],
    hash_status: str,
    gate_text: str,
    snapshot_text: str,
    ci_al_status: str | None,
    content_rule_ids: set[str],
) -> list[dict[str, Any]]:
    leads: list[dict[str, Any]] = []
    receipt = claim.get("receipt") or {}
    replay = claim.get("replay") or {}

    if receipt.get("status") == "INDETERMINATE" or replay.get("status") == "PENDING":
        leads.append(
            emit_lead(
                utc,
                "AL",
                "fixtures/al/al_budget_2026_claim.json",
                "BBRISK_CLAIM_REPLAY_PENDING",
                "HIGH",
                "EVIDENCE_CHAIN_CLAIM_STILL_PENDING",
                (
                    f"claim.receipt.status={receipt.get('status')}; "
                    f"claim.replay.status={replay.get('status')}; "
                    f"replay_passed={receipt.get('replay_passed')}; "
                    f"notes={receipt.get('notes')}; "
                    f"pdf_hash_status={hash_status}. "
                    "Frozen PDF commit is present. This is a lead, not a PASS flip."
                ),
            )
        )

    if "OFFICIAL_SOURCE_PENDING" in snapshot_text:
        leads.append(
            emit_lead(
                utc,
                "AL",
                "fixtures/al/sources/al_budget_snapshot_2026-05-03.txt",
                "BBRISK_PLACEHOLDER_SOURCE_PENDING",
                "MEDIUM",
                "PLACEHOLDER_SNAPSHOT_STILL_PENDING",
                "Placeholder snapshot still self-declares OFFICIAL_SOURCE_PENDING while Act 2025-251 PDF bytes are checked in.",
            )
        )

    if "Hashing this placeholder would only prove" in gate_text:
        leads.append(
            emit_lead(
                utc,
                "AL",
                "docs/audit/AL_PASS_GATE.md",
                "BBRISK_GATE_DOC_STALE",
                "MEDIUM",
                "PASS_GATE_DOC_DESCRIBES_PLACEHOLDER_ONLY",
                "AL_PASS_GATE.md still describes the placeholder snapshot as the current Alabama source artifact.",
            )
        )

    if ci_al_status == "PASS":
        leads.append(
            emit_lead(
                utc,
                "AL",
                "alms/national/national_root_ci_latest.json",
                "BBRISK_CI_PASS_VS_GATE",
                "HIGH",
                "CI_AL_PASS_CONFLICTS_WITH_CLAIM_AND_GATE",
                (
                    f"national_root_ci_latest.json records AL status=PASS while the claim receipt "
                    f"is {receipt.get('status')} and replay_passed={receipt.get('replay_passed')}. "
                    "Hashable is not verified. No fraud is proven."
                ),
            )
        )

    if hash_status == HASH_MATCH and "BBRISK_LARGE_DOLLAR_AMOUNT" not in content_rule_ids:
        leads.append(
            emit_lead(
                utc,
                "AL",
                "data/boss_bre_anomaly_rules.json",
                "BBRISK_RULE_COVERAGE_GAP",
                "LOW",
                "LARGE_DOLLAR_RULE_MISSES_RAW_INTEGERS",
                (
                    "BBRISK_LARGE_DOLLAR_AMOUNT looks for '$N million/billion' language. "
                    "Act 2025-251 uses raw integers such as 84,749,919. Coverage gap only."
                ),
            )
        )

    return leads


def classify_hash(expected: str, computed: str | None, source_exists: bool) -> str:
    if not source_exists:
        return SOURCE_MISSING
    if (
        isinstance(expected, str)
        and expected.startswith("sha256:")
        and computed == expected
    ):
        return HASH_MATCH
    return HASH_MISMATCH


def write_board(path: Path, summary: dict[str, Any], leads: list[dict[str, Any]]) -> None:
    preview = json.dumps(leads[:25], indent=2)
    path.write_text(
        "\n".join(
            [
                "# Boss Bre AL Checked-In Bytes Replay Board",
                "",
                f"UTC: {summary['generated_utc']}",
                "",
                "## Status",
                "",
                f"- Scope: `{summary['scope']}`",
                f"- Source PDF: `{summary['source_pdf']}`",
                f"- PDF hash: {summary['source_pdf_sha256']}",
                f"- Claim hash: {summary['claim_hash']}",
                f"- Hash status: {summary['hash_status']}",
                f"- Extract status: {summary['extract_status']}",
                f"- Anomaly leads: {summary['lead_count']}",
                f"- HIGH: {summary['high_count']}",
                f"- MEDIUM: {summary['medium_count']}",
                f"- LOW: {summary['low_count']}",
                f"- Leads hash: {summary['leads_sha256']}",
                "",
                "## Doctrine",
                "",
                "Boss Bre publishes **audit leads**, not fraud verdicts.",
                "",
                f"- PUBLIC_CONTENT_CLAIM: {PUBLIC_CONTENT_CLAIM}",
                "- HUMAN_REVIEW_REQUIRED: TRUE",
                "- NO_FAKE_GREEN: ACTIVE",
                f"- CLAIM TYPE: {CLAIM_TYPE}",
                "- authority: false",
                "- AL PASS flipped: false",
                "- fraud_verdict: false",
                "- network_fetch: false",
                "",
                "## Latest leads",
                "",
                "```json",
                preview,
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run_replay(root: Path, outdir: Path, utc: str) -> dict[str, Any]:
    pdf_rel = Path("fixtures/al/sources/al_budget_act_2025_251.pdf")
    claim_rel = Path("fixtures/al/al_budget_2026_claim.json")
    rules_rel = Path("data/boss_bre_anomaly_rules.json")
    gate_rel = Path("docs/audit/AL_PASS_GATE.md")
    snapshot_rel = Path("fixtures/al/sources/al_budget_snapshot_2026-05-03.txt")
    ci_rel = Path("alms/national/national_root_ci_latest.json")

    pdf_path = root / pdf_rel
    claim_path = root / claim_rel
    rules_path = root / rules_rel
    outdir.mkdir(parents=True, exist_ok=True)
    extract_path = outdir / "extracted" / "al_budget_act_2025_251.pdf.txt"
    leads_path = outdir / "latest_anomaly_leads.jsonl"
    summary_path = outdir / "latest_replay_summary.json"
    board_path = outdir / "AL_CHECKED_IN_REPLAY_BOARD.md"

    if not claim_path.is_file():
        raise FileNotFoundError(f"missing claim wrapper: {claim_rel}")
    if not rules_path.is_file():
        raise FileNotFoundError(f"missing anomaly rules: {rules_rel}")

    claim = load_json(claim_path)
    rules = load_json(rules_path).get("rules") or []
    expected = claim.get("hash", "UNSET")
    source_exists = pdf_path.is_file()
    computed = sha256_file(pdf_path) if source_exists else None
    hash_status = classify_hash(expected, computed, source_exists)

    extract_status = EXTRACT_BLOCKED
    extract_sha = ""
    if source_exists:
        extract_status = extract_pdf_text(pdf_path, extract_path)
        if extract_status == EXTRACTED:
            extract_sha = sha256_file(extract_path)

    leads: list[dict[str, Any]] = []
    if hash_status == SOURCE_MISSING:
        leads.append(
            emit_lead(
                utc,
                "AL",
                str(pdf_rel),
                "BBRISK_MISSING_PAYLOAD",
                "HIGH",
                "EVIDENCE_CHAIN_BLOCKED",
                "Checked-in AL PDF bytes are missing at fixtures/al/sources/al_budget_act_2025_251.pdf",
            )
        )
    if extract_status == EXTRACT_BLOCKED:
        leads.append(
            emit_lead(
                utc,
                "AL",
                str(pdf_rel),
                "BBRISK_MISSING_PAYLOAD",
                "HIGH",
                "EVIDENCE_CHAIN_BLOCKED",
                "PDFTOTEXT_MISSING_OR_FAILED. Hash replay can still observe PDF bytes. Text leads are blocked.",
            )
        )
    elif extract_status == EXTRACTED:
        leads.extend(scan_rules(utc, "AL", repo_rel(root, extract_path), extract_path.read_text(encoding="utf-8", errors="replace"), rules))
    else:
        raise RuntimeError(f"unhandled extract_status: {extract_status}")

    gate_text = (root / gate_rel).read_text(encoding="utf-8") if (root / gate_rel).is_file() else ""
    snapshot_text = (root / snapshot_rel).read_text(encoding="utf-8") if (root / snapshot_rel).is_file() else ""
    ci_al_status = None
    if (root / ci_rel).is_file():
        ci = load_json(root / ci_rel)
        for state in ci.get("states") or []:
            if state.get("state") == "AL":
                ci_al_status = state.get("status")
                break

    content_rule_ids = {lead["rule_id"] for lead in leads}
    leads.extend(
        evidence_chain_leads(
            utc,
            claim,
            hash_status,
            gate_text,
            snapshot_text,
            ci_al_status,
            content_rule_ids,
        )
    )

    high = sum(1 for lead in leads if lead["severity"] == "HIGH")
    medium = sum(1 for lead in leads if lead["severity"] == "MEDIUM")
    low = sum(1 for lead in leads if lead["severity"] == "LOW")

    leads_body = "".join(json.dumps(lead, separators=(",", ":")) + "\n" for lead in leads)
    leads_path.write_text(leads_body, encoding="utf-8")
    leads_sha = sha256_file(leads_path)

    summary = {
        "artifact": "AL_CHECKED_IN_BYTES_REPLAY",
        "version": "0.1",
        "scope": "checked-in AL Act 2025-251 PDF bytes plus claim/gate/snapshot/CI witnesses",
        "generated_utc": utc,
        "lane": "AL",
        "authority": False,
        "verified": False,
        "status": "ANOMALY_SCAN_COMPLETE",
        "claim_type": CLAIM_TYPE,
        "public_content_claim": PUBLIC_CONTENT_CLAIM,
        "human_review_required": True,
        "no_fake_green": True,
        "network_fetch": False,
        "pass_flipped": False,
        "fraud_verdict": False,
        "al_pass_gate": "INDETERMINATE",
        "source_pdf": str(pdf_rel),
        "source_pdf_sha256": computed or "",
        "claim_hash": expected,
        "hash_match": hash_status == HASH_MATCH,
        "hash_status": hash_status,
        "extract_status": extract_status,
        "extract_path": repo_rel(root, extract_path) if extract_status == EXTRACTED else "",
        "extract_sha256": extract_sha,
        "lead_count": len(leads),
        "high_count": high,
        "medium_count": medium,
        "low_count": low,
        "leads_path": repo_rel(root, leads_path),
        "leads_sha256": leads_sha,
        "public_board_path": repo_rel(root, board_path),
        "ci_al_status_observed": ci_al_status,
        "boundary": "Lead identification only. Hash match is not PASS. Language hits are not fraud.",
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_board(board_path, summary, leads)
    return summary


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay checked-in AL bytes into anomaly leads only.")
    parser.add_argument("--root", default=None, help="Repository root. Defaults to cwd git root or cwd.")
    parser.add_argument(
        "--outdir",
        default=None,
        help="Output directory. Defaults to projects/mn-fiscal-replay/boss_bre/al_checked_in_replay",
    )
    return parser.parse_args(argv)


def resolve_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    git = shutil.which("git")
    if git:
        result = subprocess.run(
            [git, "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    return Path.cwd().resolve()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = resolve_root(args.root)
    outdir = Path(args.outdir).resolve() if args.outdir else root / "projects/mn-fiscal-replay/boss_bre/al_checked_in_replay"
    summary = run_replay(root, outdir, utc_now())
    print(json.dumps(summary, indent=2))
    print("PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW")
    print("CLAIM_TYPE: ANOMALY_LEAD_ONLY")
    print("authority: false")
    print("NO_FAKE_GREEN: ACTIVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
