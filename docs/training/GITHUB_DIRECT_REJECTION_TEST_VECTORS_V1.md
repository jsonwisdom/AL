# GitHub Direct Rejection Test Vectors V1

## Purpose

This document records canonical rejection and acceptance behavior for GitHub Direct receipt verification.

It is documentation-only. It does not advance governance lineage, seal an epoch, activate a proposal, or close any open SHA-256 gate.

## Machine State

```json
{
  "object": "GITHUB_DIRECT_REJECTION_TEST_VECTORS_V1",
  "type": "documentation_test_vectors",
  "epoch_0002": "MINTED_PENDING_EXTERNAL_SHA256",
  "global_state": "NO_DRIFT"
}
```

## Acceptance Vector

### A1 — commit_pinned_raw_url

```json
{
  "id": "A1",
  "class": "acceptance",
  "input": "https://raw.githubusercontent.com/jsonwisdom/AL/<40-char-commit-sha>/<path>",
  "requirement": "URL contains a full 40-character commit SHA and returns raw bytes.",
  "verification": "curl -fsSL <url> | sha256sum",
  "expected_result": "ACCEPT_FOR_SHA256_GATE"
}
```

## Rejection Vectors

### R1 — ao_link

```json
{
  "id": "R1",
  "class": "surface_error",
  "example": "https://ao.link/#/message/...",
  "rejection_reason": "AO message link, not Arweave mainnet data transaction or GitHub commit-pinned raw byte surface.",
  "expected_result": "REJECT"
}
```

### R2 — testnet_tx

```json
{
  "id": "R2",
  "class": "surface_error",
  "example": "Any transaction ID from a testnet gateway or faucet surface.",
  "rejection_reason": "Testnet transaction, not mainnet permanent storage or commit-pinned raw byte surface.",
  "expected_result": "REJECT"
}
```

### R3 — folder_manifest_or_drive_link

```json
{
  "id": "R3",
  "class": "surface_error",
  "example": "ArDrive folder, manifest ID, or application-layer drive link.",
  "rejection_reason": "Application-layer wrapper; bytes are not directly established as the target raw object.",
  "expected_result": "REJECT"
}
```

### R4 — branch_name

```json
{
  "id": "R4",
  "class": "surface_error",
  "example": "https://raw.githubusercontent.com/jsonwisdom/AL/master/<path>",
  "rejection_reason": "Mutable branch reference, not commit-pinned.",
  "expected_result": "REJECT"
}
```

### R5 — blob_sha_only

```json
{
  "id": "R5",
  "class": "surface_error",
  "example": "Git blob SHA without the commit SHA that contains it.",
  "rejection_reason": "Blob SHA identifies file content but does not bind the file to a repository state or commit-pinned raw URL.",
  "expected_result": "REJECT"
}
```

### R6 — non_commit_pinned_url

```json
{
  "id": "R6",
  "class": "surface_error",
  "example": "Any URL that does not contain a 40-character commit SHA.",
  "rejection_reason": "Surface is not permanently pinned to a Git commit.",
  "expected_result": "REJECT"
}
```

### R7 — placeholder_like_sha256

```json
{
  "id": "R7",
  "class": "hash_error",
  "example": "7b28f5a7a9f1dc2e6c3b8d5e0f4a6c9d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
  "rejection_reason": "Patterned hex sequence; not credible as SHA-256 output from actual raw bytes.",
  "expected_result": "REJECT"
}
```

### R8 — declarative_agent_self_attestation

```json
{
  "id": "R8",
  "class": "hash_error",
  "example": "Any SHA-256 asserted by a chat/declarative agent without external execution.",
  "rejection_reason": "No external execution surface; violates External Verifier Gate.",
  "expected_result": "REJECT"
}
```

## Invariants

1. Branch URLs are pointers, not receipts.
2. Blob SHAs are not commit SHAs.
3. Commit-pinned raw bytes are the GitHub Direct receipt surface.
4. SHA-256 gates require an external execution surface.
5. Placeholder-like or inferred hashes are rejected.
6. No governance transition advances while a required SHA-256 gate is open.

## Current Open Gate

```text
EPOCH_0002_SHA256=<64-hex>
```

This document does not satisfy or close that gate.
