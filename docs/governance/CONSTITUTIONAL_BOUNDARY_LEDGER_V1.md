# CONSTITUTIONAL_BOUNDARY_LEDGER_V1 — ALMS Kernel Boundaries

## Status

`CONSTITUTIONAL_BOUNDARY_LEDGER_V1_OPENED`

---

## Purpose

Codify the mandatory, forbidden, and executable boundaries of ALMS Constitutional Kernel v0.1.

The ledger is a control surface for auditors, implementers, verifiers, and future agents.

It records what ALMS must do, must forbid, and must execute deterministically.

---

## Boundary Table

| ID | Class | Rule | Enforcement Surface | Failure Mode |
|---|---|---|---|---|
| B001 | MUST | GitHub is the canonical byte surface unless another canonical source is explicitly declared. | Root schema / fixtures | INDETERMINATE |
| B002 | MUST | Identity resolves discovery. | ENS / public root / witnesses | REVIEW_REQUIRED |
| B003 | MUST | Replay resolves truth. | Verifier / replay spec | FAIL or INDETERMINATE |
| B004 | MUST | Every proof claim requires canonical bytes. | REPLAY_SPEC_V1 | INDETERMINATE |
| B005 | MUST | Every fixture requires provenance declaration. | FIXTURE_SPEC_V1 | INDETERMINATE |
| B006 | MUST | Every replay requires declared transform policy. | REPLAY_SPEC_V1 | INDETERMINATE or TAINTED |
| B007 | MUST | Every verifier verdict requires replay trace. | VERIFIER_SPEC_V1 / CVD_OUTPUT_SCHEMA_V1 | invalid opinion |
| B008 | MUST | Every public drift opinion emits CVD_OUTPUT_SCHEMA_V1. | CVD output | invalid report |
| B009 | MUST | Witnesses remain optional timestamp/discovery surfaces. | Witness validator | REVIEW_REQUIRED |
| B010 | MUST | Minnesota is STATE_FIXTURE_001 until superseded by explicit versioned doctrine. | MN corpus spec | REVIEW_REQUIRED |
| F001 | FORBID | No network calls during replay. | Reference verifier | TAINTED |
| F002 | FORBID | No hidden API keys or private secrets required for public proof. | Verifier / CI | invalid proof |
| F003 | FORBID | No witness may replace canonical bytes. | Witness validator | REVIEW_REQUIRED or FAIL |
| F004 | FORBID | No platform ID may be treated as authoritative UID. | Root schema | REVIEW_REQUIRED |
| F005 | FORBID | No implicit transform. | Canonicalizer | INDETERMINATE |
| F006 | FORBID | No self-referential report hashing. | CVD output / CI | invalid report |
| F007 | FORBID | No narrative summary may substitute for canonical evidence. | Fixture / receipt | FAIL or INDETERMINATE |
| F008 | FORBID | No PASS without digest recomputation. | Verifier / CI | invalid verdict |
| E001 | EXECUTE | Validate schema before replay. | Verifier | invalid input |
| E002 | EXECUTE | Validate provenance before admissibility. | Fixture validator | INDETERMINATE |
| E003 | EXECUTE | Canonicalize under declared policy. | Canonicalizer | TAINTED if policy-divergent |
| E004 | EXECUTE | Compute digest over canonical bytes. | Digest engine | FAIL on mismatch |
| E005 | EXECUTE | Verify receipt binding. | Receipt engine | FAIL or INDETERMINATE |
| E006 | EXECUTE | Validate manifest aggregation rule. | Manifest validator | INDETERMINATE |
| E007 | EXECUTE | Classify drift under CVD V1-V5. | CVD classifier | variant verdict |
| E008 | EXECUTE | Emit deterministic public opinion artifact. | CVD output generator | invalid opinion |
| E009 | EXECUTE | Preserve replay trace hash. | Report generator | invalid opinion |
| E010 | EXECUTE | Fail closed when evidence is insufficient. | Verdict engine | INDETERMINATE |

---

## Closure Conditions

```text
No replay, no proof.
No canonical bytes, no replay.
No declared transform policy, no admissibility.
No trace, no opinion.
No network calls during replay.
```

---

## Final Rule

A constitutional replay system is trusted only when its boundaries are enforceable.

Verify > narrative.
