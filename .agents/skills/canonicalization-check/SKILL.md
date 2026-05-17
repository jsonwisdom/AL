# Canonicalization Check Skill

## Purpose
Verify deterministic normalization and hashing behavior across replay environments.

## Use When
- Adding new fixtures.
- Expanding replay matrices.
- Testing Unicode, newline, or serialization edge cases.

## Never Do
- Never hash unnormalized Unicode.
- Never rely on implicit locale or encoding behavior.
- Never silently change canonicalization rules.

## Required Inputs
- Canonical fixture string.
- Expected normalization form.
- Expected SHA-256 root.

## Allowed Outputs
- NFC_CONFIRMED
- UTF8_CONFIRMED
- ROUND_TRIP_PASS
- CANONICALIZATION_DRIFT
- ROOT_MISMATCH

## Verification Command
```bash
python3 src/matrix_runner.py
```

## Receipt Path
- `docs/forensic/`

## Failure Condition
Reject replay settlement if normalized bytes diverge across witnesses.

## Constitutional Rule
The membrane settles normalized bytes, not visual glyph appearance.
