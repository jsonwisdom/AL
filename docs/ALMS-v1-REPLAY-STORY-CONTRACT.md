# ALMS-v1-REPLAY-STORY-CONTRACT.md

```yaml
status: CANONICAL_CANDIDATE
surface_role: REPLAY_STORY_CONTRACT
epoch_id: ALMS_v1
global_state: NO_DRIFT
```

## 1. Purpose

This surface defines the canonical replay story contract for ALMS-v1.

Replay is the constitutional act of reconstructing the ancestry, equivalence checks, registry standing, and boundary conditions of a claim under the seated epoch.

Replay is not interpretation.

Replay is not inference.

Replay is a deterministic state machine.

Replay determines admissibility, not truth.

## 2. Hard Locks

```yaml
ALMS_v1_REPLAY_STORY_CONTRACT:
  replay_is_interpretation: false
  replay_is_state_machine: true
  network_access: prohibited
  missing_ancestor_inference: prohibited
  synthetic_continuity: prohibited
  output_role: admissibility_not_legitimacy
  global_state: NO_DRIFT
```

These locks are constitutional and MUST NOT be relaxed in ALMS-v1.

## 3. Replay Prohibitions

Replay MUST refuse if any of the following are attempted:

- Network access: replay MUST NOT fetch remote resources.
- Missing ancestor inference: replay MUST NOT invent or assume missing receipts.
- Synthetic continuity: replay MUST NOT fill in gaps in lineage.
- Equivalence inference: replay MUST NOT infer equivalence beyond declared `class_id` values.
- Epoch mutation: replay MUST NOT accept any attempt to mutate a closed epoch.

## 4. Replay Phases

Replay consists of three deterministic phases, executed in order.

### 4.1 Phase 1 — Structural Reconstruction

- Parse provenance.
- Build declared ancestry DAG.
- Validate:
  - no missing parents,
  - no cycles,
  - no undeclared determinism classes.

### 4.2 Phase 2 — Equivalence Enforcement

For each declared equivalence step:

- Load `class_id` from v1 Equivalence Classes.
- Validate:
  - class exists,
  - predicate substrate is allowed,
  - predicate is total,
  - test vectors exist.
- Apply predicate to `{lhs, rhs}`.
- Reject on predicate failure.

### 4.3 Phase 3 — Registry & Boundary Enforcement

- Confirm operator standing under v1 Registry Charter.
- Confirm jurisdiction.
- Confirm no mutation of closed epoch surfaces.
- Confirm `epoch_id` matches `ALMS_v1`.

Replay completes only if all phases succeed.

## 5. Canonical Replay Story Object

Replay MUST emit a single canonical JSON object with the following shape:

```json
{
  "object": "ALMS_REPLAY_STORY_V1",
  "epoch_id": "ALMS_v1",
  "status": "REPLAYABLE",
  "claim_hash": "sha256:<64-hex>",
  "provenance_hash": "sha256:<64-hex>",
  "ancestry": [],
  "equivalence_checks": [],
  "registry_checks": [],
  "boundary_checks": [],
  "replay_story_hash": "sha256:<64-hex>"
}
```

### 5.1 Field Semantics

- `object`: MUST be exactly `ALMS_REPLAY_STORY_V1`.
- `epoch_id`: MUST match the seated epoch.
- `status`: MUST be `REPLAYABLE` if and only if all replay phases succeed.
- `claim_hash`: SHA-256 of the canonical serialization of the claim or receipt.
- `provenance_hash`: SHA-256 of the canonical serialization of the provenance file.
- `ancestry`: canonical ordered list of ancestor receipts.
- `equivalence_checks`: canonical ordered list of equivalence predicate evaluations.
- `registry_checks`: canonical ordered list of operator standing validations.
- `boundary_checks`: canonical ordered list of boundary and epoch immutability validations.
- `replay_story_hash`: SHA-256 of the canonical serialization of the entire replay story object with this field set to `""` during computation.

## 6. Canonical Ordering Rules

Replay MUST use deterministic ordering:

- `ancestry`: ordered from root to leaf.
- `equivalence_checks`: ordered in the sequence declared in provenance.
- `registry_checks`: ordered by the order in which operators appear in the replay story.
- `boundary_checks`: ordered by the order in which boundary constraints are evaluated.

No other ordering is permitted.

## 7. Failure Mapping

Replay MUST map failures to refusal codes exactly as follows:

```text
missing parent        REFUSE-PROV-003
cycle detected        REFUSE-PROV-004
unknown class_id      REFUSE-EQ-001
predicate failure     REFUSE-REPLAY-001
execution log missing REFUSE-REPLAY-002
closed epoch mutate   REFUSE-MUTATION-001
```

No other mappings are allowed.

No additional refusal codes may be introduced in ALMS-v1.

## 8. Replay Does Not Prove Truth

Replay MUST NOT be interpreted as a truth claim.

Replay proves only:

```text
The claimant supplied a lawful, reconstructable story under the seated epoch.
```

Replay does not:

- validate real-world facts,
- assert correctness of outputs,
- assert legitimacy of claims,
- or resolve conflicts.

Replay is admissibility, not judgment.

## 9. Constitutional State

```yaml
epoch_id: ALMS_v1
replay_story_contract: CLOSED
replay_is_state_machine: true
network_access: prohibited
synthetic_continuity: prohibited
output_role: admissibility_not_legitimacy
global_state: NO_DRIFT
```

End of ALMS-v1-REPLAY-STORY-CONTRACT.md
