# Materiality Rule v1.0

**Parent:** `ORGANIZED_CHAOS_NAMING_v0.1-theta`, `RECEIPT_CHAIN_PROTOCOL_v0.1-theta`, `ENTRENCHED_ADMISSIONS_v1.0`  
**Classification:** Frozen simulation control rule  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Vessel status:** EMPTY_VESSEL  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Determine when a token edit, split, join, transformation, classification, or lineage mutation MUST produce a receipt. The rule is fail-closed: uncertainty does not excuse receipt creation.

```text
DEFAULT_MATERIALITY      = MUST
INHERITANCE_RULE         = STRICTEST_PARENT_WINS
UNRECEIPTED_EDIT         = MATERIAL
INDETERMINATE            = MUST
RECEIPT                  ≠ AUTHORITY
MATERIALITY              ≠ EPISTEMIC_MASS
```

## 2. Materiality Classes

| Class | Receipt obligation | Meaning |
|---|---|---|
| `MUST` | Required | Change affects identity, lineage, meaning, scoring, progression, custody, evidence reference, or replay state |
| `MAY` | Optional | Proven decorative rendering change with no semantic or procedural effect |

There is no implicit `MAY`. A change is `MAY` only when an explicit classifier records why it cannot affect meaning, lineage, scoring, progression, custody, admission, or replay.

## 3. Default-MUST Polarity

Any edit without a valid, receipted `MAY` classification is material.

```text
missing classification  → MUST
malformed classification → MUST
conflicting classification → MUST
review unavailable → MUST
```

Silence is not evidence of decoration.

## 4. Strictest-Parent-Wins

For every Fission or Fusion transformation:

```text
child.materiality = MAX_STRICTNESS(all parent.materiality, local_effect)
```

Where:

```text
MUST > MAY
```

Therefore:

- `MUST + MUST → MUST`
- `MUST + MAY → MUST`
- `MAY + MAY → MAY` only when the local transformation is independently classified and receipted as decorative
- any unknown parent → `MUST`

A child may never downgrade a parent’s receipt obligation.

## 5. Material Transformations

The following always resolve to `MUST`:

- creation, deletion, or renaming of an `ATM-`, `FIS-`, `FUS-`, `ISO-`, `CV-`, or `CRX-` object;
- changes to parent or daughter identifiers;
- claim, evidence, authority, provenance, custody, or jurisdiction changes;
- score, stage, gate, attention-budget, precedent, or replay-state changes;
- changes that affect validation output;
- conversion between fictional and real epistemic classes;
- any operation touching admission, mass, Gate 1, or the core docket.

`NFL-` attention-budget consumption is material when it changes session state. Cosmetic display of an unchanged balance may be classified `MAY`.

## 6. Required Receipt Fields

A materiality receipt MUST include:

```json
{
  "receipt_id": "RECEIPT-MAT-<seq>",
  "rule_version": "MATERIALITY_RULE_v1.0",
  "object_id": "TOKEN://...",
  "operation": "CREATE | UPDATE | DELETE | FISSION | FUSION | CLASSIFY",
  "materiality": "MUST | MAY",
  "parent_ids": [],
  "parent_materialities": [],
  "inheritance_result": "MUST | MAY",
  "reason_codes": [],
  "authority": false,
  "historical_truth_established": false,
  "gate_1_status": "BLOCKED",
  "previous_receipt_hash": null,
  "receipt_hash": null,
  "recorded_at": null
}
```

Receipts follow RFC 8785 JCS and SHA-256 under `RECEIPT_CHAIN_PROTOCOL_v0.1-theta`.

## 7. Fail-Closed Validation

```text
if classification absent: MUST
if any parent MUST: MUST
if any parent unknown: MUST
if lineage incomplete: FAIL
if required receipt absent: FAIL
if receipt chain invalid: FAIL
if role merge detected: exit(1) + ROLE_MERGE_DETECTED
```

A failed materiality check blocks the affected simulation transition. It does not open Gate 1 or establish truth.

## 8. Hard Boundaries

```text
MATERIALITY_RECEIPT      ≠ SOURCE_VERIFICATION
MATERIALITY_RECEIPT      ≠ ADMISSION
MATERIALITY              ≠ CIVIC_MASS
TOKEN_LINEAGE            ≠ HISTORICAL_TRUTH
NO_MATERIALITY_RULE_OPENS_GATE_1
SEPARATION_OF_DUTIES     = FROZEN
```

## 9. Current State

```text
ARTIFACT              = MATERIALITY_RULE_v1.0
DEFAULT_MATERIALITY   = MUST
INHERITANCE_RULE      = STRICTEST_PARENT_WINS
GATE_1                = BLOCKED
VESSEL_STATUS         = EMPTY_VESSEL
MASS_BEARING_RECORD   = NONE
AUTHORITY             = FALSE
CORE_DOCKET           = EMPTY
PROMOTION             = BLOCKED
```
