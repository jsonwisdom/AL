# SPEC_ARCADE_PROVER_V0.1.0

Title: PROVER_AGGREGATION_SERVICE Boundary Requirements

Status: GOVERNANCE_READY_BACKEND_BLOCKED

## Hydration Module

Input: raw LeafPreimage JSON from arcade/zk/witnesses/

Rules:
- Validate against LEAF_PREIMAGE_V2 before computation.
- Serialize fields in exact order:
  player_id, episode_id, fragment_id, replay_count, egg_id.
- On failure, emit ERROR_HYDRATION_FAILURE.
- On failure, emit zero proof artifacts.

## Execution Module

Rules:
- Treat nargo as an untrusted guest.
- Execute with only Prover.toml and circuit artifacts accessible.
- Same input must produce same witness and completion_hash.
- Completion hash must match declared state transition.

## Artifact Module

Output:
- PROVER_OUTPUT_INTENT
- public inputs
- proof_hash when backend exists
- data_sha256
- backend_state

## Ledger Semantics

The service may not write directly to zk_audit_trail.jsonl.

Flow:
1. Service emits PROVER_OUTPUT_INTENT.
2. root-publisher validates signature or integrity.
3. root-publisher appends to ledger.

## Honest Red States

- INPUT_REJECTED
- ERROR_HYDRATION_FAILURE
- PROOF_INVALID
- SYSTEM_PENDING
- BLOCKED_BY_BACKEND
- COMPROMISED

No proof green may be claimed while bb/backend is absent.
