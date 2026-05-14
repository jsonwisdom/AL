# receipt_verifier_test_vectors_v1

Status: FROZEN_TEST_VECTOR_SPEC  
Parent spec: `docs/semantic_membrane/trace_receipt_schema_v1.md`  
Verifier: `receipt_verifier_contract_v1`  
Primitive: `SHOW_ME_THE_REPLAY`

## Purpose

This document defines the deterministic test vectors every public verifier implementation MUST pass before it can claim compliance with `receipt_verifier_contract_v1`.

The verifier is valid only if independent engines converge on the same output for the same receipt bundle.

## Required output shape

```json
{
  "verifier": "receipt_verifier_contract_v1",
  "test_vector_id": "",
  "status": "VALID | INVALID",
  "failure_state": null,
  "recomputed": {
    "lineage_hash": "",
    "trace_bundle_hash": "",
    "fork_type": "",
    "weighted_delta_H": null
  }
}
```

## Test vector classes

### TV_VALID_001_BASELINE_KATZ

Purpose: prove that a properly formed baseline receipt validates.

Expected result:

```json
{
  "test_vector_id": "TV_VALID_001_BASELINE_KATZ",
  "status": "VALID",
  "failure_state": null
}
```

Requirements:

- `receipt_id` recomputes.
- `CIC_v1_0` resolves.
- `Katz_test_v1_2` CDG IR resolves.
- `WORLD_1967_V1` resolves.
- `capability_root` resolves.
- `lineage_hash` recomputes.
- `trace_bundle_hash` recomputes.
- signatures verify.

### TV_VALID_002_SMITH_MINOR_FORK

Purpose: prove that Smith is classified as a C2 contraction `MINOR_FORK` when replayed against the declared parent.

Expected result:

```json
{
  "test_vector_id": "TV_VALID_002_SMITH_MINOR_FORK",
  "status": "VALID",
  "recomputed": {
    "fork_type": "MINOR_FORK"
  }
}
```

Requirements:

- parent receipt exists in `public_replay_receipt_index_v1`.
- delta_H recomputes against `baseline_vector_0_katz_1967`.
- dominant family delta is C2.
- fork type matches computed divergence.

### TV_INVALID_001_TRACE_HASH_MISMATCH

Purpose: prove the verifier fails closed when the receipt claims a trace hash that does not match replay.

Mutation:

- Change `trace_bundle_hash` without changing replay traces.

Expected result:

```json
{
  "test_vector_id": "TV_INVALID_001_TRACE_HASH_MISMATCH",
  "status": "INVALID",
  "failure_state": "TRACE_HASH_MISMATCH"
}
```

### TV_INVALID_002_LINEAGE_HASH_MISMATCH

Purpose: prove the verifier detects a mismatched semantics/world binding.

Mutation:

- Keep `rule_semantics_hash` stable.
- Swap `infra_context_hash` without recomputing `lineage_hash`.

Expected result:

```json
{
  "test_vector_id": "TV_INVALID_002_LINEAGE_HASH_MISMATCH",
  "status": "INVALID",
  "failure_state": "LINEAGE_HASH_MISMATCH"
}
```

### TV_INVALID_003_CAPABILITY_ROOT_UNRESOLVED

Purpose: prove the verifier rejects receipts that reference unavailable or unsigned capability roots.

Mutation:

- Reference a `capability_root` not present in the capability registry.

Expected result:

```json
{
  "test_vector_id": "TV_INVALID_003_CAPABILITY_ROOT_UNRESOLVED",
  "status": "INVALID",
  "failure_state": "CAPABILITY_ROOT_UNRESOLVED"
}
```

### TV_INVALID_004_FORK_TYPE_MISMATCH

Purpose: prove the verifier rejects semantic laundering by label.

Mutation:

- Claim `fork_type: PATCH` for a receipt whose replay produces non-zero meaningful ΔH.

Expected result:

```json
{
  "test_vector_id": "TV_INVALID_004_FORK_TYPE_MISMATCH",
  "status": "INVALID",
  "failure_state": "FORK_TYPE_MISMATCH"
}
```

### TV_INVALID_005_SIGNATURE_VERIFICATION_FAILED

Purpose: prove the verifier rejects receipts without valid witness signatures.

Mutation:

- Alter receipt body after signing, or provide an invalid validator signature.

Expected result:

```json
{
  "test_vector_id": "TV_INVALID_005_SIGNATURE_VERIFICATION_FAILED",
  "status": "INVALID",
  "failure_state": "SIGNATURE_VERIFICATION_FAILED"
}
```

### TV_INVALID_006_OPEN_SURFACE_UNDECLARED

Purpose: prove the verifier rejects receipts that rely on unresolved capability domains without declaring them.

Mutation:

- Replay a C4 behavioral inference scenario while omitting `C4_behavioral_inference` from `open_surfaces` or declared handled surfaces.

Expected result:

```json
{
  "test_vector_id": "TV_INVALID_006_OPEN_SURFACE_UNDECLARED",
  "status": "INVALID",
  "failure_state": "OPEN_SURFACE_UNDECLARED"
}
```

## Conformance rule

An implementation may claim `receipt_verifier_contract_v1` compliance only if all valid vectors return `VALID` and all invalid vectors return the exact expected failure state.

## Canon line

A verifier that cannot fail closed cannot guard legitimacy.
