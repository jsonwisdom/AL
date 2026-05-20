# CONTENTCOIN_FORENSIC_RECORD_SCHEMA_V1

**Schema ID:** `CONTENTCOIN_FORENSIC_RECORD_SCHEMA_V1`  
**Status:** `DRAFT_LOCKED`  
**Class:** `EVIDENCE_BOUNDED_FORENSIC_SCHEMA`  
**Operator:** `jaywisdom.base.eth`  

---

## Invariant

A ContentCoin forensic record may classify only what the observable evidence can support.

Sparse metadata does not prove malicious origin.

Low attestation does not prove coordinated farming.

Every attribution must be bounded by receipts, observable surfaces, and explicitly stated uncertainty.

---

## Schema Invariant Block

### CLAIM_BOUNDARY_ENFORCEMENT_V1

If the analyst cannot complete the supported/unsupported claim split, the record MUST remain `INSUFFICIENT_EVIDENCE`.

No inference may be promoted into attribution.

No classification may exceed its evidentiary surface.

A forensic record may not:

- assert identity without identity evidence.
- assert coordination without cluster evidence.
- assert intent without behavioral evidence.
- assert farm attribution without multi-signal confirmation.
- assert narrative origin without narrative binding.
- assert lineage without traceable funding, deployer, or receipt continuity.

If any required support is absent, the record must preserve:

```json
{
  "forensic_status": "INSUFFICIENT_EVIDENCE"
}
```

This is not a fallback state.

This is the default constitutional state when evidence is incomplete.

### INSUFFICIENT_EVIDENCE_REFUSAL_FLOW_V1

The forensic engine MUST execute the following refusal flow before any attribution is promoted:

```text
OBSERVABLE_SURFACE
→ CLAIM_EXTRACTION
→ SUPPORTED_CLAIMS_LIST
→ UNSUPPORTED_CLAIMS_LIST
→ CLAIM_BOUNDARY_CHECK
→ ATTRIBUTION_GATE
```

The attribution gate is lawful only if:

```text
supported_claims is complete
AND unsupported_claims is complete
AND every promoted attribution maps to at least one supported claim
AND no promoted attribution depends on an unsupported claim
```

If this condition fails, the engine MUST set:

```json
{
  "classification": "INSUFFICIENT_EVIDENCE",
  "forensic_status": "INSUFFICIENT_EVIDENCE",
  "attribution_promotion": "REFUSED"
}
```

This flow prevents:

- narrative inflation.
- epistemic drift.
- adversarial overreach.
- false certainty.
- farm-attribution hallucination.
- identity misbinding.

### ATTRIBUTION_PROMOTION_RULE_V1

A record may promote attribution only when the evidence type matches the claim type.

```text
identity claim → identity evidence required
coordination claim → cluster evidence required
intent claim → behavior evidence required
farm claim → multi-signal confirmation required
narrative-origin claim → narrative binding required
lineage claim → deployer, funding, or receipt continuity required
```

If the evidence type does not match the claim type, the attribution is schema-invalid.

---

## Canonical Record Object

```json
{
  "contentcoin_forensic_record": {
    "record_id": "string",
    "schema_id": "CONTENTCOIN_FORENSIC_RECORD_SCHEMA_V1",
    "network": "Base",
    "contract_address": "0x...",
    "zora_page_ref": "string | null",
    "referrer_address": "0x... | null",
    "observed_surface_label": "string | null",
    "record_status": "EVIDENCE_BOUNDED_PRELIMINARY | UPDATED | FINALIZED | SUPERSEDED",
    "classification": "LOW_CONTEXT_CONTENTCOIN | ATTESTED_CREATOR_COIN | FACTORY_PATTERN_CONFIRMED | FARM_ATTRIBUTION_CONFIRMED | INSUFFICIENT_EVIDENCE",
    "narrative_binding": "NONE | WEAK | MODERATE | STRONG",
    "identity_binding": "UNVERIFIED | WEAK | PROFILE_LINKED | WALLET_ATTESTED | STRONG",
    "replay_meaningfulness": "LOW | MODERATE | HIGH",
    "metadata_density": "EMPTY | SPARSE | PARTIAL | RICH",
    "lineage_confidence": "UNKNOWN | UNCONFIRMED_FACTORY_PATTERN | BYTECODE_MATCH_CONFIRMED | DEPLOYER_CLUSTER_CONFIRMED",
    "risk_flags": [],
    "supported_claims": [],
    "unsupported_claims": [],
    "claim_boundary_check": "PASSED | FAILED",
    "attribution_promotion": "ALLOWED | REFUSED",
    "required_next_checks": [],
    "forensic_status": "string",
    "cognitive_metadata_density": {
      "identity_binding": "number | null",
      "narrative_binding": "number | null",
      "media_binding": "number | null",
      "lineage_visibility": "number | null",
      "attestation_depth": "number | null",
      "creator_continuity": "number | null",
      "replay_context": "number | null"
    }
  }
}
```

