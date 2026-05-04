#!/usr/bin/env python3
"""
ALMS Hardened Receipt Generator

Generates an ALMS PDF receipt representation and SHA256 sidecar.
Boundary: this PDF is a representation until the source artifacts are committed.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

RECEIPTS_DIR = Path("_truth/receipts")
PDF_PATH = RECEIPTS_DIR / "ALMS_RUN_001.pdf"
SHA_PATH = RECEIPTS_DIR / "ALMS_RUN_001.pdf.sha256"

CANONICAL_ROOT = "e1fbf116972f368c13fab67ef479e0b839b080ff"
SEAL_COMMIT = "afbbd791e66bc78d27e0fc4a329eb2e8bf54780a"
GENERATED_AT_UTC = os.environ.get("ALMS_GENERATED_AT_UTC", "2026-05-05T04:55:00Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def draw_line(c: canvas.Canvas, text: str, y: int, font: str = "Helvetica", size: int = 10) -> int:
    c.setFont(font, size)
    c.drawString(50, y, text)
    return y - 16


def generate_receipt_pdf(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=letter)
    c.setTitle("ALMS RUN RECEIPT 001")
    c.setSubject("ALMS hardened PDF receipt representation")
    c.setAuthor("Jay Wisdom / jsonwisdom")
    c.setKeywords(["ALMS", "receipt", "canonical_root", CANONICAL_ROOT, "seal", SEAL_COMMIT])

    y = 750
    y = draw_line(c, "ALMS RUN RECEIPT — 001 (HARDENED)", y, "Helvetica-Bold", 16)
    y -= 14
    y = draw_line(c, f"Generated: {GENERATED_AT_UTC}", y)
    y = draw_line(c, f"Canonical root: {CANONICAL_ROOT}", y)
    y = draw_line(c, f"Seal commit: {SEAL_COMMIT}", y)
    y -= 14

    y = draw_line(c, "Claim Boundary", y, "Helvetica-Bold", 12)
    y = draw_line(c, "HASH_MISMATCH proves byte/artifact drift only.", y)
    y = draw_line(c, "Intent, narrative tampering, and malice require independent evidence.", y)
    y -= 14

    y = draw_line(c, "Doctrine", y, "Helvetica-Bold", 12)
    y = draw_line(c, "Proof > vibes. Run the receipt.", y)
    y -= 14

    y = draw_line(c, "Artifact Status", y, "Helvetica-Bold", 12)
    y = draw_line(c, "- fisa702.pdf: NOT YET COMMITTED", y)
    y = draw_line(c, "- fisa702_extracted.txt: NOT YET COMMITTED", y)
    y = draw_line(c, "- fisa702_diff.txt: NOT YET COMMITTED", y)
    y -= 14

    y = draw_line(c, "Representation Warning", y, "Helvetica-Bold", 12)
    y = draw_line(c, "This PDF is a REPRESENTATION, not the source truth.", y, "Helvetica-Oblique", 9)
    y = draw_line(c, "Full closed-loop replay requires committed source artifacts.", y, "Helvetica-Oblique", 9)

    c.showPage()
    c.save()


def main() -> int:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    generate_receipt_pdf(PDF_PATH)
    digest = sha256_file(PDF_PATH)
    SHA_PATH.write_text(f"{digest}  {PDF_PATH.name}\n", encoding="utf-8")
    print(f"Generated: {PDF_PATH}")
    print(f"Manifest:  {SHA_PATH}")
    print(f"SHA256:    {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
