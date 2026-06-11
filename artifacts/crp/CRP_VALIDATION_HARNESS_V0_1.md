# CRP_VALIDATION_HARNESS_V0_1

_validation harness execution design — authority: false, semantic_change: false_

## 1. Purpose and Scope

The CRP Validation Harness V0.1 defines how the CRP Validation Suite V0.1 may be executed deterministically against Git-backed implementation artifacts.

The harness exists to:

- execute validation checks described by the validation suite
- load versioned fixtures
- isolate test execution
- produce machine-readable non-authoritative reports
- preserve GREEN, YELLOW, and RED result semantics

The harness does not:

- certify truth
- grant authority
- mutate CRP artifacts
- reinterpret validation results
- convert test success into constitutional proof

Execution reports conformance observations only.

---

## 2. Binding Receipt

This harness binds to the Git-backed validation suite:

```json
{
  "artifact": "CRP_VALIDATION_SUITE_V0_1",
  "repo": "jsonwisdom/AL",
  "path": "artifacts/crp/CRP_VALIDATION_SUITE_V0_1.md",
  "commit": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696",
  "authority": false,
  "semantic_change": false
}
```

This binding does not imply that any test has already run.

---

## 3. Harness Constitutional Boundary

```json
{
  "harness_role": "deterministic_test_executor",
  "input": "CRP_VALIDATION_SUITE_V0_1",
  "output": "validation_report",
  "authority": false,
  "semantic_change": false,
  "certification": false,
  "truth_claim": false
}
```

The harness may execute tests.
The harness may produce reports.
The harness may not declare the CRP stack verified.

---

## 4. Test Runner Model

The test runner must be deterministic.

Required runner properties:

- single explicit test manifest
- stable test ordering
- isolated test execution
- no hidden network calls unless explicitly declared as input
- no clock-dependent verdicts
- no random ordering
- no environment-dependent pass/fail behavior

Runner input envelope:

```json
{
  "harness_version": "0.1",
  "suite_commit": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696",
  "test_manifest_id": "<manifest-id>",
  "fixture_set_id": "<fixture-set-id>",
  "authority": false,
  "semantic_change": false
}
```

---

## 5. Fixture Management

Fixtures are deterministic inputs used by the harness.

Fixture rules:

- every fixture has a stable `fixture_id`
- every fixture has a content hash
- every fixture declares its target layer
- every fixture declares expected result class when applicable
- fixture mutation requires a new fixture ID or version

Fixture envelope:

```json
{
  "fixture_id": "fixture_entry_valid_001",
  "fixture_version": "0.1",
  "target_layer": "ENTRY",
  "payload_hash": "sha256:<hash>",
  "expected_status": "GREEN | YELLOW | RED",
  "authority": false,
  "semantic_change": false
}
```

Fixture categories:

- valid schema fixtures
- invalid schema fixtures
- API envelope fixtures
- forbidden authority-language fixtures
- UI determinism fixtures
- constitutional dependency fixtures expected to produce YELLOW

---

## 6. Execution Order and Isolation

Canonical execution order:

1. schema validation tests
2. API contract conformance tests
3. UI rendering determinism tests
4. authority propagation tests
5. cross-layer integrity tests
6. constitutional dependency yellow checks

Isolation rules:

- no test may mutate another test's input
- no test result may become another test's hidden precondition
- shared fixtures must be immutable
- execution state must be reset between tests
- test ordering is recorded in the report

Execution order is procedural only. It does not imply priority or authority.

---

## 7. Report Schema

The harness emits a machine-readable report.

Report envelope:

```json
{
  "validation_report_id": "<id>",
  "harness_version": "0.1",
  "suite_commit": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696",
  "tested_commits": {
    "schema_normalization": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
    "api_contracts": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
    "ui_rendering_rules": "e8e75c99bb8458aa66ea14b6bde17b3189600f58"
  },
  "results": [
    {
      "test_id": "<id>",
      "status": "GREEN | YELLOW | RED",
      "reason": "<reason>",
      "artifact": "<artifact>",
      "authority": false,
      "semantic_change": false
    }
  ],
  "summary": {
    "green": 0,
    "yellow": 0,
    "red": 0
  },
  "authority": false,
  "semantic_change": false
}
```

Report counts are observations only.
Counts do not create authority.

---

## 8. Result Classification Logic

### 8.1 GREEN

Return GREEN only when:

- target artifact has a Git receipt
- fixture is deterministic
- expected condition is satisfied
- no authority elevation is detected
- no semantic drift is detected

### 8.2 YELLOW

Return YELLOW when:

- test touches a constitutional dependency without a Git receipt
- result depends on declared conversational material
- test cannot lawfully claim Git-backed validation

Required reason:

```text
Constitutional layer not Git-backed
```

### 8.3 RED

Return RED when:

- authority is elevated
- semantic change is introduced
- deterministic replay fails
- schema binding fails
- API envelope fails
- UI renders forbidden authority language
- hidden mutation is detected

---

## 9. Non-Authority Guarantees

The harness must never emit:

- `verified: true`
- `certified: true`
- `trusted: true`
- `authoritative: true`
- `consensus: true`
- `truth: true`

Forbidden language in reports:

```regex
\b(verified|certified|trusted|authoritative|consensus reached|ground truth|official truth)\b
```

Allowed language:

- GREEN
- YELLOW
- RED
- conformance observed
- violation detected
- dependency not Git-backed

Result labels are validation classes, not truth classes.

---

## 10. Deterministic Replay Requirements

A harness run is replay-stable only if:

```json
{
  "same_suite_commit": true,
  "same_test_manifest": true,
  "same_fixture_set": true,
  "same_harness_version": true,
  "same_results_required": true,
  "authority": false
}
```

Non-replayable conditions:

- uncontrolled network fetch
- clock-dependent assertions
- randomized fixture order
- mutable fixture source
- unpinned artifact references
- hidden environment assumptions

A non-replayable run must be RED or YELLOW, never GREEN.

---

## 11. Harness Implementation Boundary

This artifact is execution design only.

It does not provide:

- executable source code
- CI workflow definition
- command-line interface
- package metadata
- runtime dependencies

Those belong to a later artifact:

```text
CRP_VALIDATION_RUNNER_IMPLEMENTATION_V0_1
```

---

## 12. Final Summary Object

```json
{
  "CRP_VALIDATION_HARNESS_V0_1": {
    "role": "deterministic_validation_executor_design",
    "binds_to": {
      "artifact": "CRP_VALIDATION_SUITE_V0_1",
      "commit": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696"
    },
    "outputs": [
      "validation_report"
    ],
    "executes_tests": true,
    "certifies_truth": false,
    "grants_authority": false,
    "mutates_artifacts": false,
    "authority": false,
    "semantic_change": false,
    "next_recommended": "CRP_VALIDATION_RUNNER_IMPLEMENTATION_V0_1"
  }
}
```

The harness executes.
The harness reports.
The harness does not certify.
Authority remains false.