---

## Required Boundary Sections

Every record must include:

1. Constitutional Correction, if prior over-attribution occurred.
2. Deterministic Classification.
3. Evidence-Bounded Interpretation.
4. Supported Claims.
5. Unsupported Claims.
6. Cognitive Metadata Deficiency analysis.
7. Claim Boundary Check.
8. Attribution Promotion Decision.
9. Replay-Legitimate Next Checks.
10. Boundary Rule.
11. Deep Rule.

---

## Classification Rules

### LOW_CONTEXT_CONTENTCOIN

Use when metadata, identity, narrative, and provenance surfaces are sparse or weak, but stronger attribution is not supported.

### FACTORY_PATTERN_CONFIRMED

Use only after bytecode equivalence, factory event, or deployment trace confirms factory lineage.

### FARM_ATTRIBUTION_CONFIRMED

Use only after multiple independent checks support coordinated farming, such as deployer cluster, holder graph, funding lineage, timing cluster, and economic pattern evidence.

### ATTESTED_CREATOR_COIN

Use when creator identity, media, narrative, and provenance surfaces are sufficiently bound.

### INSUFFICIENT_EVIDENCE

Use when observable data is too sparse even for low-context classification, or when the supported/unsupported claim split cannot be completed.

---

## Forbidden Attribution

The following are forbidden without supporting evidence:

- Confirmed farm attribution from metadata absence alone.
- Malicious intent from sparse provenance alone.
- Sybil cluster attribution from referrer reuse alone.
- Deceptive deployment attribution from factory pattern alone.
- Creator invalidity from missing profile alone.

---

## Cognitive Metadata Density Inputs

```json
{
  "CMD": "COGNITIVE_METADATA_DENSITY",
  "inputs": [
    "identity_binding",
    "narrative_binding",
    "media_binding",
    "lineage_visibility",
    "attestation_depth",
    "creator_continuity",
    "replay_context"
  ]
}
```

---

## Replay-Legitimate Next Checks

- Holder graph analysis.
- Deploy timing cluster check.
- Bytecode equivalence test.
- Funding lineage trace.
- Mint entropy analysis.
- Referrer behavior comparison.
- Creator/profile metadata refresh check.

---

## Validation Rule

```text
record_id exists
AND contract_address exists
AND classification declared
AND supported_claims declared
AND unsupported_claims declared
AND claim_boundary_check declared
AND attribution_promotion declared
AND forensic_status declared
AND uncertainty boundary declared
AND CLAIM_BOUNDARY_ENFORCEMENT_V1 satisfied
AND INSUFFICIENT_EVIDENCE_REFUSAL_FLOW_V1 satisfied
```

If any field is missing, the record is not schema-valid.

If the supported/unsupported claim split is incomplete, the record must remain `INSUFFICIENT_EVIDENCE`.

If attribution promotion is refused, the classification must not exceed `INSUFFICIENT_EVIDENCE` unless new evidence is added and the record is updated.

---

## Deep Rule

A forensic system must classify what evidence supports, not what a pattern tempts the observer to assert.

Low-context objects produce attribution inflation unless cognitive metadata boundaries are enforced.
