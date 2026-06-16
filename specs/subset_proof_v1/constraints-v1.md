# subset_proof_v1 constraints-v1

Status: DRAFT
Issue: #180

## Core doctrine

```text
CONSTRAINTS_ARE_THE_LAW
SYNTAX_IS_THE_ENVELOPE
FORMALIZE_PROOF_BEFORE_RENDERER
```

The proof format is the public semantics layer. Renderers explain valid proofs; they do not create proof or jurisdiction.

Normative terms: MUST, MUST NOT, SHOULD, MAY follow RFC 2119 meaning.

---

## HALT constraints

### HALT-001: No added capabilities

A HALT proof MUST have `added_capabilities == []`.

Rationale: Emergency halt may reduce power immediately. It may never create power.

Testability:

```text
fixtures/subset_proof_v1/halt_valid.json MUST PASS
fixtures/subset_proof_v1/halt_invalid_added_capability.json MUST FAIL
```

### HALT-002: Post capability set is subset of pre capability set

A HALT proof MUST prove `post_capability_set ⊆ pre_capability_set`.

Testability:

```text
fixtures/subset_proof_v1/halt_valid.json MUST PASS
fixtures/subset_proof_v1/halt_invalid_not_subset.json MUST FAIL
```

### HALT-003: Halted runtime cannot express strict paths

A halted runtime MUST NOT express execution paths for strict-zone capabilities, including treasury, authority, policy, settlement, slashing, classifier upgrade, or unhalt issuance.

Testability:

```text
fixtures/subset_proof_v1/halt_invalid_strict_path_expressible.json MUST FAIL
```

### HALT-004: Partial halt forbidden by default

A strict-zone halt MUST freeze all strict domains atomically unless an explicit domain-split receipt exists under prior law.

Testability:

```text
fixtures/subset_proof_v1/halt_invalid_partial_without_domain_split_receipt.json MUST FAIL
fixtures/subset_proof_v1/halt_valid_with_domain_split_receipt.json MAY PASS if domain splits are implemented
```

### HALT-005: Halt receipt signed by active classifier

A HALT proof MUST bind a halt receipt authorized by the currently active classifier.

Testability:

```text
fixtures/subset_proof_v1/halt_invalid_missing_active_classifier_receipt.json MUST FAIL
```

---

## UNHALT constraints

### UNHALT-001: Valid receipt required

An UNHALT proof MUST include a valid receipt proving admissibility.

Testability:

```text
fixtures/subset_proof_v1/unhalt_valid.json MUST PASS
fixtures/subset_proof_v1/unhalt_invalid_missing_valid_receipt.json MUST FAIL
```

### UNHALT-002: Old classifier approval required

An UNHALT proof MUST include approval from the classifier that authorized the halt or a lawful successor authorized under that classifier.

Testability:

```text
fixtures/subset_proof_v1/unhalt_invalid_missing_old_classifier_approval.json MUST FAIL
```

### UNHALT-003: Public postmortem receipt required

An UNHALT proof MUST include a postmortem receipt describing why the halt occurred, what state was frozen, and what changed during the halt.

Testability:

```text
fixtures/subset_proof_v1/unhalt_invalid_missing_postmortem_receipt.json MUST FAIL
```

### UNHALT-004: Power may restore halted capability set

An UNHALT proof MAY restore capabilities from the halted state, but restored capabilities MUST NOT exceed the pre-halt capability set.

Testability:

```text
fixtures/subset_proof_v1/unhalt_valid.json MUST PASS
fixtures/subset_proof_v1/unhalt_invalid_new_capability.json MUST FAIL
```

### UNHALT-005: No new capabilities versus pre-halt

An UNHALT proof MUST prove `unhalt.post_capability_set - pre_halt_capability_set == []`.

Testability:

```text
fixtures/subset_proof_v1/unhalt_invalid_new_capability.json MUST FAIL
```

### UNHALT-006: Delay applies if policy sets it

If the active classifier policy requires an unhalt delay, the UNHALT proof MUST show the delay was satisfied.

