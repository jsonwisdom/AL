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
7. Replay-Legitimate Next Checks.
8. Boundary Rule.
9. Deep Rule.

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

Use when observable data is too sparse even for low-context classification.

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
AND forensic_status declared
AND uncertainty boundary declared
```

If any field is missing, the record is not schema-valid.

---

## Deep Rule

A forensic system must classify what evidence supports, not what a pattern tempts the observer to assert.

Low-context objects produce attribution inflation unless cognitive metadata boundaries are enforced.
