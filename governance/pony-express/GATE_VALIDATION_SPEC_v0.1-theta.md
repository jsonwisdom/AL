# Gate Validation Spec v0.1-θ

**Parent:** `TRANSITION_CONTROL_MATRIX_v0.1-theta`  
**Materiality control:** `MATERIALITY_RULE_v1.0`  
**Classification:** Procedural validation rules for pedagogical progression gates  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Define the machine-checkable and human-reviewable rules that decide whether a candidate may advance from one role to the next inside the simulation. Validation produces receipts. Validation never produces real-world authority or historical truth.

```text
GATE_PASS          = STRUCTURAL_CONFORMANCE_ONLY
RECEIPT            ≠ AUTHORITY
ROLE_ADVANCEMENT   ≠ PUBLIC_OFFICE
SIMULATION_OUTCOME ≠ HISTORICAL_TRUTH
```

## 2. Universal Invariants (All Stages)

Every gate validation MUST enforce:

1. **Monotonicity** — No stage may be skipped or collapsed backward.
2. **Receipt completeness** — Minimum receipt count and type for the stage must be present and hash-chained.
3. **Artifact presence** — Every required artifact named in the matrix must exist and validate against its declared schema (if any).
4. **Fail-closed default** — Any indeterminate, missing, or malformed field yields FAIL.
5. **Authority annotation** — Every generated receipt carries `authority: false` and `historical_truth_established: false`.
6. **Gate 1 respect** — No validation path may set `gate_1` to any value other than `BLOCKED` unless an external, independently verified byte-capture pair has already been admitted (currently none).
7. **Docket emptiness** — Core historical docket remains `EMPTY`. Pedagogical hypos must be labeled `PEDAGOGICAL_ONLY`.
8. **Materiality enforcement** — Every affected object defaults to `MUST`. Missing, malformed, conflicting, or indeterminate classifications resolve to `MUST`.
9. **Strict inheritance** — Every Fission/Fusion child must satisfy `STRICTEST_PARENT_WINS`; any `MUST` or unknown parent yields `MUST`.
10. **Materiality receipt completeness** — A material transformation without a valid `RECEIPT-MAT-*` chain entry yields FAIL.

## 3. Per-Stage Validation Rules

### STAGE-1  STUDENT → READER

| Check | Rule |
|-------|------|
| Artifacts | `ONBOARDING_ACK.json` and `REPO_INIT_RECEIPT.json` present and schema-valid |
| Exercises | Evidence of successful US3D:// coordinate mapping and byte-integrity isolation exercise |
| Receipts | ≥ 1 cryptographic replication receipt whose payload matches a known fixture hash |
| Conditions | `BYTE_EQUALITY = INTEGRITY_ONLY` asserted; zero unauthorized branch mutations detected |
| Fail | Document existence treated as historical truth; coordinate syntax skipped |
| Reviewer | Automated CI Linter (exit code 0 required) |
| Appeal | Re-run local harness; submit patch commit |

### STAGE-2  READER → ADVOCATE

| Check | Rule |
|-------|------|
| Artifacts | `RULE_MAP_V1.md` present and non-empty |
| Exercises | At least one recorded separation of claim / evidence / authority; one counterargument; one structural self-correction |
| Receipts | ≥ 3 receipts whose payloads demonstrate distinct claim-layer separation |
| Conditions | No Z-layer authority skip; `ROUTE_EXISTENCE ≠ AUTHORITY` |
| Fail | Interpretation conflated with adjudication; narrative speed prioritized over procedure |
| Reviewer | Peer Reviewer (Reader+) |
| Appeal | Submit missing receipt hash via PR addendum; peer re-test |

### STAGE-3  ADVOCATE → CLERK

| Check | Rule |
|-------|------|
| Artifacts | `DOCKET_ENTRY_V1.json` contains raw-byte reference + identity metadata |
| Exercises | Historical depth pipeline constructed (Z0 → at least Z5); missing witness fields logged without synthesis |
| Receipts | ≥ 5 ingestion receipts, each carrying a SHA-256 digest |
| Conditions | `EVIDENCE_PRECEDES_EVOLUTION`; zero unverified source pointers |
| Fail | Unverified IPFS CIDs ingested; dead URLs treated as active evidence |
| Reviewer | Senior Clerk / Docket Administrator |
| Appeal | Re-verify pointers; replace broken hashes; re-submit package |

### STAGE-4  CLERK → PANELIST

| Check | Rule |
|-------|------|
| Artifacts | `PRECEDENT_BRIEF_V1.md` cites only simulation rulings |
| Exercises | Binding vs non-binding distinction demonstrated; structured challenge to an existing simulation ruling formulated |
| Receipts | ≥ 2 hash-chained precedent receipts |
| Conditions | Precedent fidelity confirmed; zero real-world legal authority claims |
| Fail | Simulation outcome treated as real-world law; public opinion treated as procedural validity |
| Reviewer | Panel Board (minimum 2 Panelists) |
| Appeal | Revise brief to restrict scope; resubmit to docket pool |

