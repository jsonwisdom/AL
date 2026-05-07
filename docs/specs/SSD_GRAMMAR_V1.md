# SSD Grammar v1 — Supplemental Semantic Description

**Artifact:** `SSD_GRAMMAR_V1`  
**Status:** `SEALED_SPEC_DRAFT`  
**Protocol Context:** `CBREv1 / E2-STRICT-CANONICAL`  
**Primary Rule:** The SSD describes meaning. It never controls execution.

---

## 1. Purpose

The Supplemental Semantic Description (SSD) is the human-readable semantic layer for CBRE receipts.

It exists to answer:

> What does the emitting branch claim this receipt means under its own rules?

It does **not** answer:

> What must the receiving branch believe or adopt?

The SSD carries attested claims, not adopted truths.

---

## 2. Format

SSD v1 uses **Markdown with structured reference tags**.

Rationale:

- Markdown is readable by humans.
- Tags are extractable by machines.
- Tags are claims, not global truths.
- Branches may extend the tag vocabulary without requiring a central ontology authority.

---

## 3. Tag Syntax

Tags use the following form:

```text
[TAG_NAME: TAG_VALUE]
```

Rules:

- `TAG_NAME` MUST be uppercase ASCII.
- `TAG_NAME` MAY contain underscores.
- `TAG_VALUE` MUST be printable text without nested brackets.
- Tags are non-binding on receivers.
- Unknown tags MUST be logged or ignored, not treated as invalid.

---

## 4. Required Tags

Every SSD v1 document MUST include:

```text
[ADOPTION_POSTURE: NEUTRAL]
```

Allowed values:

```text
NEUTRAL
RECOMMENDED
DISCOURAGED
```

Meaning:

- `NEUTRAL` — branch makes no adoption recommendation.
- `RECOMMENDED` — emitting branch recommends adoption under its own semantics.
- `DISCOURAGED` — emitting branch discourages adoption under its own semantics.

No value compels receiver action.

---

## 5. Recommended Reference Tags

```text
[CBRE_TRACE: sha256:<64hex>]
[ASSET_MANIFEST: sha256:<64hex>]
[ASSET_ID: <asset-id>]
[BRANCH_ID: <branch-id>]
[SEMANTIC_CONFLICT: ACKNOWLEDGED]
```

These tags help connect SSD meaning to verifiable artifacts without granting the SSD execution authority.

---

## 6. Optional Branch Tags

Branches MAY define additional tags, including but not limited to:

```text
[ASSET_INTEGRITY: VERIFIED]
[CUSTODY_POSTURE: CHALLENGED]
[RISK_CLASS: HIGH]
[POLICY_SCOPE: LOCAL]
[TRIBUNAL_NOTE: REVIEW_REQUIRED]
```

Receivers are not required to parse or accept branch-defined tags.

---

## 7. Prohibited Semantics

No SSD tag may claim authority over the receiving branch's internal state.

Prohibited examples:

```text
[RECEIVER_MUST_ADOPT: TRUE]
[OVERRIDE_NAMESPACE_POLICY: TRUE]
[TRACE_OUTPUT_SELECTOR: 2]
[LOCAL_STATE_CHANGE: REQUIRED]
```

If present, these tags MUST be treated as semantic claims only and MUST NOT affect CBRE execution, lineage validation, namespace policy, or adoption.

---

## 8. Constitutional Boundary

The SSD has zero execution authority.

It may describe:

- branch-local interpretation,
- branch-local policy context,
- adoption recommendation,
- semantic conflict,
- reference hashes.

It may not control:

- opcode execution,
- stack behavior,
- committed output selection,
- namespace reservation,
- lineage database state,
- adoption decision.

---

## 9. Receiver Behavior

A receiving branch SHOULD process SSDs as follows:

```text
1. Parse readable Markdown.
2. Extract structured tags.
3. Log known tags.
4. Preserve unknown tags as non-binding branch claims.
5. Compare tags against local policy only after CBRE trace, manifest, lineage, and namespace checks.
6. Never allow SSD tags to modify verifier behavior.
```

---

## 10. Result States

Possible SSD-layer states:

```text
SSD_STATUS: PRESENT
SSD_STATUS: MISSING
SSD_STATUS: MALFORMED_TAGS
SSD_STATUS: PARSED_WITH_UNKNOWN_TAGS
SSD_STATUS: SEMANTIC_CONFLICT_ACKNOWLEDGED
```

These states do not determine trace validity.

---

## 11. Core Law

```text
The SSD explains.
The trace executes.
The manifest binds.
The lineage remembers.
The namespace guards.
The sovereign adopts.
```

No SSD may become a hidden interpreter.

---

## 12. Minimal Example

```markdown
# SSD: Asset Verification Report

**Branch:** E1-PRIME  
**Asset:** doc:shared-research-0042  
**Policy Context:** Standard integrity verification under E1 governance scope.

## Claims

- [ASSET_INTEGRITY: VERIFIED] — Trace confirms computation over declared FACT_A.
- [ADOPTION_POSTURE: NEUTRAL] — No adoption recommendation is made.
- [SEMANTIC_CONFLICT: ACKNOWLEDGED] — Receiver may disagree without denying veracity.

## Refs

- [CBRE_TRACE: sha256:0000000000000000000000000000000000000000000000000000000000000000]
- [ASSET_MANIFEST: sha256:1111111111111111111111111111111111111111111111111111111111111111]
```

---

## 13. Final Invariant

```text
A tag is a claim.
A claim is not a command.
A parsed SSD is not adopted truth.
```

**SSD_GRAMMAR_V1: SEALED_SPEC_DRAFT**
