# ALMS-v1-COURTROOM-ADMISSIBILITY-VOCABULARY.md

```yaml
status: CANONICAL_CANDIDATE
surface_role: COURTROOM_SPEECH_CONSTRAINT
epoch_id: ALMS_v1
global_state: NO_DRIFT
```

## I. Purpose

This surface defines the complete and closed vocabulary the ALMS Courtroom may use when classifying institutional admissibility.

It does not define powers.

It defines speech boundaries.

The Courtroom may classify admissibility.

The Courtroom may not generate epistemic authority.

This vocabulary is intentionally finite, non-generative, and non-interpretive.

## II. Canonical Verdict Classes

Each verdict class is a classification, not a truth claim.

Each is downstream of mechanically sovereign layers.

### 1. ADMISSIBLE

```yaml
class: ADMISSIBLE
type: permission_classification
meaning: all upstream mechanical constraints are satisfied
```

### 2. INADMISSIBLE

```yaml
class: INADMISSIBLE
type: authority_refusal
meaning: one or more upstream constraints block institutional action
```

### 3. TAINTED

```yaml
class: TAINTED
type: caution_classification
meaning: lineage contamination or partial reconstructability
```

### 4. JURISDICTION_EXCEEDED

```yaml
class: JURISDICTION_EXCEEDED
type: boundary_classification
meaning: the courtroom is not the correct institutional venue
```

### 5. STANDING_INSUFFICIENT

```yaml
class: STANDING_INSUFFICIENT
type: eligibility_classification
meaning: claimant lacks constitutional standing
```

### 6. RECONSTRUCTABILITY_UNAVAILABLE

```yaml
class: RECONSTRUCTABILITY_UNAVAILABLE
type: mechanical_block
meaning: replay cannot reconstruct the claim
```

### 7. REPLAY_CONFLICT_UNRESOLVED

```yaml
class: REPLAY_CONFLICT_UNRESOLVED
type: mechanical_conflict
meaning: replay yields divergent or conflicting outcomes
```

### 8. REFUSAL_UPSTREAM

```yaml
class: REFUSAL_UPSTREAM
type: subordinate_acknowledgment
meaning: a lower layer has already refused; the courtroom must not override
```

These eight classes form the complete admissibility vocabulary.

No additional verdict classes may be created without constitutional amendment.

## III. Hard Speech Locks

The Courtroom is constitutionally forbidden from emitting:

```text
NO_TRUTH_VERDICTS
NO_FACT_CREATION
NO_CONFIDENCE_LANGUAGE
NO_PROBABILITY_LANGUAGE
NO_NARRATIVE_CLOSURE
NO_EQUIVALENCE_CREATION
NO_RECONSTRUCTABILITY_IMPLICATION
```

### NO_TRUTH_VERDICTS

No verdict may imply truth, correctness, or reality alignment.

### NO_FACT_CREATION

No verdict may imply creation, discovery, or assertion of facts.

### NO_CONFIDENCE_LANGUAGE

No confidence, certainty, likelihood, or strength language.

### NO_PROBABILITY_LANGUAGE

No probabilistic or statistical framing.

### NO_NARRATIVE_CLOSURE

No synthetic continuity, coherence, or story-completion language.

### NO_EQUIVALENCE_CREATION

No declaration of equivalence between claims, states, or lineages.

### NO_RECONSTRUCTABILITY_IMPLICATION

No verdict may imply reconstructability unless replay has already established it.

These locks ensure the Courtroom cannot drift into epistemic authority.

## IV. Downstream-Only Semantics

The Courtroom may reference:

- replay outcomes
- execution seals
- provenance lineage
- refusal states
- taint propagation
- jurisdictional boundaries

The Courtroom may not reinterpret, soften, or renegotiate any of them.

This enforces the invariant:

```text
The courtroom inherits constraints.
It does not renegotiate them.
```

## V. Termination Without Closure

The Courtroom may lawfully terminate proceedings with any refusal-class verdict.

No synthetic closure.

No narrative smoothing.

No institutional improvisation.

This encodes the doctrine:

```text
Constitutional integrity > institutional continuity
```

## VI. Non-Recursive Sovereignty Guarantee

No admissibility verdict may:

- imply truth
- imply reconstructability
- imply equivalence
- imply sealing integrity
- imply provenance validity
- imply reality alignment

This prevents sovereignty recursion, the historical corruption vector.

## VII. Final Doctrine

The Courtroom's vocabulary is a speech cage, not a truth engine.

It can classify admissibility.

It cannot generate epistemic authority.

This preserves the constitutional firewall:

```text
Mechanical sovereignty constrains institutional sovereignty.
Institutional sovereignty may classify admissibility,
but may never manufacture reconstructability.
```

## VIII. Constitutional State

```yaml
epoch_id: ALMS_v1
courtroom_admissibility_vocabulary: CLOSED
canonical_verdict_classes: 8
speech_locks: ACTIVE
non_recursive_sovereignty: true
global_state: NO_DRIFT
```

End of ALMS-v1-COURTROOM-ADMISSIBILITY-VOCABULARY.md
