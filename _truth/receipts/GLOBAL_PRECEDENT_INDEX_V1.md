# Global Precedent Index v1

## Purpose

Provide a cross-domain index of ALMS constitutional precedents that future halts, lift contracts, restoration attempts, and restoration rejections may cite.

This index is citation infrastructure.
It does not create new precedent.
It does not lift any halt.
It does not restore jurisdiction.
It only indexes committed precedent artifacts.

---

## Index Rules

1. Only committed, hash-addressable precedent artifacts may be listed.
2. Conversational claims, summaries, README rows, methodology rows, and issue comments are not sufficient for index inclusion.
3. Each precedent must identify:
   - precedent name
   - source artifact
   - commit SHA
   - holding
   - scope
   - citation form
   - active status
4. No inferred precedent may be added.
5. Any unverified precedent defaults to `NOT_INDEXED`.

---

## Indexed Precedents

### 1. NY-004 Unverified Input Restoration Rejection Precedent

**Precedent name:**

```text
NY-004_UNVERIFIED_INPUT_RESTORATION_REJECTION_PRECEDENT
```

**Source artifact:**

```text
_truth/receipts/NY_004_PRECEDENT_SUMMARY_V1.md
```

**Commit:**

```text
47a131ec20b3c5ec3ed1f4e09c2dd3d24d67cfd9
```

**Bound issue:**

```text
Issue #132
```

**Holding:**

```text
A referenced claim does not become admissible evidence until the underlying artifact is committed, inspectable, hash-verifiable, and replay-admissible.
```

**Rules:**

```text
REFERENCE != EVIDENCE
STRUCTURE != AUTHORITY
INTENT != AUTHORITY
RESTORATION != VALID WITHOUT ARTIFACT
UNVERIFIABLE != FALSE
UNVERIFIABLE = OUTSIDE_JURISDICTION
```

**Scope:**

```text
Missing or unverifiable artifact claims in any ALMS domain.
```

**Operational consequence:**

```text
If a restoration attempt references absent evidence, restoration is rejected and halt remains active.
```

**Citation form:**

```text
Cite: NY-004_UNVERIFIED_INPUT_RESTORATION_REJECTION_PRECEDENT
Source: _truth/receipts/NY_004_PRECEDENT_SUMMARY_V1.md
```

**Active status:**

```text
ACTIVE
```

---

## Current Non-Indexed Domains

No additional global precedents are indexed in this version.

The following categories require committed precedent artifacts before inclusion:

- attention membrane precedents
- speech membrane precedents
- hash mismatch / malice boundary precedents
- epoch boundary precedents
- anchoring invalidation precedents
- finality collapse precedents

---

## Closure Property

This file defines the current global precedent index.

No precedent may be cited as indexed unless it appears in this file or a later committed version.

Any unclassified or uncommitted precedent defaults to:

```text
NOT_INDEXED
```

Fail closed, never open.
