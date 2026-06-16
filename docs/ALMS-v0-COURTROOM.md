# ALMS v0 Courtroom

## Purpose

ALMS Courtroom defines constitutional adjudication over verified receipt state.

The Courtroom does not replace PROVENANCE, REGISTRY, or EXECUTION. It consumes their deterministic outputs and converts them into institutional posture.

The courtroom answers:

```text
Given a technically verified receipt, what does it mean?
```

## Stack Role

```text
PROVENANCE -> is the chain intact?
REGISTRY   -> does the chain have jurisdiction?
EXECUTION  -> does the chain replay deterministically?
COURTROOM  -> what verdict may be spoken?
```

## Admissibility vs Persuasiveness

### Admissibility

Admissibility is binary.

A receipt is admissible only if:

- PROVENANCE: lineage is intact.
- REGISTRY: jurisdiction is valid.
- EXECUTION: replay is deterministic.
- SIGNATURE: cryptographic binding holds.
- SCHEMA: output conforms.
- ENTROPY: covert channel budget is respected.

Admissibility is not interpretation, trust, vibes, or policy preference.

It is a machine-checkable fact.

### Persuasiveness

Persuasiveness is not binary.

It is evidentiary weight assigned by the courtroom based on:

- taint level,
- conflict status,
- recency,
- constitutional version,
- revocation proximity,
- quorum strength,
- execution environment trustworthiness.

Persuasiveness is where governance lives.

Admissibility is where physics lives.

## Taint

Taint is contextual legitimacy loss.

Taint is not corruption.

A receipt can be admissible and tainted.

### Taint Sources

A receipt becomes tainted if:

- any ancestor is tainted,
- any ancestor is revoked,
- any ancestor is constitutionally superseded,
- execution environment is marked `TAINTED`,
- replay disagreement occurred,
- registry quorum changed mid-chain,
- constitution version changed mid-chain,
- key status was close to revocation boundary.

### Taint Propagation

Taint propagates monotonically upward:

```text
tainted(R) = local_taint(R) OR any(tainted(P) for P in Parents(R))
```

Taint never self-clears.

Taint is removed only by re-issuance under a clean chain.

## Taint Lattice

ALMS v0 defines this minimal taint lattice:

```text
CLEAN < WATCH < TAINTED < CONFLICTED < REFUSED
```

Meanings:

- `CLEAN`: no known taint.
- `WATCH`: admissible, but close to a boundary such as revocation proximity or quorum transition.
- `TAINTED`: admissible, but legitimacy weight is reduced.
- `CONFLICTED`: admissible receipts disagree or occupy a jurisdictional fork.
- `REFUSED`: courtroom refuses to issue a substantive verdict.

Transitions are monotonic within an adjudication context.

## Conflict Resolution

A conflict occurs when two or more admissible receipts:

- share the same `input_hash`,
- share the same `model_id` or declared semantic task identity,
- produce different outputs,
- and each passes EXECUTION determinism under its own `exec_env_hash`.

This is not a replay mismatch.

This is a jurisdictional fork.

### Conflict Set

When conflict is detected:

```text
conflict_set = {R1, R2, ...}
```

Courtroom rules:

- All receipts in the conflict set remain admissible if lower layers passed.
- All receipts in the conflict set become non-persuasive by default.
- Courtroom must issue deterministic refusal unless a governing constitution defines a deterministic tie-breaker.
- Registry SHOULD mark conflicting `exec_env_hash` values as `TAINTED` pending review.

This prevents dueling truths from being silently accepted.

## Deterministic Refusal Doctrine

Refusal is not failure.

Refusal is constitutional discipline.

The courtroom MUST refuse to issue a substantive verdict when:

- admissibility is false,
- taint level exceeds policy threshold,
- conflict set is non-empty,
- registry quorum is unstable,
- constitution version is in transition,
- execution environment is tainted beyond threshold,
- revocation window is active,
- required evidence is unavailable.

## Refusal Receipt

A refusal is itself a receipt.

Minimum structure:

```json
{
  "object": "ALMS_COURTROOM_REFUSAL_V0",
  "courtroom_verdict": "REFUSAL",
  "reason": "CONFLICT_SET_NONEMPTY",
  "conflict_hashes": ["<receipt_hash>"],
  "timestamp": "<iso8601>",
  "signature": "<signature>"
}
```

Refusals are first-class evidence.

## Refusal Taxonomy

ALMS v0 refusal reasons:

```text
ADMISSIBILITY_FALSE
TAINT_THRESHOLD_EXCEEDED
CONFLICT_SET_NONEMPTY
REGISTRY_QUORUM_UNSTABLE
CONSTITUTION_TRANSITION_ACTIVE
EXEC_ENV_TAINTED
REVOCATION_WINDOW_ACTIVE
EVIDENCE_UNAVAILABLE
```

## Evidentiary Weight

For admissible receipts, persuasiveness is computed as evidentiary weight.

```text
weight(R) = f(
  taint(R),
  constitution_version(R),
  exec_env_trust(R),
  registry_quorum(R),
  recency(R)
)
```

`f` MUST satisfy:

- monotonic decreasing in taint,
- monotonic increasing in quorum strength,
- monotonic decreasing in execution environment distrust,
- monotonic decreasing across constitution supersession,
- monotonic decreasing with age unless constitution says otherwise.

The courtroom does not guess.

It computes.

## Verdict Classes

ALMS v0 courtroom verdicts:

```text
ADMISSIBLE_CLEAN
ADMISSIBLE_TAINTED
ADMISSIBLE_CONFLICTED
REFUSAL
INADMISSIBLE
SUPERSEDED
```

Meanings:

- `ADMISSIBLE_CLEAN`: receipt passes all lower layers and no courtroom taint applies.
- `ADMISSIBLE_TAINTED`: receipt passes lower layers but carries contextual legitimacy loss.
- `ADMISSIBLE_CONFLICTED`: receipt is part of a conflict set.
- `REFUSAL`: courtroom refuses substantive verdict under deterministic doctrine.
- `INADMISSIBLE`: one or more lower-layer checks failed.
- `SUPERSEDED`: receipt remains historically visible but is no longer current under registry or constitution rules.

## Algorithm Sketch

```text
courtroom_evaluate(R):
  lower = verify_lower_layers(R)

  if lower.admissible == false:
    return INADMISSIBLE

  taint = compute_taint(R)
  conflicts = find_conflict_set(R)

  if conflicts.non_empty:
    return REFUSAL(reason=CONFLICT_SET_NONEMPTY)

  if taint > policy.taint_threshold:
    return REFUSAL(reason=TAINT_THRESHOLD_EXCEEDED)

  if registry.quorum_unstable:
    return REFUSAL(reason=REGISTRY_QUORUM_UNSTABLE)

  if constitution.transition_active:
    return REFUSAL(reason=CONSTITUTION_TRANSITION_ACTIVE)

  weight = compute_weight(R)

  if taint == CLEAN:
    return ADMISSIBLE_CLEAN(weight)

  return ADMISSIBLE_TAINTED(weight, taint)
```

## Security Meaning

A valid receipt is not automatically persuasive.

A tainted receipt is not automatically false.

A conflict is not a permission slip to pick a favorite answer.

A refusal is not weakness.

Courtroom is the layer where deterministic verification becomes governance posture without corrupting the lower layers.

## Recommended Conformance Directory

```text
alms-v0-conformance/v7_courtroom/
```

Recommended fixtures:

```text
admissible_clean.json
admissible_tainted_parent.json
conflict_set_two_receipts.json
refusal_conflict_set_nonempty.json
refusal_taint_threshold_exceeded.json
superseded_receipt.json
```
