# trace_receipt_schema_v1 / receipt_verifier_contract_v1

Status: FROZEN_FOR_EXECUTION_SPEC  
Membrane state: FULLY_OPERATIONAL_PROTOCOL_DEFINED  
Enforcement primitive: SHOW_ME_THE_REPLAY

## Purpose

This document defines the minimum public verifier contract for validating a constitutional semantic replay receipt end to end.

A trace receipt is not a narrative. It is a signed, content-addressed claim that one semantic transition replayed over a declared corpus, world root, capability root, and rule semantics hash.

## Core invariants

- NO_REPLAY_NO_DOCTRINE
- NO_TRACE_HASH_NO_CONTINUITY_CLAIM
- NO_SIGNED_RECEIPT_NO_LEGITIMACY_EVIDENCE

## Receipt envelope

```json
{
  "schema_id": "trace_receipt_schema_v1",
  "classification": "SIGNED_REPLAY_RECEIPT_ENVELOPE",
  "receipt_id": "HASH(canonical_receipt_without_signatures)",
  "parent_receipt_ids": [],
  "lineage_graph_id": "public_fork_lineage_graph_v1",
  "doctrine_node_id": "",
  "doctrine_root": "",
  "fork_type": "PATCH | MINOR_FORK | MAJOR_FORK | SOVEREIGNTY_SPLIT",
  "continuity_claim": true,
  "CIC_version": "CIC_v1_0",
  "world_root": "",
  "capability_root": "",
  "rule_semantics_hash": "",
  "infra_context_hash": "",
  "lineage_hash": "",
  "trace_bundle_hash": "",
  "entropy_vector": {
    "C1": null,
    "C2": null,
    "C3": null,
    "C4": null,
    "C5": null
  },
  "delta_H_profile": {
    "parent_node": "",
    "weighted_delta": null,
    "family_delta": {
      "C1": null,
      "C2": null,
      "C3": null,
      "C4": null,
      "C5": null
    }
  },
  "rights_surface_delta": {
    "direction": "REPAIR | EROSION | UNDERFIT | NEUTRAL | DIVERGENCE",
    "population_weight": null,
    "reversibility": null,
    "observability": null,
    "asymmetry": null
  },
  "open_surfaces": [],
  "mismatch_flags": [],
  "validator_set": [],
  "signatures": []
}
```

## Verifier contract

A public node implementing `receipt_verifier_contract_v1` MUST validate the following gates in order:

1. Parse and canonicalize the receipt using the declared canonicalization profile.
2. Recompute `receipt_id` from the canonical receipt excluding signatures.
3. Resolve `CIC_version` and confirm the canonical input corpus root.
4. Resolve `rule_semantics_hash` to canonical CDG IR.
5. Resolve `capability_root` to signed capability receipts.
6. Resolve `infra_context_hash` and confirm it matches the capability set for the declared world root.
7. Recompute `lineage_hash = H(rule_semantics_hash || infra_context_hash)`.
8. Replay all CIC scenarios required by the receipt scope.
9. Recompute `trace_bundle_hash` from replay traces.
10. Recompute `entropy_vector` and `delta_H_profile` against the declared parent.
11. Recompute fork classification and confirm it matches `fork_type`.
12. Verify every required signature in `validator_set`.
13. Emit `VALID` only if every gate passes.

## Failure states

A verifier MUST fail closed with one of:

- INVALID_RECEIPT_ID
- CIC_ROOT_UNRESOLVED
- RULE_SEMANTICS_UNRESOLVED
- CAPABILITY_ROOT_UNRESOLVED
- INFRA_CONTEXT_MISMATCH
- LINEAGE_HASH_MISMATCH
- TRACE_HASH_MISMATCH
- ENTROPY_PROFILE_MISMATCH
- FORK_TYPE_MISMATCH
- SIGNATURE_VERIFICATION_FAILED
- OPEN_SURFACE_UNDECLARED

## Valid output

```json
{
  "verifier": "receipt_verifier_contract_v1",
  "receipt_id": "",
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

## Canon line

SHOW_ME_THE_REPLAY means: provide executable legitimacy evidence or lose continuity standing.
