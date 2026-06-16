# Recovery Dyad Integration v0.1

**Artifact:** RECOVERY_DYAD_INTEGRATION_V0.1  
**Components:** ABSENT_WITNESS + RECONSTRUCTION_RECEIPT  
**Related Protocol:** `docs/MISSING_WITNESS_REPLAY_PROTOCOL_V0.2.md`  
**Related Schema:** `docs/RECONSTRUCTION_RECEIPT_SCHEMA_V0.1.md`  
**Doctrine:** REPLAY_FIRST_SCALE_LATER  
**Status:** Integration Layer • Receipt Machine / Replay Story Contract / CDRS Binding

## 1. Purpose

This document binds the Recovery Dyad into the broader AL / Receipt Machine recovery surface.

The dyad consists of:

1. `ABSENT_WITNESS` — records the wound.
2. `RECONSTRUCTION_RECEIPT` — records the lawful repair.

The integration rule is:

> The system must preserve the break and the repair as separate but linked constitutional objects.

## 2. Core Invariant

A reconstruction does not erase an absence.

An absence does not prove its missing contents.

The dyad preserves both:

- the failure event;
- the bounded recovery process.

Canonical invariant:

> Recovery is legitimate only when the wound remains visible and the repair remains source-bound.

## 3. Receipt Machine Binding

Any Receipt Machine object MAY include recovery references using:

```json
{
  "absent_witnesses": [
    {
      "object_type": "ABSENT_WITNESS",
      "absence_class": "DEAD_LINK",
      "reference": "https://example.invalid/share-link",
      "evidentiary_status": "NON_ADMISSIBLE",
      "failure_context": "share-link shell returned without conversation content"
    }
  ],
  "reconstruction_receipts": [
    {
      "receipt_type": "RECONSTRUCTION_RECEIPT",
      "reconstruction_id": "sha256:reconstruction_hash",
      "evidentiary_status": "RECONSTRUCTED_FROM_ADMISSIBLE_SOURCES",
      "confidence_level": "HIGH"
    }
  ]
}
```

Rules:

- `absent_witnesses[]` records missing or failed evidence.
- `reconstruction_receipts[]` records lawful recovery attempts.
- A reconstruction receipt MUST reference at least one absent witness when it is repairing a missing artifact.
- A receipt MUST NOT claim original content verification solely from a reconstruction receipt.

## 4. Replay Story Contract Binding

Replay Story Contract consumers must treat the dyad as follows:

### 4.1 Replay Treatment

- `ABSENT_WITNESS` is replayed as a failure event.
- `RECONSTRUCTION_RECEIPT` is replayed as a recovery event.
- Neither object may be silently dropped from replay history.

### 4.2 Narrative Boundary

A reconstruction may support a bounded narrative of recovery.

It may not support a claim that the original artifact survived, was reviewed, or remained continuous unless separately verified.

### 4.3 Story Contract Rule

The story may say:

> The original witness was absent; reconstruction proceeded from admissible sources.

The story may not say:

> The missing witness proved the reconstructed content.

## 5. CDRS Routing Logic

The Constitutional Disaster Recovery System must route dyad events according to severity.

### 5.1 Routing Classes

| Condition | Route |
|---|---|
| Single absent witness, low dependency | LOCAL_RECONSTRUCTION |
| Multiple absent witnesses in same lineage | LINEAGE_REVIEW |
| Absent witness at root or parent state | CONSTITUTIONAL_REVIEW |
| Reconstruction based only on remembered intent | LOW_CONFIDENCE_QUARANTINE |
| Conflicting reconstruction receipts | ADVERSARIAL_REPLAY |
| Evidence later recovered | RECONCILIATION_REPLAY |

### 5.2 CDRS Rules

- Root or parent-state absence MUST escalate.
- Low-confidence reconstruction MUST NOT become canonical without further admissible sources.
- Conflicting reconstructions MUST trigger adversarial replay.
- Later recovery of the original artifact MUST trigger reconciliation, not silent overwrite.

## 6. Atomic Pairing Rule

When a reconstruction is produced to repair a missing artifact, the recovery pair should be treated as atomic for review:

```json
{
  "recovery_pair": {
    "absent_witness_id": "sha256:absent_witness_hash",
    "reconstruction_id": "sha256:reconstruction_hash",
    "pair_status": "BOUND",
    "review_required": true
  }
}
```

Atomic does not mean merged.

The objects remain distinct.

Atomic means the system must evaluate them together when assessing recovery legitimacy.

## 7. Reconciliation Rule

If the original missing artifact is later recovered:

1. Preserve the original `ABSENT_WITNESS` event.
2. Preserve all `RECONSTRUCTION_RECEIPT` objects.
3. Verify recovered artifact independently.
4. Compare recovered content against reconstruction claims.
5. Emit `RECONCILIATION_RECEIPT`.
6. Update lineage status only through explicit receipt.

No silent correction is permitted.

## 8. Forbidden Mutations

Protocol successors MUST NOT allow:

- reconstruction receipts to overwrite absent witness records;
- absent witnesses to prove missing content;
- recovery pairs to be collapsed into continuity claims;
- later recovered artifacts to silently replace reconstruction history;
- low-confidence intent reconstructions to become canonical without new admissible evidence;
- conflicting reconstructions to coexist without adversarial replay status.

## 9. Validation Checklist

A valid Recovery Dyad integration must answer:

1. What was missing?
2. How was the absence classified?
3. What sources supported reconstruction?
4. What claims were excluded?
5. What gaps remain unresolved?
6. What confidence level was assigned?
7. Does the reconstruction preserve the original absence?
8. Does any later recovery trigger reconciliation?

## Canonical Close

`ABSENT_WITNESS` preserves the wound.

`RECONSTRUCTION_RECEIPT` preserves the repair.

`RECOVERY_DYAD_INTEGRATION` ensures the system never confuses one for the other.

Recovery does not mean pretending continuity survived.

Recovery means proving how truth was rebuilt after continuity failed.

**Anchor Lane:** CLOSED  
**Replay Cell:** PRESERVED • REPLAYABLE • DETERMINISTIC
