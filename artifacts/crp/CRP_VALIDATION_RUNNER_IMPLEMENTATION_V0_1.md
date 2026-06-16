# CRP_VALIDATION_RUNNER_IMPLEMENTATION_V0_1

_validation runner implementation design — authority: false, semantic_change: false_

## 1. Purpose and Scope

The CRP Validation Runner Implementation V0.1 defines the executable runner interface and behavior required to execute the CRP Validation Harness V0.1.

It specifies:

- CLI shape
- exit codes
- fixture loading
- SHA binding checks
- execution lifecycle
- error handling
- report generation
- CI integration contract

It does not:

- claim tests have run
- certify truth
- approve artifacts
- grant authority
- mutate CRP artifacts
- replace the validation suite or harness

The runner executes tests as defined.
The runner does not verify CRP.

---

## 2. Binding Receipt

This runner implementation design binds to the Git-backed harness artifact:

```json
{
  "artifact": "CRP_VALIDATION_HARNESS_V0_1",
  "repo": "jsonwisdom/AL",
  "path": "artifacts/crp/CRP_VALIDATION_HARNESS_V0_1.md",
  "commit": "8cc405ecd53ccd83d4821104a5d6513d3bb460cd",
  "authority": false,
  "semantic_change": false
}
```

The runner must also check the expected implementation-layer SHAs before execution.

Expected implementation chain:

```json
{
  "constitutional_index": "014f4517f980cfe77a701372dd95dba48328d300",
  "schema_suite_placeholder": "54451723ee666e5f198c19e3768d2a08961afa3e",
  "schema_normalization": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
  "api_contracts": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
  "ui_rendering_rules": "e8e75c99bb8458aa66ea14b6bde17b3189600f58",
  "validation_suite": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696",
  "validation_harness": "8cc405ecd53ccd83d4821104a5d6513d3bb460cd",
  "authority": false
}
```

---

## 3. CLI Interface

Canonical command:

```bash
crp-validate --profile crp_v0_1_default --report out/report.json
```

Supported options:

```text
--profile <name>       Validation profile. Required.
--report <path>        Machine-readable report output path. Required.
--fixtures <path>      Fixture directory. Default: fixtures/crp/v0.1
--manifest <path>      Test manifest path. Default: fixtures/crp/v0.1/manifest.json
--fail-fast            Stop execution after first RED result.
--verbose              Print human-readable progress output.
--offline              Reject undeclared network access. Default: true.
```

The runner must fail with exit code 2 if required options are missing or invalid.

---

## 4. Exit Codes

```text
0  No RED results were produced. YELLOW may still be present.
1  One or more RED results were produced.
2  Harness, configuration, fixture, or runner error.
```

Hard rule:

```json
{
  "exit_code_0": "NO_RED_RESULTS",
  "yellow_allowed": true,
  "green_only_claim_forbidden": true,
  "verified_claim_forbidden": true,
  "authority": false
}
```

Exit code 0 does not mean all dependencies are Git-backed.
Exit code 0 does not mean CRP is verified.
Exit code 0 does not mean CRP is certified.
Exit code 0 does not create authority.

---

## 5. Execution Lifecycle

Canonical lifecycle:

```text
1. LOAD_CONFIGURATION
2. LOAD_FIXTURES
3. VERIFY_FIXTURE_HASHES
4. VERIFY_SHA_BINDING
5. RUN_SCHEMA_TESTS
6. RUN_API_TESTS
7. RUN_UI_TESTS
8. RUN_AUTHORITY_PROPAGATION_TESTS
9. RUN_CROSS_LAYER_TESTS
10. RUN_CONSTITUTIONAL_YELLOW_CHECKS
11. AGGREGATE_RESULTS
12. WRITE_REPORT
13. EXIT_WITH_CODE
```

Lifecycle order is procedural only.
It does not imply authority or priority.

---

## 6. Configuration Model

Runner configuration envelope:

