# JSON Canonicalization Spec — LG v1

Status: normative for LG Track 001.

## Purpose

Convert JSON source payloads into deterministic bytes before hashing.

## Rule

Use RFC 8785 / JSON Canonicalization Scheme semantics unless this repository states a stricter rule.

## Required behavior

1. Parse JSON as data, not text.
2. Reject invalid JSON.
3. Sort object keys lexicographically by Unicode code point.
4. Preserve array order.
5. Emit compact JSON with no insignificant whitespace.
6. Preserve string content exactly after JSON parsing.
7. Do not delete null fields unless a source-specific normalizer explicitly says so.
8. Hash UTF-8 encoded canonical output bytes.

## Reference command

For simple JSON objects where jq behavior is acceptable for the source:

```bash
jq -cS . input.json > normalized.json
sha256sum normalized.json
```

## Boundary

If jq and RFC 8785 disagree for a source, the source registry must name a stricter implementation before ingest may run.
