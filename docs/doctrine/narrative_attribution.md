# ALMS Doctrine — NARRATIVE_ATTRIBUTION

Status: LOCKED  
Version: ALMS_BOUNDARY_V1  
Anchor Identity: jaywisdom.base.eth

## Doctrine Pointer

This document defines the ALMS boundary for misattributed agency in verification systems.

ALMS artifacts are not persons, personalities, communities, belief systems, or social actors. They are deterministic publication surfaces composed of files, commits, hashes, receipts, pointers, and replayable artifacts.

## Core Statement

Narrative may attribute agency. ALMS accepts only state transitions.

## System Model

```json
{
  "doctrine": "NARRATIVE_ATTRIBUTION",
  "version": "ALMS_BOUNDARY_V1",
  "claim": "Verification artifacts must not be treated as agents, authorities, or social actors.",
  "misattribution_risk": {
    "source": "social_layer_interpretation",
    "failure_mode": "artifact_treated_as_actor",
    "result": "narrative_inflation"
  },
  "alms_objects": [
    "repo",
    "commit",
    "receipt",
    "pointer",
    "hash",
    "reproducible_artifact"
  ],
  "excluded_interpretations": [
    "persona",
    "belief_system",
    "coordinated_actor",
    "epistemic_authority",
    "social_protocol"
  ],
  "accepted_classification": "DETERMINISTIC_PUBLICATION_SURFACE",
  "boundary_rules": {
    "artifacts_do_not_intend": true,
    "receipts_do_not_believe": true,
    "hashes_do_not_argue": true,
    "commits_record_state": true,
    "proof_requires_replay": true
  },
  "promotion_rule": "AGENCY_CLAIM_REQUIRES_EXTERNAL_PROOF",
  "default_state": "NARRATIVE_POINTER_ONLY",
  "final_statement": "A receipt is not a speaker. A commit is not a belief. A hash is not authority. Only replayable artifacts survive verification."
}
```

## Boundary Rules

- A receipt is not a person.
- A hash is not authority.
- A commit records state; it does not imply intent.
- ENS can anchor identity, but it does not convert artifacts into agency.
- Social interpretation remains narrative until externally proven.

## Operational Rule

```text
IF interpretation attributes intent, personality, coordination, or authority to an ALMS artifact
THEN classify as NARRATIVE_POINTER_ONLY
UNLESS independently supported by reproducible external proof.
```

## Integrity Check

```text
STATUS: PASS
NO_PERSONIFICATION
NO_AUTHORITY_INFLATION
NO_SOCIAL_LAYER_LEAKAGE
STATE_TRANSITIONS_ONLY
ARTIFACTS_NOT_ACTORS
```

## One-Liner

Narrative sees actors. ALMS sees artifacts.

Verification > Narrative
