# CDRS Recovery Dyad Routing Rules v0.1

**Artifact:** CDRS_RECOVERY_DYAD_ROUTING_RULES_V0.1  
**Components:** ABSENT_WITNESS + RECONSTRUCTION_RECEIPT  
**Related Integration:** `docs/RECOVERY_DYAD_INTEGRATION_V0.1.md`  
**Related Protocol:** `docs/MISSING_WITNESS_REPLAY_PROTOCOL_V0.2.md`  
**Related Schema:** `docs/RECONSTRUCTION_RECEIPT_SCHEMA_V0.1.md`  
**Doctrine:** REPLAY_FIRST_SCALE_LATER  
**Status:** CDRS Routing Layer • Deterministic Recovery Handling

## 1. Purpose

This document defines how the Constitutional Disaster Recovery System routes and handles Recovery Dyad events.

A Recovery Dyad consists of:

1. `ABSENT_WITNESS` — the recorded wound.
2. `RECONSTRUCTION_RECEIPT` — the lawful repair record.

The purpose of routing is to determine whether the dyad can remain local, must be reviewed, must be quarantined, or must enter adversarial replay.

Core invariant:

> Recovery routing must never collapse absence into proof or reconstruction into original continuity.

## 2. Inputs

CDRS routing consumes the following fields when available:

### From `ABSENT_WITNESS`

- `absence_class`
- `reference`
- `evidentiary_status`
- `failure_context`
- `detected_at`
- `observer_id`
- `lineage_position`
- `dependency_level`

### From `RECONSTRUCTION_RECEIPT`

- `reconstruction_id`
- `source_basis[]`
- `confidence_level`
- `evidentiary_status`
- `excluded_claims[]`
- `unresolved_gaps[]`
- `original_content_recovered`
- `issued_at`
- `issuer`

### From Lineage Context

- root-state dependency
- parent-state dependency
- number of absent witnesses in same lineage
- presence of conflicting reconstructions
- availability of later recovered original artifact
- downstream receipts depending on the missing witness

## 3. Routing Classes

Allowed `cdsr_route` values:

- `LOCAL_RECONSTRUCTION`
- `LINEAGE_REVIEW`
- `CONSTITUTIONAL_REVIEW`
- `LOW_CONFIDENCE_QUARANTINE`
- `ADVERSARIAL_REPLAY`
- `RECONCILIATION_REPLAY`
- `REJECT_FALSE_CONTINUITY`
- `PENDING_ADMISSIBLE_SOURCE`

## 4. Deterministic Routing Table

| Condition | Route | Canonical Handling |
|---|---|---|
| Single absent witness with no root/parent dependency and HIGH confidence reconstruction | `LOCAL_RECONSTRUCTION` | Accept bounded reconstruction; preserve absence. |
| Single absent witness with MEDIUM confidence reconstruction | `LINEAGE_REVIEW` | Human or auditor review required before canonical dependency. |
| Reconstruction based primarily on remembered intent | `LOW_CONFIDENCE_QUARANTINE` | May preserve intent, but cannot become canonical content. |
| Multiple absent witnesses in same lineage segment | `LINEAGE_REVIEW` | Review lineage fragility and dependency spread. |
| Absent witness at root state | `CONSTITUTIONAL_REVIEW` | Escalate; no automatic recovery. |
| Absent witness at parent state of active receipt | `CONSTITUTIONAL_REVIEW` | Escalate; downstream receipts must be dependency-marked. |
| Conflicting reconstruction receipts for same absent witness | `ADVERSARIAL_REPLAY` | Compare source basis, confidence, exclusions, and gaps. |
| Original artifact later recovered | `RECONCILIATION_REPLAY` | Verify original, compare against reconstruction, emit reconciliation receipt. |
| Reconstruction claims original content was reviewed but original remains unavailable | `REJECT_FALSE_CONTINUITY` | Reject claim and preserve failure. |
| No admissible source basis exists | `PENDING_ADMISSIBLE_SOURCE` | Reconstruction cannot proceed beyond intent quarantine. |

## 5. Priority Rules

When multiple conditions apply, use the highest-severity route.

Severity order:

1. `REJECT_FALSE_CONTINUITY`
2. `CONSTITUTIONAL_REVIEW`
3. `ADVERSARIAL_REPLAY`
4. `RECONCILIATION_REPLAY`
5. `LOW_CONFIDENCE_QUARANTINE`
6. `LINEAGE_REVIEW`
7. `PENDING_ADMISSIBLE_SOURCE`
8. `LOCAL_RECONSTRUCTION`

