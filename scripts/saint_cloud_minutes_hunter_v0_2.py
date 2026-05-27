#!/usr/bin/env python3
"""
Saint Cloud Minutes Hunter v0.2

Rule-based, lineage-aware civic action-block extractor.

Authority: none.
LLM role: advisory only.
Merge rule: no final EVADED without replayable coordinates and confidence >= 0.85.

Output modes:
- action_blocks: full extracted action-block JSON
- contradiction_rows: one row per missing required field, with receipt hash + commit hash
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional

WATCH_PHRASES = [
    "discussion was held",
    "staff recommends",
    "authorize execution",
    "as presented",
    "various improvements",
    "related costs",
    "community needs",
    "public safety",
    "redevelopment",
    "necessary",
    "future consideration",
]

FISCAL_TRIGGERS = [
    "contract",
    "agreement",
    "change order",
    "professional services",
    "grant",
    "purchase",
    "award",
    "authorize",
]

LEGAL_TRIGGERS = ["ordinance", "resolution", "license", "zoning", "easement"]

AGENDA_ITEM_RE = re.compile(r"\b(?:item\s+)?(?P<item>\d{1,2}(?:\.[A-Z0-9]+)+|[A-Z]\.?\d+)\b", re.I)
RESOLUTION_RE = re.compile(r"\b(?:resolution|res\.)\s*(?:no\.?\s*)?(?P<id>\d{4}[-/]\d+|\d+[-/]\d{2,4})\b", re.I)
ORDINANCE_RE = re.compile(r"\b(?:ordinance|ord\.)\s*(?:no\.?\s*)?(?P<id>\d{4}[-/]\d+|\d+[-/]\d{2,4})\b", re.I)
MOTION_RE = re.compile(r"\b(?:motion|moved)\s+by\s+(?P<name>[A-Z][A-Za-z .'-]+)", re.I)
SECOND_RE = re.compile(r"\bsecond(?:ed)?\s+by\s+(?P<name>[A-Z][A-Za-z .'-]+)", re.I)
VOTE_RE = re.compile(r"\b(?P<vote>\d+\s*[-–]\s*\d+|unanimous(?:ly)?|approved|carried|passed)\b", re.I)
MONEY_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?")
DATE_RE = re.compile(r"\b(?:effective\s+)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+\d{4}\b", re.I)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

CONTRADICTION_FIELDS = [
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

EXPECTED_BY_FIELD = {
    "vote_result": "present_for_action_item",
    "motion_maker": "present_for_action_item",
    "second": "present_for_action_item",
    "resolution_number": "required_for_resolution_action",
    "ordinance_number": "required_for_ordinance_action",
    "dollar_amount": "required_for_fiscal_action",
    "effective_date": "required_for_legal_or_status_change",
}


@dataclass
class ActionBlock:
    source_doc_id: str
    source_url: Optional[str]
    source_page: Optional[int]
    source_line_number: Optional[int]
    agenda_item_id: Optional[str]
    meeting_date: Optional[str]
    text: str
    watch_phrase_hits: List[str]
    resolution_number: Optional[str]
    ordinance_number: Optional[str]
    motion_maker: Optional[str]
    second: Optional[str]
    vote_result: Optional[str]
    dollar_amounts: List[str]
    effective_date: Optional[str]
    extraction_confidence: float
    membrane_state: str
    missing_fields: List[str]


def iter_lines(path: Path) -> Iterable[tuple[Optional[int], int, str]]:
    """Yield page, line, text. Plain text uses page=1; form-feed separates pages."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    pages = raw.split("\f")
    for page_idx, page in enumerate(pages, start=1):
        for line_idx, line in enumerate(page.splitlines(), start=1):
            clean = line.strip()
            if clean:
                yield page_idx, line_idx, clean


def chunk_action_blocks(lines: Iterable[tuple[Optional[int], int, str]]) -> List[tuple[Optional[int], int, str]]:
    blocks: List[tuple[Optional[int], int, str]] = []
    current: List[str] = []
    start_page: Optional[int] = None
    start_line = 0

    def flush() -> None:
        nonlocal current, start_page, start_line
        if current:
            blocks.append((start_page, start_line, " ".join(current)))
            current = []
            start_page = None
            start_line = 0

    for page, line_no, text in lines:
        starts_new = bool(AGENDA_ITEM_RE.search(text)) or bool(re.search(r"\b(resolution|ordinance|motion|consent agenda)\b", text, re.I))
        if starts_new and current:
            flush()
        if not current:
            start_page = page
            start_line = line_no
        current.append(text)
    flush()
    return blocks


def first_group(pattern: re.Pattern[str], text: str, group: str) -> Optional[str]:
    match = pattern.search(text)
    return match.group(group).strip() if match else None


def confidence_score(text: str, source_page: Optional[int], source_line: Optional[int], present_count: int) -> float:
    coordinate_score = 0.35 if source_page is not None and source_line is not None else 0.0
    regex_score = min(0.45, present_count * 0.075)
    completeness_score = 0.20 if len(text) >= 40 else 0.05
    return round(min(1.0, coordinate_score + regex_score + completeness_score), 3)


def classify(text: str, missing: List[str], confidence: float, watch_hits: List[str]) -> str:
    has_fiscal_or_legal = any(t in text.lower() for t in FISCAL_TRIGGERS + LEGAL_TRIGGERS)
    if confidence < 0.85:
        if watch_hits and has_fiscal_or_legal:
            return "EVADED_PENDING_REVIEW"
        return "PENDING_REVIEW" if missing else "CLEAN"
    if not missing:
        return "CLEAN"
    if watch_hits and has_fiscal_or_legal:
        return "EVADED_PENDING_REVIEW"
    return "SOFTENED"


