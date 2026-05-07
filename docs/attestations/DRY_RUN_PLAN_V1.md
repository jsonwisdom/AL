# DRY_RUN_PLAN_V1

Status: DRAFT_LOCKED
Purpose: pre-mainnet validation of admissibility mechanics for TRACK_001.

## 0. Objective

Run the full ceremony path without production mainnet activation.

The dry run MUST validate:

- canonical ordering and hashing
- environment sealing
- transform manifest integrity
- refusal semantics
- independent replay
- transcript emission
- schema validation

## 1. Required frozen inputs

- REPUTATION_SPEC_V1
- VERIFIER_SERVICE_CONTRACT_V1
- REPLAY_VERDICT_SCHEMA_V1
- OPERATOR_IMPLEMENTATION_GUIDE_V1
- TRACK_001_MAINNET_CEREMONY_CHECKLIST_V1
- TRACK_001_CEREMONY_TRANSCRIPT_SCHEMA
- TRACK_001_MAINNET_RECEIPT_SCHEMA
- ens_keymap.json

## 2. Positive path

1. Build dry-run payload.
2. Compute payload SHA-256.
3. Build dry-run receipt.
4. Compute receipt SHA-256.
5. Run verifier in no-network mode.
6. Require exit code 0.
7. Emit transcript.
8. Validate transcript against schema.
9. Commit transcript.

## 3. Negative tests

Each negative test MUST produce deterministic REFUSE or FAIL output.

### 3.1 Undeclared transform

Inject a transform not listed in the manifest.
Expected: REFUSE / UNDECLARED_TRANSFORM.

### 3.2 Missing ancestor

Remove or alter a required ancestor reference.
Expected: REFUSE / MISSING_ANCESTOR.

### 3.3 Network call

Attempt HTTP, RPC, DNS, or external network access during replay.
Expected: REFUSE / NETWORK_CALL_DURING_REPLAY.

### 3.4 Modified input

Mutate canonical input bytes after receipt creation.
Expected: FAIL / BYTE_DIVERGENCE.

## 4. Independent replay

A second operator or clean environment MUST reproduce the positive-path transcript and verifier exit code.

## 5. Promotion rule

Mainnet ceremony may proceed only after:

- positive path returns exit code 0;
- all negative tests return expected deterministic failures;
- transcript validates against schema;
- independent replay reaches the same verdict.

## 6. Status

DRY_RUN_PLAN_V1_DRAFT_LOCKED
MAINNET_ACTIVATION_BLOCKED_UNTIL_DRY_RUN_PASS
