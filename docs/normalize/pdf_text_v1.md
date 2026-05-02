# PDF to Text Normalization Spec — LG v1

Status: normative for LG Track 001 PDF sources.

## Purpose

Convert PDF source payloads into deterministic UTF-8 text before hashing.

## Required behavior

1. Extract text using a deterministic toolchain (e.g., pdftotext -layout -nopgbrk).
2. Normalize Unicode to NFC.
3. Remove form feed characters.
4. Preserve reading order as emitted by the extractor.
5. Collapse runs of spaces and tabs to one space.
6. Collapse three or more blank lines to two newlines.
7. Trim leading and trailing whitespace.
8. Emit UTF-8 text bytes ending with exactly one newline.

## Hash boundary

Hash only the normalized text bytes.

## Forbidden behavior

- Do not include file metadata (creation date, producer) in normalized text.
- Do not reorder paragraphs.
- Do not apply OCR unless declared and versioned in this spec.
