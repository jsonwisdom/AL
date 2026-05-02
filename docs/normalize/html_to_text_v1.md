# HTML to Text Normalization Spec — LG v1

Status: normative for LG Track 001 HTML sources.

## Purpose

Convert HTML source payloads into deterministic UTF-8 text before hashing.

## Required behavior

1. Fetch raw response bytes.
2. Decode as UTF-8 unless source-specific headers require another declared encoding.
3. Remove script, style, noscript, and SVG blocks.
4. Strip HTML tags after preserving block boundaries.
5. Decode HTML entities.
6. Normalize Unicode to NFC.
7. Collapse runs of spaces and tabs to one space.
8. Collapse three or more blank lines to two newlines.
9. Trim leading and trailing whitespace.
10. Emit UTF-8 text bytes ending with exactly one newline.

## Hash boundary

Hash only the normalized text bytes.

## Forbidden behavior

- Do not include crawl timestamp in normalized text.
- Do not include request headers in normalized text.
- Do not reorder page content.
- Do not silently drop visible text unless this spec is versioned.
