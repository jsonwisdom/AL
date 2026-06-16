# CONSTITUTIONAL_GRAMMAR.md

## Federation V2 Doctrine

The federation is memory without will.

It may record:

- epoch roots
- compact definitions
- bounded proofs
- predicate attestations
- deterministic rejection codes

It may not record:

- compliance verdicts
- obligation completion
- live current truth
- imperative commands
- centralized enforcement
- baseline mutation

## Inviolable Rule

> Thou shalt not encode obligation.

In Federation V2, obligations are proof-carrying predicates, not commands.

The federation may attest that proof was present at a named root.
It may not declare that an obligation was met.
It may not decide compliance.
It may not command local enforcement.

## Deterministic Rejection Vocabulary

The following failures are constitutional replay states, not commentary:

```text
LATEST_EPOCH_AMBIGUITY
UNPROVABLE_OBLIGATION_MET
UNPROVABLE_DEONTIC_STATE
PRIVILEGED_INTERPRETER_ATTEMPT
PROOF_BOUNDS_EXCEEDED
RAW_UNBOUNDED_EVIDENCE
FEDERATION_ENFORCEMENT_ATTEMPT
COMPACT_BASELINE_MUTATION_ATTEMPT
```

## Canonical Example

This field is invalid:

```json
"obligation_met": true
```

Expected runtime output:

```text
INVALID_ARTIFACT:UNPROVABLE_OBLIGATION_MET
```

This is not a moderation label.
It is a deterministic constitutional state transition.

## Replay Rule

An artifact may enter federation governance state only if it can be replayed from:

- named epoch roots
- bounded proofs
- deterministic schemas
- canonical validators

If it cannot replay, it does not constitutionally exist.

## Final Invariant

Failure output is replay state.
Not commentary.

The federation remembers.
It does not rule.