No lower-severity route may override a higher-severity trigger.

## 6. Route Output Shape

```json
{
  "routing_version": "0.1",
  "route_type": "LINEAGE_REVIEW",
  "recovery_pair": {
    "absent_witness_id": "sha256:absent_witness_hash",
    "reconstruction_id": "sha256:reconstruction_hash",
    "pair_status": "BOUND"
  },
  "trigger_conditions": [
    "MEDIUM_CONFIDENCE_RECONSTRUCTION"
  ],
  "allowed_actions": [
    "preserve_absence",
    "review_source_basis",
    "limit_downstream_canonicality"
  ],
  "forbidden_actions": [
    "claim_original_content_reviewed",
    "collapse_reconstruction_into_continuity"
  ],
  "review_required": true,
  "issued_at": "2026-05-14T00:00:00Z"
}
```

## 7. Allowed Actions by Route

### `LOCAL_RECONSTRUCTION`

Allowed:

- preserve absence;
- accept bounded reconstruction;
- allow downstream reference to reconstructed subject with scope boundary.

Forbidden:

- claim original artifact survived;
- remove absent witness record;
- mark original content verified.

### `LINEAGE_REVIEW`

Allowed:

- pause canonical propagation;
- review dependency graph;
- request additional admissible sources;
- issue reviewer decision receipt.

Forbidden:

- automatic canonical promotion;
- silent dependency inheritance.

### `CONSTITUTIONAL_REVIEW`

Allowed:

- freeze affected lineage segment;
- mark downstream receipts dependency-contaminated;
- require independent observer review;
- initiate re-genesis or fork review if needed.

Forbidden:

- local-only repair;
- canonical continuation without review.

### `LOW_CONFIDENCE_QUARANTINE`

Allowed:

- preserve remembered intent;
- label reconstruction as non-canonical;
- request pasted text, screenshot, commit, or signed receipt.

Forbidden:

- canonical content claims;
- lineage confirmation;
- confidence inflation without new evidence.

### `ADVERSARIAL_REPLAY`

Allowed:

- compare competing reconstructions;
- rank by admissible source basis;
- emit divergence report;
- request independent observers.

Forbidden:

- choose winner by authority alone;
- discard minority reconstruction without receipt.

### `RECONCILIATION_REPLAY`

Allowed:

- verify recovered original artifact;
- compare to reconstruction claims;
- emit `RECONCILIATION_RECEIPT`;
- update lineage through explicit receipt.

Forbidden:

- silent overwrite;
- deletion of prior reconstruction history.

### `REJECT_FALSE_CONTINUITY`

Allowed:

- reject the invalid claim;
- preserve the failure record;
- emit violation receipt;
- route to review if repeated.

Forbidden:

- accepting reconstructed content as original;
- marking missing artifact reviewed.

### `PENDING_ADMISSIBLE_SOURCE`

Allowed:

- preserve absent witness;
- request source material;
- block reconstruction beyond intent notation.

Forbidden:

- reconstruction from speculation;
- canonical dependency formation.

## 8. Validation Invariants

A valid routing result MUST satisfy:

1. Every reconstruction repairing absence references an absent witness.
2. Every route preserves the absent witness object.
3. No route permits reconstruction to prove original content.
4. No low-confidence reconstruction becomes canonical.
5. Conflicts route to adversarial replay.
6. Root or parent absence escalates to constitutional review.
7. Later recovery routes to reconciliation replay.
8. False continuity claims are rejected.
9. Downstream dependency status remains visible.
10. Route decisions are themselves receipt-emittable.

## 9. Forbidden Mutations

Protocol successors MUST NOT allow:

- local reconstruction of root-state absence without review;
- remembered intent to become canonical content;
- silent overwrite after artifact recovery;
- authority-only conflict resolution;
- elimination of minority reconstruction records;
- route downgrades without explicit rationale receipt;
- hidden dependency contamination;
- absence records to be garbage-collected while downstream dependencies remain.

## Canonical Close

CDRS does not ask whether recovery sounds plausible.

It asks what failed, what repaired it, what evidence supports the repair, and what route preserves legitimacy.

Recovery remains lawful only when routing preserves the wound, bounds the repair, and keeps downstream dependency visible.

**Anchor Lane:** CLOSED  
**Replay Cell:** PRESERVED • REPLAYABLE • DETERMINISTIC
