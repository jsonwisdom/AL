# PRECHECK_SPEC_V1

## Purpose

Validate whether an ALMS artifact is already byte-stable before it is allowed to enter leaf, batch, bundle, or anchor stages.

## Rule

An artifact passes precheck when its bytes are identical to its canonical form.

For JSON and JSONL artifacts:

```bash
jq -cS . input > canonical
cmp -s input canonical && echo PRECHECK_PASS || echo PRECHECK_FAIL
```

## Meaning

- `PRECHECK_PASS` means the input file is already canonical.
- `PRECHECK_FAIL` means the file is valid JSON but not byte-canonical.
- A failed precheck is not repaired silently.
- The operator must replace the input with the canonical bytes or regenerate the artifact in canonical key order.

## Forbidden

- No anchoring after `PRECHECK_FAIL`.
- No batch ID after `PRECHECK_FAIL`.
- No semantic equivalence override.
- No manual hash substitution.
- No narrative explanation as a substitute for matching bytes.

## Doctrine

Same meaning is not enough. Same bytes are required.
