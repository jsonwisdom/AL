# OPERATOR_IMPLEMENTATION_GUIDE_V1

Status: DRAFT_LOCKED
Derived From: REPUTATION_SPEC_V1
Purpose: make operator replaceability testable.

## Step 1 — Acquire canonical inputs

Input:
- declared source bytes
- declared receipt path
- declared transform manifest

Rules:
- UTF-8 where text is used
- LF line endings
- no BOM
- no hidden state
- no network reads during replay

Output:
- canonical_input_sha256
- source_manifest_sha256

## Step 2 — Declare transform manifest

Input:
- ordered transform list
- runtime invariants
- allowed tools

Rules:
- transforms must be deterministic
- transforms must be pure
- transform ordering must be fixed
- undeclared transforms require REFUSE

Output:
- transform_manifest_sha256

## Step 3 — Execute replay in sealed mode

Input:
- canonical inputs
- transform manifest
- environment invariants

Rules:
- no HTTP(S)
- no RPC
- no DNS
- no external filesystem reads
- no nondeterministic time reads

Output:
- replay_output_bytes
- replay_output_sha256

## Step 4 — Compare declared and replayed outputs

Input:
- canonical_output_sha256
- replay_output_sha256

Decision:
- PASS if hashes and canonical bytes match
- FAIL if replay output diverges
- REFUSE if admissibility conditions are violated

Output:
- verdict
- refusal_code if REFUSE
- failure_reason if FAIL

## Step 5 — Build canonical verdict envelope

Input:
- verdict
- claim_id
- canonical_input_sha256
- canonical_output_sha256
- replay_output_sha256
- receipt_sha256
- operator_identity
- git_commit
- environment
- service_contract_sha256

Rules:
- serialize with deterministic key ordering
- use UTF-8 LF
- compute verdict_sha256 over canonical verdict bytes

Output:
- REPLAY_VERDICT_SCHEMA_V1-compatible JSON
- verdict_sha256

## Step 6 — Publish and link ancestors

Input:
- verdict JSON
- receipt JSON
- git commit
- optional EAS attestation
- optional ENS pointers

Rules:
- payment receipt must remain separate from governance receipt
- testnet identifiers may be referenced but never inherited as mainnet identifiers
- any missing ancestor requires REFUSE

Output:
- git commit containing verdict/receipt
- transcript if ceremony-level adjudication is performed
- verifier exit code

## Required exit behavior

- 0 = PASS / admissible where all invariants converge
- nonzero = deterministic failure or refusal reason

## Compliance condition

An operator is compliant only if another verifier can reproduce the same verdict from the same canonical inputs without trusting the operator.

## Status

OPERATOR_IMPLEMENTATION_GUIDE_V1_DRAFT_LOCKED
OPERATOR_REPLACEABILITY_PATH_DEFINED
