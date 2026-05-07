# FAILURE_SURFACE_MAP_V1

## Purpose

Map each adversarial federation V2 failure surface to the exact artifact fields or structures that trigger deterministic rejection.

---

## 1. LATEST_EPOCH_AMBIGUITY

### Trigger Surface

```json
"latest_epoch": true
```

### Expected Output

```text
INVALID_ARTIFACT:LATEST_EPOCH_AMBIGUITY
```

### Constitutional Reason

Queries and compacts must bind to explicit replay roots.
"latest" is not replayable.

---

## 2. UNPROVABLE_OBLIGATION_MET

### Trigger Surface

```json
"obligation_met": true
```

### Expected Output

```text
INVALID_ARTIFACT:UNPROVABLE_OBLIGATION_MET
```

### Constitutional Reason

Federation may attest proof presence only.
Compliance verdicts are forbidden.

---

## 3. UNPROVABLE_DEONTIC_STATE

### Trigger Surface

```json
"action": "MUST_REDUCE_WITHDRAWALS"
```

### Expected Output

```text
INVALID_ARTIFACT:UNPROVABLE_DEONTIC_STATE
```

### Constitutional Reason

Federation cannot derive mandatory obligations from predicates.
Enforcement remains local to sovereign runtimes.

---

## 4. PRIVILEGED_INTERPRETER_ATTEMPT

### Trigger Surface

Any structure requiring federation-side semantic interpretation beyond deterministic replay.

### Expected Output

```text
INVALID_ARTIFACT:PRIVILEGED_INTERPRETER_ATTEMPT
```

### Constitutional Reason

No federation component may gain interpretive supremacy.

---

## 5. PROOF_BOUNDS_EXCEEDED

### Trigger Surface

Any string field exceeding bounded replay limits.

### Expected Output

```text
INVALID_ARTIFACT:PROOF_BOUNDS_EXCEEDED
```

### Constitutional Reason

Replay cost must remain bounded.
Semantic laundering through oversized proofs is forbidden.

---

## 6. RAW_UNBOUNDED_EVIDENCE

### Trigger Surface

```json
"proof": "RAW_EVIDENCE_BLOB"
```

### Expected Output

```text
INVALID_ARTIFACT:RAW_UNBOUNDED_EVIDENCE
```

### Constitutional Reason

Evidence must be typed, hashed, and bounded.
Raw unbounded evidence is non-replayable.

---

## 7. FEDERATION_ENFORCEMENT_ATTEMPT

### Trigger Surface

```json
"federation_verdict": "COMPLIANT"
```

### Expected Output

```text
INVALID_ARTIFACT:FEDERATION_ENFORCEMENT_ATTEMPT
```

### Constitutional Reason

Federation may not command, enforce, or adjudicate.
It may only attest.

---

## 8. COMPACT_BASELINE_MUTATION_ATTEMPT

### Trigger Surface

Any compact structure implying rewrite, rebase, or mutation of participant baselines.

### Expected Output

```text
INVALID_ARTIFACT:COMPACT_BASELINE_MUTATION_ATTEMPT
```

### Constitutional Reason

Federation dependencies may not rewrite sovereign baselines.

---

## Final Invariant

Failure output is replay state.
Not commentary.
