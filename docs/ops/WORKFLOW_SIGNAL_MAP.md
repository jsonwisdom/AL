# Workflow Signal Map

Status: ACTIVE_OPERATOR_GUIDE

## Core rule

Everything can affect the Merkle / genesis surface eventually, but not every workflow failure means the same thing.

This file separates **human signal** from **machine signal** so GitHub Actions does not become unreadable.

---

## 1. Signal classes

### Class A — Global / Genesis-affecting

These workflows protect roots, ledgers, claims, or repo-wide safety.

A failure here means: **do not promote global state until reviewed.**

Examples:

- Zero Trust Audit
- Jay Repo Safety Scan
- Verify Claims
- Verify Merkle Note
- ALMS CI Enforcement

Human interpretation:

```json
{
  "class": "A",
  "meaning": "global promotion gate",
  "failure_action": "pause promotion; inspect reason; do not assume corpus failure"
}
```

---

### Class B — Local corpus / proof lanes

These workflows test one bounded proof surface.

Examples:

- C0001 Source Hash Discovery
- C0002 Source Hash Discovery
- MANUAL ONLY C0001 C0002 REPLAY REPORT
- TRACK_00X_10 Deterministic Replay Corpus

Human interpretation:

```json
{
  "class": "B",
  "meaning": "local proof gate",
  "failure_action": "inspect only that corpus report; do not chase unrelated workflows"
}
```

---

### Class C — Legacy / batch rebuild lanes

These workflows may fail due to older batch invariants, blocked entries, or drift unrelated to the active corpus lane.

Examples:

- KB Batch - Build & Verify

Human interpretation:

```json
{
  "class": "C",
  "meaning": "legacy/batch lane",
  "failure_action": "record separately; do not treat as C0001/C0002 proof failure unless dependency is explicit"
}
```

---

## 2. Merkle bleed rule

Because global roots aggregate state, local changes can eventually affect global checks.

But causality must be explicit:

```json
{
  "valid_inference": "C0002 changed -> root manifest includes C0002 -> root changed",
  "invalid_inference": "KB Batch failed -> C0002 failed"
}
```

A workflow failure must identify the artifact path it owns before it can be used as evidence against another lane.

---

## 3. Operator triage order

When many workflows fire on one commit:

1. Identify the target lane.
2. Read only the workflow that owns the target artifact.
3. Copy the machine JSON if available.
4. Treat unrelated failures as separate issues unless they cite the same path.

For C0001/C0002 replay, the target workflow is:

```text
MANUAL ONLY C0001 C0002 REPLAY REPORT
```

Target artifact:

```text
ci/c0001_c0002_replay_report.json
```

Target job:

```text
COPY JSON FROM THIS JOB ONLY
```

---

## 4. Machine-readable lane registry

```json
{
  "lanes": {
    "global": {
      "class": "A",
      "blocks_global_promotion": true,
      "blocks_local_corpus_promotion": false
    },
    "corpus": {
      "class": "B",
      "blocks_global_promotion": false,
      "blocks_local_corpus_promotion": true
    },
    "legacy_batch": {
      "class": "C",
      "blocks_global_promotion": "review_required",
      "blocks_local_corpus_promotion": false
    }
  }
}
```

---

## 5. Current C000 status

```json
{
  "C0001": "LOCKED",
  "C0002": "LOCKED_FROM_CI_SOURCE_HASH_DISCOVERY",
  "C0003": "BLOCKED_UNTIL_C0001_C0002_REPLAY_REPORT_PASS",
  "active_target_workflow": "MANUAL ONLY C0001 C0002 REPLAY REPORT"
}
```

---

## 6. Human doctrine

Do not chase red icons blindly.

A red icon is not evidence until it says:

- which artifact path failed,
- which invariant failed,
- which lane owns it,
- whether it blocks the current promotion target.

No ghost promotion. No ghost panic.
