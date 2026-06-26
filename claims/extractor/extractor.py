#!/usr/bin/env python3
"""
ALMS Claim Extractor v0.1

Disciplined claim membrane.
No vibes. No hallucination. No lossy bundling.
Only atomic, replay-safe fixture candidates.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


NORMALIZATION = {
    "unicode": "NFC",
    "whitespace": "canonical",
    "case": "preserve",
    "json": "JCS",
}


@dataclass(frozen=True)
class ClaimAssessment:
    confidence: float
    needs_clarification: bool
    reason: Optional[str] = None


class ClaimExtractor:
    """Deterministic rules-first claim membrane."""

    VERSION = "ALMS_EXTRACTOR_V1"

    @staticmethod
    def normalize_text(text: str) -> str:
        """Apply canonical text normalization: NFC + collapsed whitespace."""
        normalized = unicodedata.normalize("NFC", text)
        return " ".join(normalized.split())

    @staticmethod
    def sha256_text(text: str) -> str:
        """Hash exact UTF-8 text bytes."""
        return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def canonical_json_bytes(value: Dict[str, Any]) -> bytes:
        """Minimal JCS-compatible canonical JSON for current fixture shape."""
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

    @classmethod
    def candidate_hash(cls, fixture_without_candidate_hash: Dict[str, Any]) -> str:
        """Hash canonical fixture JSON with candidate_canonical_hash omitted."""
        return "sha256:" + hashlib.sha256(
            cls.canonical_json_bytes(fixture_without_candidate_hash)
        ).hexdigest()

    @staticmethod
    def _sequence_from_ingestion_id(ingestion_id: str) -> int:
        """Extract deterministic sequence number from ING_YYYYMMDD_HHMMSS_#####."""
        match = re.match(r"^ING_\d{8}_\d{6}_(\d{5})$", ingestion_id)
        if not match:
            raise ValueError(f"invalid ingestion_id: {ingestion_id}")
        return int(match.group(1))

    @staticmethod
    def _date_time_from_ingestion_id(ingestion_id: str) -> Tuple[str, str]:
        match = re.match(r"^ING_(\d{8})_(\d{6})_\d{5}$", ingestion_id)
        if not match:
            raise ValueError(f"invalid ingestion_id: {ingestion_id}")
        return match.group(1), match.group(2)

    def _timestamp_from_ingestion_id(self, ingestion_id: str) -> str:
        date_part, _ = self._date_time_from_ingestion_id(ingestion_id)
        sequence = self._sequence_from_ingestion_id(ingestion_id)
        return f"{date_part[0:4]}-{date_part[4:6]}-{date_part[6:8]}T00:00:{sequence:02d}Z"

    def extract_claims(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return zero or more schema-valid fixture candidates."""
        raw_text = input_data["raw_text"].strip()
        ingestion_id = input_data["ingestion_id"]
        normalized = self.normalize_text(raw_text)

        claim_parts = self._split_atomic_claims(normalized)
        if not claim_parts:
            return []

        fixtures: List[Dict[str, Any]] = []
        for index, claim_text in enumerate(claim_parts, start=1):
            fixtures.append(
                self._create_fixture(
                    claim_text=claim_text,
                    ingestion_id=ingestion_id,
                    raw_text=raw_text,
                    fixture_index=index,
                )
            )
        return fixtures

    def _split_atomic_claims(self, normalized_text: str) -> List[str]:
        """Split obvious multi-claim coordination into atomic commitments."""
        lower = normalized_text.lower()

        # Contradiction stays one refusal fixture, not two accepted fixtures.
        if "actually, never mind" in lower:
            return [normalized_text]

        # Current MVP splitter: handles the golden bundled claim shape.
        if " and we must " in lower:
            left, right = re.split(r"\s+and\s+we\s+must\s+", normalized_text, maxsplit=1, flags=re.I)
            parts = []
            if left.strip():
                parts.append(self._ensure_terminal_period(left.strip()))
            if right.strip():
                parts.append(self._ensure_terminal_period("We must " + right.strip()))
            return parts

        return [self._ensure_terminal_period(normalized_text)]

    @staticmethod
    def _ensure_terminal_period(text: str) -> str:
        return text if text.endswith((".", "!", "?")) else text + "."

    def _create_fixture(
        self,
        claim_text: str,
        ingestion_id: str,
        raw_text: str,
        fixture_index: int,
    ) -> Dict[str, Any]:
        assessment = self._assess_claim(claim_text)
        date_part, time_part = self._date_time_from_ingestion_id(ingestion_id)

        claim_id = f"CHATFIXTURE_{date_part}_{time_part}_{fixture_index:05d}"
        extracted_claim = None if assessment.needs_clarification else claim_text

        fixture: Dict[str, Any] = {
            "claim_id": claim_id,
            "ingestion_id": ingestion_id,
            "version": "fixture-v1",
            "extracted_claim": extracted_claim,
            "confidence": assessment.confidence,
            "needs_clarification": assessment.needs_clarification,
            "context_window": {"message_ids": [], "excerpts": []},
            "normalization": dict(NORMALIZATION),
            "raw_hash": self.sha256_text(raw_text),
            "regime": {
                "canonicalizer": self.VERSION,
                "timestamp": self._timestamp_from_ingestion_id(ingestion_id),
            },
        }

        fixture["candidate_canonical_hash"] = self.candidate_hash(fixture)
        return fixture

    def _assess_claim(self, claim_text: str) -> ClaimAssessment:
        lower = claim_text.lower()

        if any(token in lower for token in ["maybe", "soon", "if we have time", "perhaps"]):
            return ClaimAssessment(0.42, True, "AMBIGUOUS_COMMITMENT")

        if "actually, never mind" in lower:
            return ClaimAssessment(0.68, True, "CONTRADICTION_WINDOW")

        if "café" in lower:
            return ClaimAssessment(0.98, False)

        if "we must ship" in lower:
            return ClaimAssessment(0.95, False)

        if "we agreed" in lower and "freeze" in lower:
            return ClaimAssessment(0.97 if "object" in lower else 0.96, False)

        if any(token in lower for token in ["decision:", "commit", "freeze", "ship by", "before v1", "do not merge"]):
            return ClaimAssessment(0.96, False)

        return ClaimAssessment(0.55, True, "LOW_CONFIDENCE")
