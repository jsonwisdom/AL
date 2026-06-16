# ALMS-v1-SUCCESSION-MANIFEST.md

```yaml
status: CANONICAL_CANDIDATE
epoch_id: ALMS_v1
surface_role: EPOCH_CLOSURE_AND_SUCCESSION_MANIFEST
global_state: NO_DRIFT
```

## 1. Purpose

This surface:

- Closes the ALMS_v1 epoch over a complete, executable law stack.
- Freezes the v1 constitutional surfaces as immutable historical law.
- Defines the only admissible mechanisms by which ALMS_v1 may be succeeded.

No governance act may amend v1 except via succession as defined here.

## 2. Closed Surface Set for ALMS_v1

At the time of this manifest's seating, ALMS_v1 consists of:

```yaml
ALMS_v1:
  boundary: 53bffacfc9883b6e801a4bd76a953126444ee76a
  registry_charter: cb8dc80520666343653a355891257d46d53df813
  provenance_schemas: 8e4fa90ce0ecbc24b77d3241f792242bff3ef3ee
  equivalence_classes: 81409ffbffefad64cc73d724d771ef34a74b3e43
  global_state: NO_DRIFT
```

### 2.1 Closure Invariants

At epoch close:

- Identity law is defined by boundary.
- Registry law is defined by registry_charter.
- Provenance law is defined by provenance_schemas.
- Equivalence and executability law is defined by equivalence_classes.
- All referenced `class_id` values are defined, executable, and substrate-bounded.
- `global_state` for ALMS_v1 is `NO_DRIFT`.

Any claim that ALMS_v1 includes additional canonical surfaces is inadmissible.

## 3. Immutability of ALMS_v1

Once this manifest is seated:

- The commit hashes in Section 2 are constitutionally frozen for `epoch_id = ALMS_v1`.
- No canonical v1 surface may be modified in place.
- Any change to identity, registry, provenance, or equivalence law MUST occur via a new epoch.

### 3.1 Forbidden Operations inside ALMS_v1

Within ALMS_v1, it is prohibited to:

- amend canonical surfaces by replacement or patch,
- introduce shadow law that contradicts seated surfaces,
- reinterpret v1 law via non-canonical commentary.

Such attempts are jurisdictionally void and may be treated as provenance forgery.

## 4. Succession Model

Succession is the only admissible evolution path for ALMS_v1.

### 4.1 Successor Epoch Requirements

A successor epoch MUST:

- declare a new `epoch_id`, such as `ALMS_v2`,
- seat its own boundary, registry, provenance, and equivalence surfaces,
- seat its own Succession Manifest that:
  - references ALMS_v1 by `epoch_id` and the hashes in Section 2,
  - declares the succession type: `LINEAR_SUCCESSOR` or `FORKED_SUCCESSOR`.

### 4.2 Linear Successor

A `LINEAR_SUCCESSOR`:

- acknowledges ALMS_v1 as its unique direct ancestor,
- MAY deprecate or supersede v1 law, but MUST do so explicitly,
- MUST preserve the ability to:
  - verify v1 provenance,
  - interpret v1 registry decisions,
  - replay v1 equivalence judgments.

If a claimed linear successor cannot replay v1, its succession claim is inadmissible.

### 4.3 Forked Successor

A `FORKED_SUCCESSOR`:

- declares ALMS_v1 as an ancestor but limits its jurisdiction,
- MUST define fork conditions as machine-checkable predicates, not natural language,
- MUST NOT claim authority over v1 objects outside those predicates.

Fork predicates themselves are subject to provenance and equivalence law in the successor epoch.

## 5. Cross-Epoch Replay and Admissibility

### 5.1 Replay Obligations

Any successor epoch:

- MUST treat ALMS_v1 as replayable law, not advisory text,
- MUST preserve the ability to:
  - re-evaluate v1 provenance chains,
  - re-check v1 equivalence classes,
  - re-derive v1 registry standing.

### 5.2 Evidence Admissibility

In successor epochs, evidence originating in ALMS_v1 is admissible iff:

- its provenance is valid under ALMS_v1 law, and
- it is not explicitly tainted or revoked by successor law.

Successors MAY tighten admissibility.

They MUST NOT silently relax v1 constraints.

## 6. Taint, Revocation, and Sunset

### 6.1 Taint

Successor epochs MAY declare v1 objects or surfaces tainted, provided that:

- taint declarations are provenance-backed and replayable,
- taint is expressed via explicit predicates over objects or acts.

Taint affects current admissibility, not historical fact.

### 6.2 Revocation

Revocation of v1-era standing or authority:

- MUST be expressed as a successor-epoch act,
- MUST reference the specific v1 registry entries being revoked,
- MUST be replayable as a state transition.

### 6.3 Sunset

A successor MAY declare ALMS_v1 sunset, meaning:

- no new v1-native acts, such as new registry entries, are permitted,
- existing v1 acts remain replayable as historical law.

Sunset is a jurisdictional boundary, not deletion.

## 7. Verification of this Manifest

To verify that ALMS_v1 is properly closed:

- Check hashes: confirm the surface hashes match Section 2.
- Check completeness: confirm no additional canonical surfaces are claimed for ALMS_v1.
- Check executability: confirm that all referenced equivalence classes are executable and substrate-bounded under v1 law.
- Check binding: confirm this manifest is referenced wherever `epoch_id = ALMS_v1` is used in successor law.

If any check fails, claims of valid succession from ALMS_v1 are inadmissible.

## 8. Constitutional State

```yaml
epoch_id: ALMS_v1
surface_set: CLOSED
succession_status: OPEN_FOR_SUCCESSORS
global_state: NO_DRIFT
```

End of ALMS-v1-SUCCESSION-MANIFEST.md
