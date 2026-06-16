# ALMS-v1-COURTROOM-STACK.md

```yaml
status: CANONICAL_CANDIDATE_READY
surface_role: COURTROOM_CLOSURE_INDEX
epoch_id: ALMS_v1
global_state: NO_DRIFT
```

## I. Purpose

This surface binds the ALMS-v1 courtroom surfaces into a closed institutional subsystem.

It establishes:

- the courtroom's complete authority set,
- the courtroom's complete speech set,
- the courtroom's complete contamination rules,
- the courtroom's complete eligibility rules,
- the courtroom's complete consequence mappings,

and declares that no additional courtroom authority exists in ALMS-v1.

This is the Courtroom's closure index.

## II. Courtroom Surface Index

The ALMS-v1 Courtroom consists only of the following canonical surfaces.

### 1. Courtroom Contract

```yaml
path: docs/ALMS-v1-COURTROOM-CONTRACT.md
commit_sha: 24e9d2af3d4dab7af7e7c13ebd860e5db7088054
role: authority_boundaries_and_prohibitions
```

Defines authority boundaries and prohibitions.

### 2. Courtroom Admissibility Vocabulary

```yaml
path: docs/ALMS-v1-COURTROOM-ADMISSIBILITY-VOCABULARY.md
commit_sha: 4896f4d3ef4200dacd9c79e88ed61ce641ca751f
role: complete_and_closed_speech_set
```

Defines the Courtroom's complete and closed speech set.

### 3. Courtroom Taint Propagation

```yaml
path: docs/ALMS-v1-COURTROOM-TAINT-PROPAGATION.md
commit_sha: 32029df73e99a12f659c9fb136f168a13c5c2d87
role: contamination_flow_and_downstream_taint_constraints
```

Defines contamination flow and downstream taint constraints.

### 4. Courtroom Standing Matrix

```yaml
path: docs/ALMS-v1-COURTROOM-STANDING-MATRIX.md
commit_sha: f3c32b8c792e8ab882c0423aeedfd5f95db12afc
role: eligibility_jurisdiction_and_non_self_authorization
```

Defines eligibility, jurisdiction, and non-self-authorization rules.

### 5. Courtroom Institutional Consequences

```yaml
path: docs/ALMS-v1-COURTROOM-INSTITUTIONAL-CONSEQUENCES.md
commit_sha: 2f88a893581fbbc8732d1b59f2a1249fd2caa17d
role: downstream_institutional_posture_mapping
```

Defines downstream institutional posture mapping.

These five surfaces constitute the entire Courtroom domain for ALMS-v1.

## III. Closure Doctrine

### 1. The Courtroom Is Closed Over These Five Surfaces

No additional courtroom powers, speech, or authority exist in ALMS-v1.

### 2. No Implicit Courtroom Authority

No surface outside this index may grant the Courtroom:

- new powers,
- new speech,
- new verdicts,
- new jurisdiction,
- new consequences.

### 3. No Recursive Expansion

The Courtroom may not:

- expand itself,
- reinterpret its own boundaries,
- create new authority surfaces,
- or modify upstream sovereignty.

### 4. No Cross-Surface Override

None of the five courtroom surfaces may override or reinterpret another.

They form a mutually constraining set.

### 5. No Drift

All courtroom behavior MUST remain within the constraints of these five surfaces.

## IV. Amendment Rule

### 1. No New Courtroom Authority May Be Added In ALMS-v1

Any expansion requires:

- a successor epoch, ALMS-v2 or later,
- or an explicit constitutional amendment.

### 2. Amendments Must Be Upstream-Compatible

No amendment may:

- weaken mechanical sovereignty,
- introduce recursion,
- grant epistemic authority,
- allow truth creation,
- manufacture reconstructability,
- or expand institutional action beyond admissibility posture.

### 3. Amendments Must Be Explicit

No implicit or emergent authority is permitted.

## V. Final Doctrine

The Courtroom is a sealed institutional subsystem within ALMS-v1.

It is:

- downstream-only,
- mechanically constrained,
- non-truth-generating,
- non-self-authorizing,
- refusal-compatible,
- and constitutionally incapable of expanding its own domain.

This closure surface ensures:

```text
Mechanical sovereignty constrains institutional sovereignty.
Institutional sovereignty constrains institutional action.
No recursion. No laundering. No inflation.
```

## VI. Constitutional State

```yaml
epoch_id: ALMS_v1
courtroom_stack: CLOSED
canonical_courtroom_surfaces: 5
implicit_courtroom_authority: prohibited
recursive_expansion: prohibited
cross_surface_override: prohibited
global_state: NO_DRIFT
```

End of ALMS-v1-COURTROOM-STACK.md
