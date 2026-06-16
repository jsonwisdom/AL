# ALMS-v1-COURTROOM-STANDING-MATRIX.md

```yaml
status: CANONICAL_CANDIDATE_READY
surface_role: COURTROOM_ELIGIBILITY_CONSTRAINTS
epoch_id: ALMS_v1
global_state: NO_DRIFT
```

## I. Purpose

This surface defines institutional eligibility for invoking the ALMS Courtroom.

Standing is:

- not truth,
- not correctness,
- not reconstructability,
- not legitimacy,
- not epistemic authority.

Standing is eligibility to request an admissibility classification under constitutional constraints.

Standing is a gate, not a verdict.

## II. Core Doctrine

### 1. Standing Is Downstream Of Mechanical Sovereignty

Standing cannot be evaluated unless:

- provenance is valid enough to identify a claimant,
- replay can reconstruct the invocation lineage,
- execution seals are intact for the invocation context,
- refusal boundaries have not already terminated the claim.

If any upstream layer blocks evaluation, standing is unreachable.

### 2. Standing Is Eligibility, Not Entitlement

Standing does not guarantee:

- admissibility,
- institutional action,
- narrative closure,
- continuity.

Standing only grants permission to be evaluated.

### 3. Standing Is Non-Recursive

The Courtroom cannot:

- grant standing to itself,
- expand its own jurisdiction,
- create new claimant classes,
- reinterpret upstream constraints to justify standing.

This prevents self-authorizing institutions.

### 4. Standing Failures Are Terminal

If standing is insufficient, the Courtroom MUST emit one of:

```text
STANDING_INSUFFICIENT
JURISDICTION_EXCEEDED
REFUSAL_UPSTREAM
```

and terminate without synthetic closure.

No continuity fabrication.

No narrative smoothing.

### 5. Standing Cannot Cleanse Taint

Standing evaluation MUST incorporate taint classifications:

```text
TAINT_PROVENANCE
TAINT_REPLAY
TAINT_EXECUTION
TAINT_STANDING
TAINT_JURISDICTION
TAINT_UPSTREAM_REFUSAL
```

If taint intersects with standing, standing is blocked, not repaired.

This prevents:

```text
institutional eligibility -> contamination laundering
```

## III. Standing Matrix Structure

Standing is defined as a matrix, not a rule.

Each invocation is evaluated across the following dimensions.

### 1. Claimant Type

```text
operator
registry
execution_environment
provenance_anchor
external_institutional_actor
```

### 2. Claim Type

```text
admissibility_request
taint_propagation_inquiry
jurisdictional_challenge
standing_challenge
refusal_acknowledgment
```

### 3. Jurisdictional Domain

```text
provenance_domain
replay_domain
execution_domain
refusal_domain
courtroom_domain
```

### 4. Mechanical Prerequisites

Standing requires:

- reconstructable invocation lineage,
- sealed invocation context,
- no upstream refusal,
- no unresolved replay conflict.

### 5. Admissibility Pathway

If standing is satisfied, the claim proceeds to:

- admissibility classification,
- taint propagation,
- jurisdictional routing.

If standing fails, the pathway terminates.

## IV. Hard Locks

```text
NO_STANDING_EXPANSION
NO_STANDING_REPAIR
NO_STANDING_OVERRIDE
NO_STANDING_INFERENCE
NO_SELF_AUTHORIZATION
```

### NO_STANDING_EXPANSION

The Courtroom cannot create new standing categories.

### NO_STANDING_REPAIR

Standing cannot fix taint, replay ambiguity, or execution defects.

### NO_STANDING_OVERRIDE

Standing cannot override upstream refusal.

### NO_STANDING_INFERENCE

Standing cannot be inferred from context. It must be explicitly satisfied.

### NO_SELF_AUTHORIZATION

The Courtroom cannot grant itself standing or jurisdiction.

These locks prevent:

```text
institutional eligibility -> institutional sovereignty
```

## V. Termination Rule

If standing cannot be established due to:

- taint,
- replay conflict,
- reconstructability failure,
- execution defect,
- jurisdictional mismatch,
- upstream refusal,

the Courtroom MUST terminate with one of:

```text
STANDING_INSUFFICIENT
JURISDICTION_EXCEEDED
REFUSAL_UPSTREAM
RECONSTRUCTABILITY_UNAVAILABLE
REPLAY_CONFLICT_UNRESOLVED
```

No synthetic closure.

No continuity fabrication.

## VI. Final Doctrine

Standing is the eligibility firewall of the Courtroom.

It ensures:

- no self-authorizing institutions,
- no contamination laundering,
- no jurisdictional drift,
- no sovereignty recursion.

It preserves the constitutional invariant:

```text
Mechanical sovereignty constrains institutional sovereignty.
Institutional sovereignty may classify admissibility,
but may never manufacture reconstructability.
```

## VII. Constitutional State

```yaml
epoch_id: ALMS_v1
courtroom_standing_matrix: CLOSED
standing_is_eligibility_not_truth: true
standing_downstream_of_mechanical_sovereignty: true
standing_may_cleanse_taint: false
standing_may_override_refusal: false
self_authorization: prohibited
global_state: NO_DRIFT
```

End of ALMS-v1-COURTROOM-STANDING-MATRIX.md
