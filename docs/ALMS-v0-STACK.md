# ALMS-v0-STACK — Constitutional Index

## 1. Status

ALMS-v0 is seated as a constitutional stack.

```json
{
  "ALMS_v0": {
    "status": "CONSTITUTIONAL_STACK_SEATED",
    "global_state": "NO_DRIFT"
  }
}
```

This document is the canonical index and front door for ALMS-v0. All referenced components are enacted law, not proposals.

## 2. Canonical Stack Overview

### 2.1 PROVENANCE — Lineage Legality

Defines:

- Recursive admissibility: a receipt is admissible only if all reachable ancestors are admissible.
- Deterministic ancestor selection: first failing ancestor is chosen by fixed hash-ordered traversal.
- Cycle rejection: any cycle in the provenance DAG renders the receipt inadmissible.
- FULL_RECURSIVE verification: parent verification must be replayable to raw receipts, not cached summaries.
- Taint propagation: taint is monotonic and inherited from ancestors.

Answers: what is inherited.

Spec anchor: `docs/ALMS-v0-PROVENANCE.md`

Constitutional hash: `PROVENANCE_SHA256_PLACEHOLDER`

### 2.2 REGISTRY — Jurisdiction and Revocation

Defines:

- Trust roots: which keys and constitutions have standing.
- Constitution registry: how constitutions are published, versioned, and revoked.
- Artifact registry: how models, runtimes, and schemas are registered and revoked.
- Replay windows: how long receipts remain replayable under a given registry state.
- Quorum semantics: how many signers and which sets are required for registry validity.

Answers: who has jurisdiction.

Spec anchor: `docs/ALMS-v0-REGISTRY.md`

Constitutional hash: `REGISTRY_SHA256_PLACEHOLDER`

### 2.3 EXECUTION — Deterministic Replay Law

Defines:

- Execution environment manifest: `exec_env_manifest` and `exec_env_hash`.
- Execution key: `(weight_hash, runtime_hash, decoding_graph_hash, exec_env_hash)`.
- Cache law: VALID / STALE / TAINTED / ABSENT states and mandatory invalidation triggers.
- Deterministic replay: two independent verifiers with the same exec key must produce bit-identical outputs and exit codes.
- Network isolation: no remote fetches after registry sync during replay.

Answers: what replay means.

Spec anchor: `docs/ALMS-v0-EXECUTION.md`

Constitutional hash: `EXECUTION_SHA256_PLACEHOLDER`

### 2.4 COURTROOM — Adjudication and Legitimacy

Defines:

- Admissibility vs persuasiveness: binary admissibility vs graded evidentiary weight.
- Taint lattice: CLEAN < WATCH < TAINTED < CONFLICTED < REFUSED.
- Conflict sets: handling of admissible but mutually inconsistent receipts.
- Deterministic refusal: when the courtroom must refuse to issue a substantive verdict.
- Evidentiary weight: deterministic function over admissible receipts and their taint, constitution, environment, quorum, and recency.

Answers: what may be spoken.

Spec anchor: `docs/ALMS-v0-COURTROOM.md`

Constitutional hash: `COURTROOM_SHA256_PLACEHOLDER`

## 3. Binding Relationships

The ALMS-v0 stack is strictly layered:

```text
PROVENANCE -> REGISTRY -> EXECUTION -> COURTROOM
```

- PROVENANCE determines whether a claim's lineage is intact.
- REGISTRY determines whether that lineage has jurisdiction.
- EXECUTION determines whether that lineage replays deterministically.
- COURTROOM determines what verdict, if any, may be issued.

Each layer is necessary; none is sufficient on its own.

No layer may override the invariants of a lower layer.

## 4. Constitutional Guarantees

ALMS-v0 enacts the following invariants:

- Replay supremacy: no claim is admissible unless its output can be replayed bit-for-bit from declared inputs under a known execution key.
- Jurisdictional clarity: no claim is admissible unless its constitutions, keys, and artifacts are valid in the registry at the claimed time.
- Lineage integrity: no claim is admissible unless every reachable ancestor receipt is admissible; provenance is a hard dependency.
- Execution as evidence: runtime, libraries, hardware features, and samplers are part of the execution key and cannot change without changing the claim.
- Adjudicative discipline: no claim is persuasive by virtue of cryptographic validity alone; persuasiveness is computed at the courtroom layer.
- Refusal as law: when taint, conflict, or instability prevent a legitimate verdict, deterministic refusal is a valid and required outcome.

These guarantees are not advisory. They are binding conditions for ALMS-v0 conformance.

## 5. v0 Closure

ALMS-v0 is closed and anchored by the following constitutional artifacts:

```json
{
  "ALMS_v0_closure": {
    "provenance_spec": {
      "path": "docs/ALMS-v0-PROVENANCE.md",
      "sha256": "PROVENANCE_SHA256_PLACEHOLDER"
    },
    "registry_spec": {
      "path": "docs/ALMS-v0-REGISTRY.md",
      "sha256": "REGISTRY_SHA256_PLACEHOLDER"
    },
    "execution_spec": {
      "path": "docs/ALMS-v0-EXECUTION.md",
      "sha256": "EXECUTION_SHA256_PLACEHOLDER"
    },
    "courtroom_spec": {
      "path": "docs/ALMS-v0-COURTROOM.md",
      "sha256": "COURTROOM_SHA256_PLACEHOLDER"
    },
    "conformance_suite": {
      "path": "alms-v0-conformance/",
      "description": "Canonical test vectors and CLI contracts for ALMS-v0 admissibility and replay."
    }
  }
}
```

Once the placeholders are replaced with actual SHA-256 digests of the referenced files, any modification to those files constitutes a constitutional change and must be treated as a versioned amendment, v1 or later, not an in-place edit.

## 6. v1 Boundary

ALMS-v1 may extend but may not modify ALMS-v0 invariants.

- No v1 artifact may weaken replay supremacy, lineage integrity, registry jurisdiction, or courtroom admissibility rules.
- Any change to v0 behavior must be expressed as a new versioned constitution or an explicit amendment document that coexists with, rather than overwrites, v0.

Planned v1 surfaces, non-binding at v0:

- `ALMS-v1-TREATIES.md` — cross-registry agreements and inter-jurisdictional rules.
- `ALMS-v1-AMENDMENTS.md` — formal constitutional evolution mechanisms.
- `ALMS-v1-MULTI-COURT.md` — federated and hierarchical court structures.
- `ALMS-v1-PUBLIC-OPINION-LEDGER.md` — replayable civic and institutional commentary.
- `ALMS-v1-CIVIC-MEMORY.md` — long-term, replayable institutional memory over receipts and verdicts.

Until v1 artifacts are minted, ALMS-v0 remains the complete and sole constitutional stack for admissible claims.
