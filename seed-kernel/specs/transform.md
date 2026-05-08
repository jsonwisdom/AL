# Transform Receipt Spec v0

A TransformReceipt is epistemic motion.

It records how one or more claims produced another claim.

## Fields

- `id`: SHA-256 hash of transform payload.
- `timestamp`: Unix timestamp.
- `input_claim_ids`: Ordered list of input claim hashes.
- `output_claim_id`: Output claim hash.
- `operation`: `assert | summarize | infer | revise | fork | merge | recalc`
- `operation_params`: Arbitrary JSON object.
- `policy`: `human:* | model:* | script:*`
- `signed_by`: List of actor ids.
- `signature`: Optional Ed25519 signature bytes.

## Constitutional Rule

Claims store state.

Transforms store epistemic motion.

Replay is deterministic re-execution from visible transforms.
