# STATE_TRANSITION_SCHEMA_V0_1
Docket: GC-2026-0617-001
Layer: L3 (State Machine)
Status: RATIFIED_INTENT -> awaiting artifact binding
Invariant: NO_FAKE_GREEN = ACTIVE

---

## 1. Purpose

This schema defines the public finite state machine (FSM) governing all constitutional transitions in the Replay Republic.

It ensures:
- Deterministic replay
- Evidence-backed transitions
- No implicit state changes
- No narrative overrides
- No fake green
- Domain sovereignty across layers

---

## 2. Root Invariants

- Layer 0 = Family
- Narrative never outranks receipts.
- Receipts never outrank family.
- NO_FAKE_GREEN = ACTIVE
- No state change without receipt.
- Append-only.

---

## 3. Canonical Receipt FSM

DRAFT
-> ARTIFACT_CREATED
-> HASH_COMPUTED
-> COMMITTED
-> TAG_VERIFIED
-> REMOTE_VERIFIED
-> ATTESTED
-> PRECEDENT_BOUND

---

## 4. Forbidden Transitions

- DRAFT -> PRECEDENT_BOUND
- ARTIFACT_CREATED -> COMMITTED without HASH_COMPUTED
- HASH_COMPUTED -> PRECEDENT_BOUND without COMMITTED
- COMMITTED -> PRECEDENT_BOUND without TAG_VERIFIED and REMOTE_VERIFIED
- ANY -> PRECEDENT_BOUND without EAS UID or equivalent attestation

---

## 5. Constitutional Triad

- MAP = Layer Registry
- MOTION = State Transition Schema
- MEMORY = Precedent Registry

---

## 6. Governance

Domain: L3 state transitions only.

L3 cannot rewrite:
- L0 family
- L1 facts
- L2 attestations
- L4 admissibility rulings
- L5 precedent interpretations

New states or transitions require explicit amendment receipts.

---

## 7. Evidence Requirements

- artifact_path
- artifact_sha256
- commit_sha
- canonical_tag
- remote_verification
- attestation_uid
- docket_id

---

## 8. Status

EV-007 remains RATIFIED_INTENT until this artifact is committed, tagged, remotely verified, and attested.