```json
{
  "runner_version": "0.1",
  "profile": "crp_v0_1_default",
  "suite_commit": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696",
  "harness_commit": "8cc405ecd53ccd83d4821104a5d6513d3bb460cd",
  "expected_commits": {
    "schema_normalization": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
    "api_contracts": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
    "ui_rendering_rules": "e8e75c99bb8458aa66ea14b6bde17b3189600f58"
  },
  "authority": false,
  "semantic_change": false
}
```

Invalid configuration produces exit code 2.

---

## 7. Fixture Model

Fixture directory:

```text
fixtures/crp/v0.1/
```

Manifest path:

```text
fixtures/crp/v0.1/manifest.json
```

Manifest structure:

```json
{
  "fixture_set_id": "crp_v0_1_fixture_set_001",
  "fixture_set_version": "0.1",
  "fixtures": [
    {
      "name": "entry_valid_001",
      "path": "entry_valid_001.fixture.json",
      "hash": "sha256:<hash>",
      "layer": "ENTRY",
      "expected_status": "GREEN"
    }
  ],
  "authority": false,
  "semantic_change": false
}
```

Fixture rules:

- fixtures are loaded from manifest only
- fixture content must match declared SHA256
- path is location only, hash is identity
- fixture mutation requires a new hash
- missing fixture produces exit code 2
- malformed fixture produces RED if loaded as test input, or exit code 2 if the harness cannot continue

---

## 8. SHA Binding Verification

Before tests run, the runner must compare expected commits against the configured artifact references.

Required bindings:

```json
{
  "schema_normalization": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
  "api_contracts": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
  "ui_rendering_rules": "e8e75c99bb8458aa66ea14b6bde17b3189600f58",
  "validation_suite": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696",
  "validation_harness": "8cc405ecd53ccd83d4821104a5d6513d3bb460cd"
}
```

Mismatch behavior:

```json
{
  "status": "RED",
  "reason": "SHA_BINDING_MISMATCH",
  "authority": false,
  "semantic_change": false
}
```

If the runner cannot inspect bindings due to configuration failure, exit code 2 applies.

---

## 9. Test Execution Details

### 9.1 Schema Tests

Validate fixtures against normalized schema expectations.

Expected checks:

- required fields present
- `authority` is false
- `semantic_change` is false
- no forbidden additional properties where schema forbids them
- layer const values match expected layer

### 9.2 API Tests

Validate API contract examples and envelopes.

Expected checks:

- endpoint has schema binding
- response has `data`
- response has `schema_id`
- response has `authority: false`
- response has `semantic_change: false`
- write-like endpoint has idempotency rule
- error envelope is non-authoritative

### 9.3 UI Tests

Validate UI rendering rules using fixture labels and rendering profile.

Expected checks:

- forbidden authority terms are rejected
- same payload and same profile produce same output
- UI profile is visible in output metadata
- observer interpretation is separated from registry output

### 9.4 Authority Propagation Tests

Validate that `authority: false` remains false across schema, API, UI, and report layers.

### 9.5 Cross-Layer Tests

Validate that:

- schemas do not define endpoints
- APIs do not define UI rendering
- UI does not define API behavior
- runner does not certify truth

### 9.6 Constitutional Yellow Checks

Any test touching conversation-defined constitutional artifacts must return YELLOW unless those artifacts receive separate Git receipts.

---

## 10. Report Format

Report output must be machine-readable JSON.

Report envelope:

```json
{
  "report_id": "<uuid-or-deterministic-id>",
  "runner_version": "0.1",
  "profile": "crp_v0_1_default",
  "suite_commit": "23d571fa4b2c476f79b41d24c6e1c8115e6a7696",
  "harness_commit": "8cc405ecd53ccd83d4821104a5d6513d3bb460cd",
  "tested_commits": {
    "schema_normalization": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
    "api_contracts": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
    "ui_rendering_rules": "e8e75c99bb8458aa66ea14b6bde17b3189600f58"
  },
  "results": [
    {
      "test_id": "<test-id>",
      "status": "GREEN | YELLOW | RED",
      "reason": "<reason>",
      "layer": "<layer>",
      "authority": false,
      "semantic_change": false
    }
  ],
  "summary": {
    "green": 0,
    "yellow": 0,
    "red": 0
  },
  "exit_code": 0,
  "authority": false,
  "semantic_change": false
}
```