### STAGE-5  PANELIST → JUDICIAL_ENGINEER

| Check | Rule |
|-------|------|
| Artifacts | `JUDICIAL_ENGINEER_V1.py` present and executable inside the sandbox |
| Exercises | Contradiction dominance enforced; fail-closed gate block authored; materiality inheritance tested |
| Receipts | ≥ 3 passing automated test receipts under malicious fixture injection, including missing-materiality and mixed-parent cases |
| Conditions | `INTERPRETATION ≠ ADJUDICATION`; `DEFAULT_MATERIALITY = MUST`; `STRICTEST_PARENT_WINS` enforced in code |
| Fail | Indeterminate states allowed to pass; absolute paths hardcoded; material child downgraded to decorative; required materiality receipt absent |
| Reviewer | System Architect / Lead Maintainer |
| Appeal | Patch script; fix path encapsulation or materiality enforcement; run full integration suite |

### STAGE-6  JUDICIAL_ENGINEER → STEWARD_OF_JUSTICE

| Check | Rule |
|-------|------|
| Artifacts | `STEWARD_MANIFEST_V1.md` present |
| Exercises | Dual-axis audit (SELF-Score + JUSTICE-Score) completed; full lifecycle audit from raw bytes to steward receipt |
| Receipts | Complete verified chain covering Stages 1–5; zero-defect self-examination log; complete required materiality receipts |
| Conditions | `WISDOM = SELF ∩ JUSTICE` demonstrated inside the simulation |
| Fail | High SELF / low JUSTICE (Ego); Low SELF / high JUSTICE (Accident); material transformation without receipt |
| Reviewer | Full Judicial Council |
| Appeal | Complete remediation module on bias + procedural humility; restart promotion cycle |

## 4. Materiality Validation

For each created, updated, deleted, split, joined, classified, scored, or replayed object:

```text
classification absent       → MUST
classification malformed    → MUST
classification conflicting  → MUST
any parent MUST             → MUST
any parent unknown          → MUST
required receipt absent     → FAIL
lineage incomplete          → FAIL
receipt chain invalid       → FAIL
```

A `MAY` result is valid only when an explicit `RECEIPT-MAT-*` records a purely decorative change and proves that identity, lineage, meaning, scoring, progression, custody, admission, and replay state are unchanged.

Materiality validation does not verify source truth, admit evidence, assign civic mass, or open Gate 1.

## 5. Validation Outcome Object

Every gate evaluation MUST emit a receipt of the form:

```json
{
  "receipt_id": "RECEIPT-GV-<stage>-<seq>",
  "matrix_version": "TRANSITION_CONTROL_MATRIX_v0.1-theta",
  "materiality_rule_version": "MATERIALITY_RULE_v1.0",
  "stage_id": "STAGE-N",
  "candidate_id": "...",
  "result": "PASS | FAIL | INDETERMINATE",
  "authority": false,
  "historical_truth_established": false,
  "gate_1_status": "BLOCKED",
  "checks": [],
  "materiality_checks": [],
  "previous_receipt_hash": null,
  "receipt_hash": null,
  "recorded_at": null
}
```

`INDETERMINATE` is treated as FAIL for advancement purposes.

## 6. Prohibited Behaviors

```text
SKIP_STAGE                         = PROHIBITED
BACKWARD_COLLAPSE                  = PROHIBITED
GATE_1_BYPASS                      = PROHIBITED
REAL_WORLD_AUTHORITY_CLAIM         = PROHIBITED
HISTORICAL_TRUTH_FROM_SIMULATION   = PROHIBITED
SYNTHETIC_SOURCE_BYTES             = PROHIBITED
UNLABELED_PEDAGOGICAL_HYPO         = PROHIBITED
MATERIALITY_DEFAULT_MAY            = PROHIBITED
MATERIAL_PARENT_DOWNGRADE          = PROHIBITED
UNRECEIPTED_MATERIAL_TRANSFORMATION = PROHIBITED
```

## 7. Current State

```text
ARTIFACT                = GATE_VALIDATION_SPEC_v0.1-theta
PARENT                  = TRANSITION_CONTROL_MATRIX_v0.1-theta
MATERIALITY_CONTROL     = MATERIALITY_RULE_v1.0
DEFAULT_MATERIALITY     = MUST
INHERITANCE_RULE        = STRICTEST_PARENT_WINS
GATE_1                  = BLOCKED
AUTHORITY               = FALSE
CORE_DOCKET             = EMPTY
EXECUTION               = SIMULATION_ONLY
PROMOTION               = BLOCKED
```
