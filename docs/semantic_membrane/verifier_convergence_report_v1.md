# verifier_convergence_report_v1

Status: FROZEN_CONVERGENCE_REPORT_SPEC  
Parent spec: `receipt_verifier_test_vectors_v1`  
Verifier: `receipt_verifier_contract_v1`  
Primitive: `SHOW_ME_THE_REPLAY`

## Purpose

This report proves that independent verifier engines produce identical outputs across the full conformance suite.

A legitimacy protocol is not complete unless its own verification layer converges.

## Required inputs

- `receipt_verifier_contract_v1`
- `receipt_verifier_test_vectors_v1`
- canonicalization profile
- engine implementation identifiers
- engine binary/source hashes
- conformance run outputs
- witness signatures

## Engine record

Each engine participating in the report MUST provide:

```json
{
  "engine_id": "",
  "engine_version": "",
  "implementation_language": "",
  "source_hash": "",
  "binary_hash": "",
  "canonicalization_profile": "",
  "operator_id": "",
  "run_timestamp_logical": ""
}
```

## Per-vector result

Each engine MUST emit one result per test vector:

```json
{
  "engine_id": "",
  "test_vector_id": "",
  "status": "VALID | INVALID",
  "failure_state": null,
  "recomputed": {
    "lineage_hash": "",
    "trace_bundle_hash": "",
    "fork_type": "",
    "weighted_delta_H": null
  },
  "result_hash": "HASH(canonical_result)"
}
```

## Convergence rule

For each `test_vector_id`, all participating engines MUST produce byte-identical canonical results except for engine metadata fields explicitly excluded from the result hash.

If any engine diverges, the report MUST return:

```json
{
  "convergence_status": "FAILED",
  "failure_state": "ENGINE_DIVERGENCE_DETECTED"
}
```

## Report envelope

```json
{
  "report_id": "verifier_convergence_report_v1",
  "status": "PASSED | FAILED",
  "verifier_contract": "receipt_verifier_contract_v1",
  "test_vector_suite": "receipt_verifier_test_vectors_v1",
  "engine_count": 0,
  "engine_records": [],
  "vector_results_root": "",
  "divergence_records": [],
  "witness_signatures": []
}
```

## Failure states

- ENGINE_DIVERGENCE_DETECTED
- TEST_VECTOR_MISSING
- RESULT_HASH_MISMATCH
- CANONICALIZATION_PROFILE_MISMATCH
- ENGINE_SOURCE_HASH_MISSING
- WITNESS_SIGNATURE_FAILED

## Validity condition

A convergence report is valid only if:

1. every required test vector is executed by every engine,
2. every result hash converges per vector,
3. every engine declares source and/or binary hash,
4. canonicalization profiles match,
5. witness signatures verify.

## Canon line

Legitimacy verification must itself be replay-verifiable.
