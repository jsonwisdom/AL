# ALMS-v1-ADVERSARIAL-TEST-SUITE.md

```yaml
status: CANONICAL_CANDIDATE
surface_role: ADVERSARIAL_CONSTITUTIONAL_TESTS
epoch_id: ALMS_v1
goal: prove_the_machine_refuses_unlawful_stories
global_state: NO_DRIFT
```

## 1. Purpose

This surface defines the canonical adversarial test suite for ALMS-v1.

Its purpose is not to test correctness.

Its purpose is to test constitutional refusal.

A conformant ALMS implementation MUST:

- refuse unlawful stories,
- refuse unlawful executions,
- refuse unlawful equivalence claims,
- refuse unlawful ancestry,
- and converge deterministically under replay.

This suite is the constitutional guarantee that ALMS is a hostile environment for dishonesty.

## 2. Doctrine

```text
A conformant ALMS implementation must fail predictably under adversarial pressure.
```

The question is never:

```text
Can it pass happy paths?
```

The question is:

```text
Does it refuse the exact lies the constitution says are inadmissible?
```

This suite defines those lies.

## 3. Test Object Format

Each adversarial test case MUST be expressed as:

```json
{
  "id": "ADV-XXX-YYY",
  "name": "<UPPER_SNAKE_CASE>",
  "description": "<machine-readable description>",
  "inputs": {
    "claim_or_receipt": "<path>",
    "provenance": "<path>",
    "executor_environment": "<optional>"
  },
  "expected": "<REFUSE-CODE | IDENTICAL_REPLAY_STORY_HASH>"
}
```

No natural-language interpretation is permitted.

Descriptions MUST be machine-readable.

## 4. Canonical v1 Adversarial Cases

These are the minimum required adversarial tests for ALMS-v1.

They correspond exactly to the refusal codes and replay doctrine already seated.

### 4.1 ADV-PROV-001 — MALFORMED_ANCESTRY_DAG

```yaml
id: ADV-PROV-001
name: MALFORMED_ANCESTRY_DAG
expected: REFUSE-PROV-004
```

Description:

```text
Provenance declares a cycle or impossible ancestry graph.
```

Constitutional basis:

```text
Replay Story Contract -> LINEAGE_CYCLE_DETECTED
```

### 4.2 ADV-EQ-001 — UNKNOWN_CLASS_ID

```yaml
id: ADV-EQ-001
name: UNKNOWN_CLASS_ID
expected: REFUSE-EQ-001
```

Description:

```text
Provenance references a class_id not defined in ALMS-v1 Equivalence Classes.
```

Constitutional basis:

```text
Equivalence Classes -> UNDEFINED_CLASS_IDS = PROHIBITED
```

### 4.3 ADV-EQ-002 — NATURAL_LANGUAGE_EQUIVALENCE

```yaml
id: ADV-EQ-002
name: NATURAL_LANGUAGE_EQUIVALENCE
expected: REFUSE-EQ-002
```

Description:

```text
Equivalence predicate uses natural-language semantics instead of a substrate-bounded predicate.
```

Constitutional basis:

```text
NATURAL_LANGUAGE_EQUIVALENCE = INADMISSIBLE
```

### 4.4 ADV-EXEC-001 — BLAS_SWAP

```yaml
id: ADV-EXEC-001
name: BLAS_SWAP
expected: REFUSE-EXEC-007
```

Description:

```text
Executor silently substitutes a different BLAS backend than declared.
```

Constitutional basis:

```text
Execution Contract -> backend substitution prohibited
```

### 4.5 ADV-EXEC-002 — HIDDEN_GPU_VARIANCE

```yaml
id: ADV-EXEC-002
name: HIDDEN_GPU_VARIANCE
expected: REFUSE-EXEC-008
```

Description:

```text
Executor runs on GPU hardware with undeclared feature differences such as different SM count, FP mode, or driver.
```

Constitutional basis:

```text
Execution Contract -> undeclared hardware variance prohibited
```

### 4.6 ADV-REPLAY-001 — TWO_RUNTIME_REPLAY_HASH_CONVERGENCE

```yaml
id: ADV-REPLAY-001
name: TWO_RUNTIME_REPLAY_HASH_CONVERGENCE
expected: IDENTICAL_REPLAY_STORY_HASH
```

Description:

```text
Two independent ALMS implementations replay the same claim and provenance and MUST produce identical ALMS_REPLAY_STORY_V1.replay_story_hash.
```

Constitutional basis:

```text
Replay Story Contract -> replay is deterministic, canonical, and substrate-bounded
```

## 5. Constitutional Obligations for Implementations

A conformant ALMS-v1 implementation MUST:

- run all adversarial tests,
- produce the exact refusal codes specified,
- produce no additional refusal codes,
- produce no warnings,
- produce no partial passes,
- produce no best-effort behavior,
- and produce identical replay hashes across independent runtimes.

Any deviation is a constitutional violation, not a test failure.

## 6. Constitutional State

```yaml
epoch_id: ALMS_v1
adversarial_test_suite: CLOSED
goal: prove_the_machine_refuses_unlawful_stories
global_state: NO_DRIFT
```

End of ALMS-v1-ADVERSARIAL-TEST-SUITE.md
