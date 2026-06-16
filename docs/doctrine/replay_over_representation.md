# ALMS Doctrine — REPLAY_OVER_REPRESENTATION

Status: LOCKED  
Version: ALMS_BOUNDARY_V1  
Anchor Identity: jaywisdom.base.eth

## Doctrine Pointer

This document defines the ALMS boundary for representations, summaries, diagrams, screenshots, receipts, manifests, and other structured artifacts that describe a claim.

A representation may point to evidence, but it is not itself proof unless the underlying state can be independently replayed.

## Core Statement

Only what can be replayed can be authoritative.

## System Model

```json
{
  "doctrine": "REPLAY_OVER_REPRESENTATION",
  "version": "ALMS_BOUNDARY_V1",
  "claim": "Representations must not be treated as proof unless the underlying state can be independently replayed.",
  "representation_surfaces": [
    "summary",
    "screenshot",
    "diagram",
    "receipt",
    "manifest",
    "dashboard",
    "narrative",
    "claim_block"
  ],
  "accepted_authority": "REPLAYABLE_STATE",
  "excluded_promotions": [
    "polished_form_to_truth",
    "receipt_to_proof_without_replay",
    "screenshot_to_fact_without_source",
    "dashboard_to_authority_without_inputs",
    "manifest_to_verdict_without_reproduction"
  ],
  "replay_requirements": [
    "source_input_available_or_anchored",
    "transform_defined",
    "canonicalization_defined",
    "hash_recomputable",
    "verdict_reproducible"
  ],
  "default_state": "REPRESENTATION_ONLY",
  "promotion_path": [
    "representation",
    "source_input",
    "defined_transform",
    "canonical_state",
    "recomputed_hash",
    "replayable_verdict"
  ],
  "boundary_rules": {
    "form_is_not_truth": true,
    "clarity_is_not_verification": true,
    "receipt_without_replay_is_ritual": true,
    "dashboard_without_inputs_is_display": true,
    "authority_requires_reproduction": true
  },
  "final_statement": "A clean representation can point to truth, but only replayable state can carry authority."
}
```

## Boundary Rules

- Form is not truth.
- Clarity is not verification.
- Screenshots are not proof without source binding.
- Receipts are not proof without replay.
- Dashboards are display surfaces unless their inputs and transforms are reproducible.
- Authority requires reproduction.

## Operational Rule

```text
IF input is a representation
THEN classify as REPRESENTATION_ONLY
UNTIL source input, transform, canonicalization, and recomputed hash are available.

IF replay succeeds
THEN promote to REPLAYABLE_VERDICT.

IF replay fails or cannot be performed
THEN remain REPRESENTATION_ONLY.
```

## Integrity Check

```text
STATUS: PASS
NO_FORM_AUTHORITY
NO_RECEIPT_AUTHORITY_WITHOUT_REPLAY
NO_SCREENSHOT_AUTHORITY_WITHOUT_SOURCE
NO_DASHBOARD_AUTHORITY_WITHOUT_INPUTS
REPLAY_REQUIRED
```

## Triad Fit

```text
SIGNAL_BEFORE_PROOF              -> no premature elevation
NO_ELEVATION_NO_ATTRIBUTION      -> no unproven agency
REPLAY_OVER_REPRESENTATION       -> no unreplayable authority
```

## One-Liner

Representation points. Replay proves.

Verification > Narrative
