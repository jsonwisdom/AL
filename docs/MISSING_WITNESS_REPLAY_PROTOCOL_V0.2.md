# Missing Witness Replay Protocol v0.2

**Artifact:** MISSING_WITNESS_REPLAY_PROTOCOL_V0.2  
**Classification:** Recovery Primitive • Absent Artifact Governance  
**Doctrine:** REPLAY_FIRST_SCALE_LATER  
**Status:** Constitutional Recovery Rule • First-Class AL / Receipt Machine Primitive

## Purpose

This protocol governs absent artifacts, dead links, deleted chats, corrupted receipts, inaccessible evidence, and unavailable witnesses.

The protocol prevents a missing artifact from being falsely elevated into evidence, lineage, or continuity.

Core invariant:

> Missing artifacts do not authorize hallucinated continuity. They authorize disciplined reconstruction.

This aligns with the civilizational axiom:

> Truth does not need to remain unbroken. Truth must remain reconstructable.

## 1. Absence Classification

The system must first determine what kind of absence occurred. This prevents accidental elevation of a missing artifact into an evidentiary object.

Allowed absence classes:

- `DEAD_LINK` — URL resolves but content surface is empty.
- `INACCESSIBLE_PAGE` — authentication, permission, or sandbox boundary prevents access.
- `DELETED_ARTIFACT` — intentionally removed or no longer retrievable.
- `CORRUPTED_FILE` — bytes present but non-parseable or integrity-invalid.
- `UNAVAILABLE_WITNESS` — referenced witness or artifact not present.
- `NON_VERIFIABLE_CLAIM` — assertion without admissible evidence.

This classification is itself an admissible fact.

The missing artifact is not.

## 2. Reject False Continuity

The system must not fabricate continuity from absence.

Forbidden operations:

- pretending the artifact was reviewed;
- inventing contents;
- inferring lineage from unavailable material;
- asserting continuity based on missing material;
- propagating assumed truth;
- treating a wrapper, shell, or reference as if it contained the missing content.

Constitutional firewall:

> absence is not evidence, and absence is not continuity.

## 3. Preserve the Failure

The absence itself becomes a recorded, immutable event.

Record the following when available:

- `ABSENT_WITNESS` classification;
- URL, hash, name, or reference identifier;
- observation timestamp;
- evidentiary status: `NON_ADMISSIBLE`;
- failure context, such as `share-link shell returned without content`;
- observer identifier or system component that detected the absence.

This creates a stable, replayable failure object without granting the missing artifact evidentiary authority.

## 4. Reconstruct Only From Admissible Sources

Reconstruction must be grounded in actual evidence, not the missing artifact.

Valid reconstruction sources:

- pasted text;
- screenshots;
- repository commits;
- signed receipts;
- canonical lineage objects;
- hashes with retrievable preimages;
- remembered intent explicitly labeled as reconstruction.

Invalid reconstruction sources:

- speculation;
- invented continuity;
- unverifiable claims;
- assumptions about what the artifact probably said;
- inaccessible wrappers treated as content.

Core invariant:

> Reconstruction is lawful only when its basis is admissible.

## 5. Emit Reconstruction Receipt

Every reconstruction must produce a receipt documenting:

- `source_basis` — what admissible evidence was used;
- `confidence_level` — high, medium, or low;
- `excluded_claims` — what cannot be asserted;
- `unresolved_gaps` — what remains unknown;
- `next_admissible_action` — paste, screenshot, fetch, restore, or proceed with reconstruction;
- `reconstruction_scope` — what is reconstructed and what is not;
- `observer_signature` when available.

This receipt prevents reconstruction from mutating into false continuity.

## 6. Evidentiary Status Rules

A missing artifact may receive only the following statuses:

- `NON_ADMISSIBLE`
- `ABSENT_WITNESS_RECORDED`
- `RECONSTRUCTION_REQUIRED`
- `RECONSTRUCTED_FROM_ADMISSIBLE_SOURCES`

A missing artifact MUST NOT receive:

- `VERIFIED`
- `CANONICAL`
- `LINEAGE_CONFIRMED`
- `CONTENT_REVIEWED`
- `ADMISSIBLE_SOURCE`

unless the original content is later recovered and independently verified.

## 7. Integration Surfaces

This protocol integrates with:

- AL lineage;
- Receipt Machine;
- Replay Story Contract;
- Recovery Lattice;
- Merkle Reconstruction Frame;
- Constitutional Disaster Recovery System;
- schema and validation surfaces;
- litigation and evidentiary review workflows.

## 8. Example Failure Context

Scenario:

A shared chat link resolves only to a generic wrapper, login shell, navigation surface, or expired page. The conversation body is not present.

Correct classification:

```json
{
  "object_type": "ABSENT_WITNESS",
  "absence_class": "DEAD_LINK",
  "evidentiary_status": "NON_ADMISSIBLE",
  "failure_context": "share-link shell returned without conversation content",
  "continuity_claim_allowed": false,
  "reconstruction_allowed": true
}
```

Required conclusion:

> The link is evidence only of failed retrieval, not evidence of the missing conversation.

## 9. Forbidden Mutations

Protocol successors MUST NOT introduce rules that allow:

- assumed contents from absent artifacts;
- lineage confirmation without retrievable evidence;
- canonical status based only on memory;
- wrapper metadata treated as content;
- missing links treated as proof of prior claims;
- reconstruction without source-basis disclosure;
- confidence inflation without admissible evidence.

## Canonical Close

A missing witness is not a broken truth.

It is a recovery obligation.

The system does not hallucinate continuity.

The system records absence, preserves the failure, and reconstructs only from admissible sources.

**Anchor Lane:** CLOSED  
**Replay Cell:** PRESERVED • REPLAYABLE • DETERMINISTIC