def audit_block(source_doc_id: str, source_url: Optional[str], meeting_date: Optional[str], page: Optional[int], line: int, text: str) -> ActionBlock:
    lower = text.lower()
    watch_hits = [phrase for phrase in WATCH_PHRASES if phrase in lower]
    agenda = first_group(AGENDA_ITEM_RE, text, "item")
    resolution = first_group(RESOLUTION_RE, text, "id")
    ordinance = first_group(ORDINANCE_RE, text, "id")
    motion = first_group(MOTION_RE, text, "name")
    second = first_group(SECOND_RE, text, "name")
    vote = first_group(VOTE_RE, text, "vote")
    amounts = MONEY_RE.findall(text)
    effective = DATE_RE.search(text)

    required = {
        "vote_result": vote,
        "motion_maker": motion,
        "second": second,
    }
    if "resolution" in lower:
        required["resolution_number"] = resolution
    if "ordinance" in lower:
        required["ordinance_number"] = ordinance
    if any(t in lower for t in FISCAL_TRIGGERS):
        required["dollar_amount"] = amounts[0] if amounts else None
    if any(t in lower for t in LEGAL_TRIGGERS):
        required["effective_date"] = effective.group(0) if effective else None

    missing = [k for k, v in required.items() if not v]
    present_count = len(required) - len(missing) + len(watch_hits) + (1 if agenda else 0)
    confidence = confidence_score(text, page, line, present_count)
    state = classify(text, missing, confidence, watch_hits)

    return ActionBlock(
        source_doc_id=source_doc_id,
        source_url=source_url,
        source_page=page,
        source_line_number=line,
        agenda_item_id=agenda,
        meeting_date=meeting_date,
        text=text,
        watch_phrase_hits=watch_hits,
        resolution_number=resolution,
        ordinance_number=ordinance,
        motion_maker=motion,
        second=second,
        vote_result=vote,
        dollar_amounts=amounts,
        effective_date=effective.group(0) if effective else None,
        extraction_confidence=confidence,
        membrane_state=state,
        missing_fields=missing,
    )


def receipt_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def action_to_contradiction_rows(block: ActionBlock, commit_hash: str) -> List[dict[str, object]]:
    rows: List[dict[str, object]] = []
    if not block.missing_fields:
        rows.append({
            "document_date": block.meeting_date,
            "agenda_item_id": block.agenda_item_id,
            "source_doc_id": block.source_doc_id,
            "source_url": block.source_url,
            "source_page": block.source_page,
            "source_line_number": block.source_line_number,
            "required_field": "ALL_REQUIRED_FIELDS",
            "observed_value": "present",
            "expected_value": "present",
            "classification": "COMPLIANT" if block.membrane_state == "CLEAN" else block.membrane_state,
            "extraction_confidence": block.extraction_confidence,
            "receipt_hash": receipt_hash(block.text),
            "commit_hash": commit_hash,
            "source_text_excerpt": block.text[:240],
        })
        return rows

    for field in block.missing_fields:
        rows.append({
            "document_date": block.meeting_date,
            "agenda_item_id": block.agenda_item_id,
            "source_doc_id": block.source_doc_id,
            "source_url": block.source_url,
            "source_page": block.source_page,
            "source_line_number": block.source_line_number,
            "required_field": field,
            "observed_value": None,
            "expected_value": EXPECTED_BY_FIELD.get(field, "present"),
            "classification": block.membrane_state,
            "extraction_confidence": block.extraction_confidence,
            "receipt_hash": receipt_hash(block.text),
            "commit_hash": commit_hash,
            "source_text_excerpt": block.text[:240],
        })
    return rows


def write_payload(path: Optional[Path], text: str) -> None:
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def write_csv(path: Optional[Path], rows: List[dict[str, object]]) -> None:
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = path.open("w", encoding="utf-8", newline="")
    else:
        handle = sys.stdout
    try:
        writer = csv.DictWriter(handle, fieldnames=CONTRADICTION_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    finally:
        if path:
            handle.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Saint Cloud minutes lineage hunter v0.2")
    parser.add_argument("input", type=Path, help="Plain text minutes/proceedings file. Form-feed separates pages.")
    parser.add_argument("--source-url", default=None)
    parser.add_argument("--meeting-date", default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--output-mode", choices=["action_blocks", "contradiction_rows"], default="contradiction_rows")
    parser.add_argument("--commit-hash", required=True, help="40-character commit hash binding this run")
    args = parser.parse_args()

    if not COMMIT_RE.fullmatch(args.commit_hash):
        raise SystemExit("--commit-hash must be a 40-character lowercase hex commit hash")

    blocks = chunk_action_blocks(iter_lines(args.input))
    results = [audit_block(args.input.name, args.source_url, args.meeting_date, page, line, text) for page, line, text in blocks]

    if args.output_mode == "action_blocks":
        payload = [asdict(r) for r in results]
        write_payload(args.output, json.dumps(payload, indent=2, sort_keys=True))
        return 0

    rows: List[dict[str, object]] = []
    for block in results:
        rows.extend(action_to_contradiction_rows(block, args.commit_hash))
    write_csv(args.output, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