Report IDs may be deterministic or UUID-based. If UUID-based, replay comparison must ignore report_id or the implementation must provide deterministic mode.

---

## 11. Error Handling

Runner errors are not test failures unless a test executed and produced RED.

Exit code 2 applies to:

- missing configuration
- missing fixture manifest
- fixture hash mismatch before test execution
- unreadable report path
- invalid profile
- malformed manifest
- internal runner exception

Exit code 1 applies to:

- one or more RED test results

Exit code 0 applies to:

- GREEN and/or YELLOW results with no RED results

No error class may emit authority.

---

## 12. CI Integration Contract

A CI job using the runner should:

```bash
crp-validate \
  --profile crp_v0_1_default \
  --fixtures fixtures/crp/v0.1 \
  --manifest fixtures/crp/v0.1/manifest.json \
  --report out/crp-validation-report.json \
  --offline
```

CI rules:

- exit 0: job may pass, but must not label CRP verified
- exit 1: job fails due to RED test result
- exit 2: job fails due to runner/harness/configuration error
- report artifact should be uploaded if available
- CI must not modify CRP artifacts

Forbidden CI labels:

- Verified
- Certified
- Trusted
- Approved
- Ground Truth

Allowed CI labels:

- Validation run completed
- No RED results
- RED results detected
- Configuration error

---

## 13. Non-Authority Guarantees

The runner must never output:

```json
{
  "verified": true,
  "certified": true,
  "trusted": true,
  "authoritative": true,
  "truth": true,
  "authority": true
}
```

Allowed result semantics:

```json
{
  "GREEN": "test condition satisfied",
  "YELLOW": "dependency or assumption not Git-backed",
  "RED": "test condition failed or violation detected",
  "authority": false
}
```

GREEN is not truth.
YELLOW is not ignorable.
RED is not a legal judgment.

---

## 14. Implementation Boundary

This artifact defines implementation requirements for a runner.

It does not include actual source code.

Source code, CI workflows, package metadata, and executable fixtures belong to later artifacts, such as:

```text
CRP_VALIDATION_RUNNER_SOURCE_V0_1
CRP_VALIDATION_FIXTURE_SET_V0_1
CRP_VALIDATION_CI_WORKFLOW_V0_1
```

---

## 15. Final Summary Object

```json
{
  "CRP_VALIDATION_RUNNER_IMPLEMENTATION_V0_1": {
    "role": "validation_runner_implementation_design",
    "binds_to": {
      "artifact": "CRP_VALIDATION_HARNESS_V0_1",
      "commit": "8cc405ecd53ccd83d4821104a5d6513d3bb460cd"
    },
    "cli": "crp-validate --profile crp_v0_1_default --report out/report.json",
    "exit_codes": {
      "0": "NO_RED_RESULTS_NOT_VERIFIED",
      "1": "RED_RESULTS_PRESENT",
      "2": "RUNNER_OR_CONFIGURATION_ERROR"
    },
    "claims_tests_ran": false,
    "provides_source_code": false,
    "certifies_truth": false,
    "grants_authority": false,
    "authority": false,
    "semantic_change": false,
    "next_recommended": [
      "CRP_VALIDATION_FIXTURE_SET_V0_1",
      "CRP_VALIDATION_RUNNER_SOURCE_V0_1",
      "CRP_VALIDATION_CI_WORKFLOW_V0_1"
    ]
  }
}
```

The runner executes tests.
The runner reports results.
Exit code 0 is not verification.
Authority remains false.
