# CIPHER_COURT_HW25_DATA_ACQUISITION_PLAN_V1

Status: `DATA_ACQUISITION_REQUIRED`
Related:
- `CITATION.cff`
- `docs/research/README.md`
- `docs/research/CIPHER_COURT_PREREGISTRATION_V1.md`
- `schemas/cipher_court/telemetry_v1.schema.json`

## Purpose

Define the acquisition, provenance, and admissibility requirements before importing any HW 25 historical intercept data into Cipher Court.

No historical intercept may be treated as validation data until its provenance chain, archive reference, digitization status, and replay constraints are documented.

## Current Access State

```text
HW25_DIGITIZED_DATA_ACCESS = UNCONFIRMED
IMPORT_STATUS = BLOCKED
VALIDATION_STATUS = NOT_STARTED
```

Cipher Court must not fabricate ciphertext, folio references, B-Dienst baselines, convoy outcomes, or confidence records.

## Acquisition Targets

Primary target:

```text
The National Archives, UK — HW 25 series
```

Required metadata for each candidate intercept:

```json
{
  "intercept_id": "HW25/<record_id>",
  "archive_source": "TNA HW 25/<piece>, folio <folio>",
  "archive_url": null,
  "digitization_status": "UNCONFIRMED|DIGITIZED|PHYSICAL_ONLY|RESTRICTED|SEALED|PARTIAL",
  "digital_fingerprint": null,
  "transcription_status": "NOT_TRANSCRIBED|MACHINE_TRANSCRIBED|HUMAN_VERIFIED|DOUBLE_VERIFIED",
  "original_crib_used": null,
  "historical_key_or_state": null,
  "actual_outcome": null,
  "confidence_baseline": "UNKNOWN|DOCUMENTED|INFERRED",
  "provenance_notes": []
}
```

## Provenance Requirements

Each imported intercept must include:

1. Archive identifier.
2. Piece / folio reference where available.
3. Digital source URL or scan custody record.
4. SHA-256 fingerprint of the digitized source file.
5. Transcription method and verification status.
6. Historical context link to convoy or operational outcome.
7. Known missing-data flags.

## Missing Data Rules

If historical confidence is unavailable:

```text
confidence_baseline = UNKNOWN
```

Do not infer analyst confidence unless a documented method is specified.

If an intercept remains sealed or unavailable:

```text
digitization_status = SEALED or RESTRICTED
import_status = BLOCKED
```

If only partial material is available:

```text
digitization_status = PARTIAL
replay_scope = LIMITED
```

## Replay Fairness Condition

Historical validation must require cross-message consistency.

```text
ONE_MESSAGE_SUCCESS != VERDICT
TWO_MESSAGE_REPLAY_REQUIRED = TRUE
```

A candidate key or state must survive replay across the required message set.

## Validation Claims Allowed

Allowed only after provenance and replay checks:

- Construct validity tests.
- Historical benchmarking.
- Ecological face-validity analysis.
- Calibration transfer comparison.

Not allowed before acquisition:

- claims of B-Dienst baseline accuracy
- claims of modern-player superiority
- claims that Cipher Court predicts historical outcomes
- claims that a specific convoy outcome was replay-validated

## First Implementation Target

Before importing intercepts, create:

```text
data/hw25/manifest.pending.json
scripts/validate_hw25_manifest.py
```

The pending manifest should validate metadata completeness, not historical truth.

## Gate Rule

```text
NO_PROVENANCE = NO_IMPORT
NO_DIGITAL_FINGERPRINT = NO_VALIDATION
NO_REPLAY_SET = NO_VERDICT
```

## Research Position

HW 25 validation is not content expansion.

It is historical construct validation for the Cipher Court instrument.

Science is honest about missing data.
