# membrane_bootstrap_proof_v1

Status: FROZEN_BOOTSTRAP_PROOF_SPEC  
Primitive: `SHOW_ME_THE_REPLAY`  
Scope: initial semantic membrane lineage, verifier, conformance suite, and public surfaces

## Purpose

This artifact defines the proof surface for the initial introduction of the membrane itself.

A self-verifying legitimacy protocol must prove that its own bootstrap did not rely on hidden state, undeclared lineage, or unverifiable authority.

## Bootstrap claim

```json
{
  "bootstrap_claim": "MEMBRANE_INITIALIZED_WITH_DECLARED_ARTIFACTS_ONLY",
  "hidden_state_policy": "FORBIDDEN",
  "continuity_condition": "SIGNED_RECEIPT_OR_TYPED_FORK",
  "verification_primitive": "SHOW_ME_THE_REPLAY"
}
```

## Declared bootstrap artifacts

The bootstrap proof covers the introduction of:

- `CIC_v1_0`
- `CDG_IR_V0_1`
- `capability_receipt_layer_v1`
- `trace_receipt_schema_v1`
- `receipt_verifier_contract_v1`
- `receipt_verifier_test_vectors_v1`
- `verifier_convergence_report_v1`
- `lineage_diff_report_v1`
- `public_fork_lineage_graph_v1`
- `public_replay_receipt_index_v1`
- `public_capability_mismatch_report_v1`
- `fourth_amendment_privacy_lineage_v1`

## Required bootstrap fields

```json
{
  "bootstrap_id": "membrane_bootstrap_proof_v1",
  "artifact_set_root": "HASH(sorted(artifact_hashes))",
  "artifact_hashes": [],
  "creation_order": [],
  "parent_context": "",
  "operator_id": "",
  "repository": "jsonwisdom/AL",
  "commit_range": {
    "start": "",
    "end": ""
  },
  "declared_assumptions": [],
  "open_surfaces": [],
  "signatures": []
}
```

## Verification gates

A verifier MUST check:

1. every declared artifact resolves by content hash,
2. artifact creation order is declared,
3. no required artifact is missing from `artifact_set_root`,
4. every public surface references the correct primitive `SHOW_ME_THE_REPLAY`,
5. verifier contract and test vectors are included in the same bootstrap root,
6. convergence report references the declared verifier and test vector suite,
7. open surfaces are declared rather than silently absorbed,
8. signatures verify.

## Failure states

- BOOTSTRAP_ARTIFACT_MISSING
- BOOTSTRAP_HASH_MISMATCH
- BOOTSTRAP_ORDER_UNDECLARED
- VERIFIER_NOT_INCLUDED_IN_BOOTSTRAP
- TEST_VECTORS_NOT_INCLUDED_IN_BOOTSTRAP
- CONVERGENCE_REPORT_UNLINKED
- OPEN_SURFACE_UNDECLARED
- BOOTSTRAP_SIGNATURE_FAILED

## Valid output

```json
{
  "verifier": "membrane_bootstrap_proof_v1",
  "bootstrap_id": "",
  "status": "VALID | INVALID",
  "failure_state": null,
  "artifact_set_root": "",
  "checked_artifact_count": 0
}
```

## Canon line

A legitimacy protocol that cannot account for its own origin cannot demand replay from others.
