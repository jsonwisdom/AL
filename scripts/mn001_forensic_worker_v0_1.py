#!/usr/bin/env python3
"""
MN001 forensic worker v0.1

Purpose:
  Convert MN_001 from "diff detected" into a sentence-level forensic package.

Doctrine:
  - NO_FAKE_GREEN active.
  - If normalized source payloads are missing, emit a blocked receipt.
  - Never promote PUBLIC_CONTENT_CLAIM from this script.

Outputs under projects/mn-fiscal-replay/live_fetch/MN_001/:
  - MN_001_sentence_level.diff
  - MN_001_sentence_review.json
  - MN_001_delta_classification.md
  - MN_001_forensic_receipt.json
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

ROOT = Path.cwd()
MN_DIR = ROOT / "projects" / "mn-fiscal-replay" / "live_fetch" / "MN_001"

BASELINE_CANDIDATES = [
    MN_DIR / "MN_001_baseline_normalized.txt",
    MN_DIR / "baseline_normalized.txt",
    MN_DIR / "baseline.txt",
    MN_DIR / "normalized_baseline.txt",
]
LIVE_CANDIDATES = [
    MN_DIR / "MN_001_live_normalized.txt",
    MN_DIR / "MN_001_current_normalized.txt",
    MN_DIR / "live_normalized.txt",
    MN_DIR / "current_normalized.txt",
    MN_DIR / "normalized_live.txt",
]

SENTENCE_DIFF = MN_DIR / "MN_001_sentence_level.diff"
REVIEW_JSON = MN_DIR / "MN_001_sentence_review.json"
CLASSIFICATION_MD = MN_DIR / "MN_001_delta_classification.md"
FORENSIC_RECEIPT = MN_DIR / "MN_001_forensic_receipt.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def first_existing(paths: Iterable[Path]) -> Optional[Path]:
    for path in paths:
        if path.exists() and path.is_file() and path.stat().st_size > 0:
            return path
    return None


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sentence_split(text: str) -> List[str]:
    text = normalize_space(text)
    if not text:
        return []
    # Split after terminal punctuation followed by likely next sentence.
    # Also preserve semicolon-heavy budget prose by keeping long fragments intact.
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9$])", text)
    return [p.strip() for p in pieces if p.strip()]


def has_money_or_number_change(a: str, b: str) -> bool:
    money = re.compile(r"\$?\b\d[\d,]*(?:\.\d+)?\s*(?:million|billion|thousand|percent|%)?\b", re.I)
    return money.findall(a) != money.findall(b)


def substantive_terms_changed(a: str, b: str) -> bool:
    terms = [
        "appropriation", "budget", "forecast", "deficit", "surplus", "fund",
        "agency", "program", "revenue", "spending", "obligation", "fiscal",
        "FY", "2024", "2025", "2026", "2027", "2028", "2029",
    ]
    al = a.lower()
    bl = b.lower()
    return any((t.lower() in al) != (t.lower() in bl) for t in terms)


def classify_pair(removed: str, added: str) -> str:
    r = normalize_space(removed)
    a = normalize_space(added)
    if not r and a:
        if has_money_or_number_change("", a) or substantive_terms_changed("", a):
            return "POSSIBLE_CONTENT_DELTA"
        return "NORMALIZATION_ARTIFACT"
    if r and not a:
        if has_money_or_number_change(r, "") or substantive_terms_changed(r, ""):
            return "POSSIBLE_CONTENT_DELTA"
        return "NORMALIZATION_ARTIFACT"
    if r == a:
        return "ORDER_ONLY"
    if normalize_space(r).lower() == normalize_space(a).lower():
        return "NORMALIZATION_ARTIFACT"
    if re.sub(r"[^A-Za-z0-9$%]+", "", r).lower() == re.sub(r"[^A-Za-z0-9$%]+", "", a).lower():
        return "NORMALIZATION_ARTIFACT"
    if has_money_or_number_change(r, a) or substantive_terms_changed(r, a):
        return "POSSIBLE_CONTENT_DELTA"
    return "EXTRACTOR_ARTIFACT"


@dataclass
class ReviewItem:
    index: int
    tag: str
    baseline_sentence: str
    live_sentence: str
    baseline_sha256: str
    live_sha256: str


def build_review(baseline_sentences: List[str], live_sentences: List[str]) -> List[ReviewItem]:
    matcher = difflib.SequenceMatcher(a=baseline_sentences, b=live_sentences, autojunk=False)
    review: List[ReviewItem] = []
    idx = 1
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        removed = baseline_sentences[i1:i2]
        added = live_sentences[j1:j2]
        max_len = max(len(removed), len(added))
        for k in range(max_len):
            r = removed[k] if k < len(removed) else ""
            a = added[k] if k < len(added) else ""
            label = classify_pair(r, a)
            review.append(
                ReviewItem(
                    index=idx,
                    tag=label,
                    baseline_sentence=r,
                    live_sentence=a,
                    baseline_sha256=sha256_text(r) if r else "",
                    live_sha256=sha256_text(a) if a else "",
                )
            )
            idx += 1
    return review


def write_blocked(reason: str, baseline_path: Optional[Path], live_path: Optional[Path]) -> int:
    MN_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "MN_001_FORENSIC_RECEIPT_V0_1",
        "timestamp": utc_now(),
        "status": "BLOCKED",
        "blocked_reason": reason,
        "public_content_claim": "BLOCKED",
        "no_fake_green": True,
        "baseline_path": str(baseline_path) if baseline_path else None,
        "live_path": str(live_path) if live_path else None,
        "required_inputs": [
            "baseline normalized text",
            "live/current normalized text",
        ],
    }
    FORENSIC_RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 1


def main() -> int:
    baseline_path = first_existing(BASELINE_CANDIDATES)
    live_path = first_existing(LIVE_CANDIDATES)
    if not baseline_path or not live_path:
        return write_blocked(
            "FORENSIC_PAYLOAD_MISSING: normalized baseline/live text files not found",
            baseline_path,
            live_path,
        )

    baseline_text = read_text(baseline_path)
    live_text = read_text(live_path)
    baseline_sentences = sentence_split(baseline_text)
    live_sentences = sentence_split(live_text)
    review = build_review(baseline_sentences, live_sentences)

    diff_lines = list(
        difflib.unified_diff(
            baseline_sentences,
            live_sentences,
            fromfile=str(baseline_path),
            tofile=str(live_path),
            lineterm="",
        )
    )
    SENTENCE_DIFF.write_text("\n".join(diff_lines) + "\n", encoding="utf-8")

    review_payload = {
        "schema": "MN_001_SENTENCE_REVIEW_V0_1",
        "timestamp": utc_now(),
        "status": "SENTENCE_REVIEW_COMPLETE" if review else "NO_SENTENCE_DIFF_DETECTED",
        "public_content_claim": "BLOCKED",
        "no_fake_green": True,
        "baseline_path": str(baseline_path),
        "live_path": str(live_path),
        "baseline_sha256": sha256_file(baseline_path),
        "live_sha256": sha256_file(live_path),
        "baseline_sentence_count": len(baseline_sentences),
        "live_sentence_count": len(live_sentences),
        "diff_item_count": len(review),
        "classification_counts": {},
        "items": [asdict(item) for item in review],
    }
    for item in review:
        review_payload["classification_counts"][item.tag] = review_payload["classification_counts"].get(item.tag, 0) + 1
    REVIEW_JSON.write_text(json.dumps(review_payload, indent=2) + "\n", encoding="utf-8")

    md = [
        "# MN_001 Delta Classification v0.1",
        "",
        "NO_FAKE_GREEN: active.",
        "PUBLIC_CONTENT_CLAIM: BLOCKED.",
        "",
        f"Baseline: `{baseline_path}`",
        f"Live: `{live_path}`",
        "",
        "| # | Tag | Baseline | Live |",
        "|---:|---|---|---|",
    ]
    for item in review:
        b = item.baseline_sentence.replace("|", "\\|")[:500]
        l = item.live_sentence.replace("|", "\\|")[:500]
        md.append(f"| {item.index} | `{item.tag}` | {b} | {l} |")
    CLASSIFICATION_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    receipt = {
        "schema": "MN_001_FORENSIC_RECEIPT_V0_1",
        "timestamp": utc_now(),
        "status": "FORENSIC_PACKAGE_GENERATED",
        "public_content_claim": "BLOCKED",
        "promotion_gate": "HUMAN_REVIEW_REQUIRED",
        "no_fake_green": True,
        "outputs": {
            str(SENTENCE_DIFF): sha256_file(SENTENCE_DIFF),
            str(REVIEW_JSON): sha256_file(REVIEW_JSON),
            str(CLASSIFICATION_MD): sha256_file(CLASSIFICATION_MD),
        },
        "classification_counts": review_payload["classification_counts"],
    }
    FORENSIC_RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