Testability:

```text
fixtures/subset_proof_v1/unhalt_invalid_delay_not_satisfied.json MUST FAIL when policy requires delay
```

---

## UPGRADE_CLASSIFIER constraints

### UPGRADE-001: Old law receipts new law

A classifier upgrade MUST be a strict-zone action authorized by the currently active classifier.

Testability:

```text
fixtures/subset_proof_v1/upgrade_classifier_pending_valid.json MUST PASS
fixtures/subset_proof_v1/upgrade_classifier_invalid_no_old_law_receipt.json MUST FAIL
```

### UPGRADE-002: Strict to optimistic downgrade requires pending window

Any downgrade from strict-zone to optimistic-zone MUST enter a pending window before activation.

Testability:

```text
fixtures/subset_proof_v1/upgrade_classifier_invalid_strict_downgrade_no_pending_window.json MUST FAIL
```

### UPGRADE-003: Diff public and replayable

A classifier upgrade MUST include a public, replayable diff hash between the old policy and new policy.

Testability:

```text
fixtures/subset_proof_v1/upgrade_classifier_invalid_missing_diff_hash.json MUST FAIL
```

### UPGRADE-004: Objection window blocks activation

If an admissible objection is filed during the pending window, activation MUST halt until the objection is resolved by replay.

Testability:

```text
fixtures/subset_proof_v1/upgrade_classifier_invalid_unresolved_objection.json MUST FAIL
```

### UPGRADE-005: No self-bootstrap

A new classifier MUST NOT reduce constraints on its own upgrade path unless the old classifier lawfully authorized that reduction before activation.

Testability:

```text
fixtures/subset_proof_v1/upgrade_classifier_invalid_self_bootstrap.json MUST FAIL
```

---

## STRICT_CONTAGION constraints

### CONTAGION-001: Strict path touch upgrades action to strict

If `touched_paths ∩ strict_paths != ∅`, the derived zone MUST be STRICT.

Testability:

```text
fixtures/subset_proof_v1/strict_contagion_valid.json MUST PASS
fixtures/subset_proof_v1/strict_contagion_invalid_optimistic_treasury_touch.json MUST FAIL
```

### CONTAGION-002: Contagion is transitive

If action A calls B and B touches a strict path, A MUST derive STRICT.

Testability:

```text
fixtures/subset_proof_v1/strict_contagion_invalid_nontransitive_call.json MUST FAIL
```

### CONTAGION-003: Contagion derivation receipted

The derivation from touched paths to STRICT zone MUST be included in the action receipt.

Testability:

```text
fixtures/subset_proof_v1/strict_contagion_invalid_missing_derivation_receipt.json MUST FAIL
```

---

## OPTIMISTIC_EXECUTION constraints

### OPTIMISTIC-001: Bounded window enforced

Optimistic execution MUST enforce wall-clock, sequence-delta, and receipt-depth bounds.

Testability:

```text
fixtures/subset_proof_v1/optimistic_valid_within_window.json MUST PASS
fixtures/subset_proof_v1/optimistic_invalid_window_expired.json MUST FAIL or QUARANTINE
```

### OPTIMISTIC-002: Quarantine automatic on fail or expiry

If optimistic verification fails or the bounded window expires, quarantine MUST occur automatically before human review.

Testability:

```text
fixtures/subset_proof_v1/optimistic_expired_quarantine_valid.json MUST PASS
fixtures/subset_proof_v1/optimistic_invalid_human_override_preserves_state.json MUST FAIL
```

### OPTIMISTIC-003: Failed optimistic actions pay replay debt

Failed optimistic actions MUST charge replay debt to the actor or action source, not the system globally.

Testability:

```text
fixtures/subset_proof_v1/optimistic_invalid_no_replay_debt_charge.json MUST FAIL
```

---

## Conformance rule

```text
same proof
→ independent verifiers
→ same validity result

same valid proof
→ independent explainers
→ identical semantic interpretation
```

If independent explainers diverge, the spec is broken or an implementation is non-compliant.
