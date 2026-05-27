# Base MCP Engine Audit V0.1

## Constitutional Invariants

- semantic_inference = false
- authority = false
- replayability over narrative
- append-only receipts

## Authorized Operations

- Canonical Anchoring
- Integrity Verification
- Availability Enforcement
- State Differencing
- Peer Replay Synchronization
- Forensic Proof Emission

## Refusal Conditions

- UNBOUNDED_PACKET
- MISSING_CAPABILITY_METADATA
- UNAUTHORIZED_TOOL
- SEMANTIC_AUTHORITY_REQUEST
- MUTATION_WITHOUT_RECEIPT

## Base Witness Layer

Base witnesses Merkle roots only.
Bulk receipts remain off-chain.

## Batch Flow

1. Emit MCP audit receipts
2. Validate receipts against schema
3. Build Merkle root
4. Emit batch manifest
5. Attest root on Base using EAS
