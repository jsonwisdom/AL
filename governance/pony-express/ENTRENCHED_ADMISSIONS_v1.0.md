# Entrenched Admissions Doctrine v1.0

**Location:** `governance/pony-express/ENTRENCHED_ADMISSIONS_v1.0.md`  
**Companion:** `GOVERNOR_SOURCE_RECORD_v0.1.schema.json` (EMPTY_VESSEL)  
**Branch:** `agent/pony-express-v0-1`  
**PR:** 408  
**Classification:** Frozen constitutional article  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Mass units:** EMPTY_VESSEL  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Lock the admissions posture of the Pony Express / Civic War / Moot Court pedagogical substrate so that role boundaries cannot silently expand, merge, or collapse. This document is an unamendable article for the lifetime of the simulation branch unless an explicit external promotion process (outside this PR) later supersedes it.

```text
SEPARATION_OF_DUTIES     = FROZEN
ROLE_MERGE_DETECTION     = ACTIVE
GATE_1                   = BLOCKED
VESSEL_STATUS            = EMPTY_VESSEL
EPISTEMIC_CLASS          = PENDING
MASS_BEARING_RECORD      = NONE
```

## 2. Separation of Duties (Unamendable)

The following role categories are distinct and may not be merged, collapsed, or unified by any future branch, PR, schema extension, commit path, record admission, receipt chain, or gate transition inside this simulation:

| Category | Scope |
|----------|--------|
| **Epistemic** | Source admission, byte integrity, provenance judgment |
| **Operational** | Transport, receipt emission, harness execution |
| **Governance** | Gate evaluation, role advancement, steward review |
| **Pedagogical** | Exercise design, fixture authorship, teaching hypos |

No operator, agent, or code path may:

- merge roles across categories;
- collapse reviewer categories;
- unify admission authority with verification authority;
- create hybrid operator classes that combine epistemic and governance power.

Violation triggers an immediate hard stop:

```text
exit(1)
ROLE_MERGE_DETECTED
```

This is a constitutional kill-switch, not a soft warning.

## 3. Role Merge Detection (Active)

Every commit path, schema extension, record admission, receipt chain, and gate transition is subject to role-conflation monitoring. Detection of any attempt to unify epistemic, operational, or governance roles halts processing.

```text
MONITOR_SCOPE =
  commit paths
  schema extensions
  record admissions
  receipt chains
  gate transitions

ON_DETECT → exit(1) + ROLE_MERGE_DETECTED
```

## 4. Gate 1 Posture (Locked)

Gate 1 remains **BLOCKED**. It will not open until both of the following are satisfied by an explicit operator action outside automatic promotion:

1. An operator declares the `epistemic_class` of the first record:
   - `fictional`
   - `real`
2. A primary-source verified record is admitted into the EMPTY_VESSEL schema (`GOVERNOR_SOURCE_RECORD_v0.1`).

Only after those steps may Gate 1 evaluate a byte-capture pair and determine eligibility for mass assignment. No receipt, merge, or schema presence alone satisfies Gate 1.

## 5. Two-Artifact Constitutional Substrate

This doctrine sits beside:

- `GOVERNOR_SOURCE_RECORD_v0.1.schema.json` — EMPTY_VESSEL, zero epistemic weight, all sensors UNVERIFIED / NOT_RUN.

Together they form the current constitutional substrate:

```text
Schema (empty) + Entrenched Admissions (frozen)
→ stable freeze awaiting operator admission of first record
```

## 6. Prohibited Amendments (Inside This Simulation)

```text
MERGE_EPISTEMIC_AND_GOVERNANCE     = PROHIBITED
COLLAPSE_REVIEWER_CATEGORIES       = PROHIBITED
UNIFY_ADMISSION_AND_VERIFICATION   = PROHIBITED
HYBRID_OPERATOR_CLASS              = PROHIBITED
SILENT_AUTHORITY_DRIFT             = PROHIBITED
GATE_1_OPEN_WITHOUT_DECLARATION    = PROHIBITED
MASS_ASSIGNMENT_WITHOUT_ADMISSION  = PROHIBITED
```

## 7. Valid Operator Moves (While Frozen)

The following actions remain constitutionally permissible and do not violate the freeze:

- Declare the `epistemic_class` of the first record (`fictional` | `real`)
- Provide the first primary-source record for admission
- Materialize the byte-capture pair for Gate 1 evaluation
- Define the authorized researcher role (without merging categories)
- Maintain the EMPTY_VESSEL posture indefinitely

Each move must itself respect Separation of Duties and emit receipts under the Receipt Chain Protocol (RFC 8785 JCS).

## 8. Current State

```text
ARTIFACT                 = ENTRENCHED_ADMISSIONS_v1.0
SEPARATION_OF_DUTIES     = FROZEN
ROLE_MERGE_DETECTION     = ACTIVE
GATE_1                   = BLOCKED
EPISTEMIC_CLASS          = PENDING
VESSEL_STATUS            = EMPTY_VESSEL
MASS_BEARING_RECORD      = NONE
AUTHORITY                = FALSE
HISTORICAL_VERIFICATION  = NOT_PERFORMED
CORE_DOCKET              = EMPTY
EXECUTION                = SIMULATION_ONLY
PROMOTION                = BLOCKED
```

## 9. Promotion Boundary

This document is a frozen article inside the simulation branch. Its presence on a branch or in a pull request does not make it normative outside the pedagogical substrate. Any real-world or production activation requires an explicit external promotion action separate from transport, hashing, delivery, merge status, or role advancement.
