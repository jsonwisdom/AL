# TRACK_001_MAINNET_CEREMONY_CHECKLIST_V1

Status: DRAFT_LOCKED
Purpose: deterministic activation checklist for TRACK_001 mainnet ceremony.

## 0. Preconditions

- REPUTATION_SPEC_V1 is committed.
- VERIFIER_SERVICE_CONTRACT_V1 is committed.
- REPLAY_VERDICT_SCHEMA_V1 is committed.
- OPERATOR_IMPLEMENTATION_GUIDE_V1 is committed.
- TRACK_001_MAINNET_RECEIPT_SCHEMA is committed.
- TRACK_001_CEREMONY_TRANSCRIPT_SCHEMA is committed.
- ENS keymap is committed.
- TRACK_001 testnet receipt is committed.
- PR_86 remains untouched until mainnet verification succeeds.
- Ghost anchor flag remains false.

## 1. Preflight

- Build canonical mainnet payload.
- Generate deterministic nonce.
- Record issued_at_unix.
- Validate payload against preflight schema.
- Compute preflight hash.

## 2. Mainnet schema registration

- Register semantically equivalent schema on Base Mainnet.
- Record schema UID.
- Record schema tx hash.
- Verify chain ID 8453.

## 3. Mainnet attestation

- Submit one production attestation under the mainnet schema.
- Confirm attester equals operator wallet.
- Record attestation UID.
- Record attestation tx hash.

## 4. Receipt generation

- Build TRACK_001_MAINNET_RECEIPT.json.
- Include testnet reference as reference only.
- Do not inherit testnet identifiers as mainnet identifiers.
- Compute receipt SHA-256.
- Commit receipt to Git.

## 5. ENS update

- Update jaywisdom.base.eth text records using ens_keymap.json.
- Record schema UID, attestation UID, receipt commit, payload SHA-256, receipt SHA-256, and status.

## 6. Verification

- Run track001_verify.js.
- Require exit code 0 for admissibility.
- Any nonzero exit code blocks activation.

## 7. Transcript emission

- Emit ceremony transcript.
- Validate transcript against transcript schema.
- Commit transcript to Git.

## 8. Activation rule

TRACK_001 mainnet is real only if verifier exit code is 0 and the transcript records admissible=true.

## Status

TRACK_001_MAINNET_CEREMONY_CHECKLIST_V1_DRAFT_LOCKED
