# First Ingestion Checklist — DOJ Epstein Public Records

State before use: `SOURCE_PENDING`

This checklist governs the first lawful transition from scaffold to ingested public-record artifact.

## 1. ACQUIRE

- Use public source only.
- Record source URL or public docket reference.
- Record retrieval timestamp in UTC.
- Do not infer completeness, alteration, withholding, or misconduct.

## 2. PLACE

- Save captured artifact bytes under:

```text
_truth/doj_epstein/sources/
```

- Do not overwrite prior captured artifacts silently.
- Use stable filenames with date or source identifier.

## 3. HASH

- Compute SHA-256 from captured bytes only.
- Do not use illustrative, placeholder, or assistant-generated hashes.
- Record byte length when available.

## 4. RECEIPT

- Copy `receipts/receipt.template.json` into a new receipt file.
- Populate only observed fields.
- Keep `verification.verdict` as `INDETERMINATE` unless replay rules produce a stronger result.
- Keep `verification.match_confirmed` false unless replay confirms parity.

## 5. MANIFEST

- Add the receipt path to a manifest that conforms to:

```text
_truth/doj_epstein/manifests/manifest.schema.json
```

- Manifest describes included receipts only.
- Manifest does not describe missing or unavailable records as evidence.

## 6. VERIFY

- Confirm source path exists.
- Confirm receipt references the captured artifact.
- Confirm SHA-256 matches captured bytes.
- Confirm neutral description does not add unsupported conclusions.

## 7. COMMIT

Commit source artifact, receipt, and manifest together only when all fields are observed.

## Non-claims

This checklist does not claim:

- a complete DOJ file set exists in this repo
- any record was withheld or altered
- any named person committed misconduct
- Amelie root exists
- Base/EAS attestation exists
- MATCH_CONFIRMED exists
