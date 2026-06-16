#!/usr/bin/env python3
"""ALMS Goblin Verifier v1.

Detect textual truth fracture across spelling, byte identity,
normalization, render/font traps, and container drift.
"""

import argparse
import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional

TOOL = "ALMS_GOBLIN_VERIFIER_V1"
DOCTRINE = "No byte match -> no truth"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utf8(text: str) -> bytes:
    return text.encode("utf-8")


def char_dump(text: str) -> List[Dict[str, str]]:
    return [
        {
            "char": char,
            "codepoint": f"U+{ord(char):04X}",
            "utf8_hex": utf8(char).hex(),
        }
        for char in text
    ]


def variant_row(id_: str, text: str, base_hash: str, note: str) -> Dict[str, object]:
    digest = sha256_bytes(utf8(text))
    return {
        "id": id_,
        "note": note,
        "text": text,
        "hash": digest,
        "fractured": digest != base_hash,
        "codepoints": char_dump(text),
    }


def run_verifier(base_text: str, file_path: Optional[str] = None) -> Dict[str, object]:
    base_hash = sha256_bytes(utf8(base_text))
    report: Dict[str, object] = {
        "tool": TOOL,
        "base": base_text,
        "text_hash": base_hash,
        "container_hash": None,
        "layers": {
            "L1_spelling": [],
            "L2_byte_identity": [],
            "L3_normalization": [],
            "L4_render_font": [],
            "L5_container": [],
        },
        "verdict": "PASS",
        "doctrine": DOCTRINE,
    }

    variants = {
        "L1_spelling": [
            ("spelling-behavior", "good Behavior", "Behaviour -> Behavior"),
        ],
        "L2_byte_identity": [
            ("trailing-space", base_text + " ", "Trailing space"),
            ("nbsp", base_text + "\u00A0", "Non-breaking space"),
            ("smart-quotes", "“" + base_text + "”", "Smart quotes"),
            ("straight-quotes", "\"" + base_text + "\"", "Straight quotes"),
            ("period", base_text + ".", "Added period"),
            ("lf", base_text + "\n", "LF line ending"),
            ("crlf", base_text + "\r\n", "CRLF line ending"),
        ],
        "L3_normalization": [
            ("nfc", unicodedata.normalize("NFC", base_text), "NFC normalization"),
            ("nfkc", unicodedata.normalize("NFKC", base_text), "NFKC normalization"),
            ("casefold", base_text.casefold(), "Case folding"),
            ("collapse-whitespace", " ".join("good  Behaviour".split()), "Whitespace collapse"),
            ("trim", " good Behaviour ".strip(), "Trim surrounding whitespace"),
        ],
        "L4_render_font": [
            ("ligature-fi", "good Behaﬁour", "ﬁ single glyph U+FB01"),
            ("greek-omicron", "gοοd Behaviour", "Greek omicron U+03BF vs Latin o"),
            ("dotless-i", "good Behavıour", "Dotless i U+0131 vs Latin i"),
            ("kerning-space", "good Beha viour", "Inserted visual gap"),
            ("soft-hyphen", "good Beha\u00ADviour", "Soft hyphen U+00AD"),
        ],
    }

    layers = report["layers"]
    assert isinstance(layers, dict)
    for layer, items in variants.items():
        target = layers[layer]
        assert isinstance(target, list)
        for id_, text, note in items:
            target.append(variant_row(id_, text, base_hash, note))

    if file_path:
        raw = Path(file_path).read_bytes()
        report["container_hash"] = sha256_bytes(raw)
        container_layer = layers["L5_container"]
        assert isinstance(container_layer, list)
        container_layer.append(
            {
                "id": "raw-container",
                "file": str(file_path),
                "hash": report["container_hash"],
                "note": "Full raw file-byte SHA-256",
            }
        )

    fractured = any(
        isinstance(row, dict) and bool(row.get("fractured"))
        for rows in layers.values()
        if isinstance(rows, list)
        for row in rows
    )
    report["verdict"] = "FRACTURED" if fractured else "PASS"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="ALMS Goblin Verifier v1")
    parser.add_argument("--input", default="good Behaviour", help="Base text to verify")
    parser.add_argument("--file", help="Optional file for raw container hashing")
    parser.add_argument(
        "--out",
        default="_truth/constitution/goblin_full_stack_report.json",
        help="Output JSON report path",
    )
    args = parser.parse_args()

    report = run_verifier(args.input, args.file)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
