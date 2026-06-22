# EAS Zora 1155 Field Order v0.1

Status: DRAFT_ONLY_NOT_REGISTERED

Purpose: lock the field order for the EAS Zora 1155 continuity proof before any schema registration, attestation, or mint.

This is a non-executable draft. It does not deploy contracts, register schemas, attest anything, or mint anything.

## Schema String

string tokenId,string zoraContract,string metadataURI,string continuityCommit,string receiptHash,string replayHash,string laneRoot,string zoraRef,bool isSoulbound,uint256 mintTimestamp

## Canonical Field Order

1. tokenId
2. zoraContract
3. metadataURI
4. continuityCommit
5. receiptHash
6. replayHash
7. laneRoot
8. zoraRef
9. isSoulbound
10. mintTimestamp

## Required Boundary

DRAFT_ONLY_NOT_REGISTERED -> DRY_RUN_PASS -> REGISTERED_UNVERIFIED -> VALIDATED

No status may skip a boundary.

## No Fake Green Rules

- This field-order draft is not a SchemaUID.
- This field-order draft is not an attestation.
- This field-order draft is not a Zora mint.
- This field-order draft does not confer authority.
- It may become replay-admissible only after a deterministic dry-run passes and a future SchemaUID is verified.
