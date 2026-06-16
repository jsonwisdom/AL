# ALMS Batch Manifest V1

Status: FROZEN
Version: ALMS_BATCH_V1
Boundary: Offline deterministic aggregation only

## 1. Purpose

The ALMS Batch Manifest V1 format defines the canonical structure for committing a fixed set of witness files into one deterministic batch root.

A V1 manifest proves:

- which witness files are included
- the exact order of inclusion
- each witness canonical hash
- the Merkle root over those witnesses
- the final batch root committed for anchoring

It does not prove chain submission. Chain state remains external and browser-only.

## 2. Canonicalization

All compliant implementations MUST canonicalize the manifest with:

```bash
jq -cS '.' manifest.json
```

Witness files MUST be canonicalized with:

```bash
jq -cS '.' witness.json
```

Field order in source files is not trusted. Canonical form is the only hash surface.

## 3. Required Top-Level Fields

A V1 manifest MUST contain exactly these top-level keys:

```text
batch_root
batch_type
boundaries
epoch
inputs
merkle
tx
version
```

No other top-level keys are allowed.

## 4. Required Object Shapes

### batch_type

MUST equal:

```text
ALMS_ATTESTATION_BATCH
```

### epoch

MUST equal the verifier epoch argument.

Example:

```text
2026-Q2
```

### version

MUST equal integer:

```text
1
```

### boundaries

MUST contain exactly:

```json
{
  "rpc": false,
  "signing": false,
  "chain_contact": false,
  "financial_surface": false,
  "execution_surface": "offline_terminal_math_only"
}
```

### inputs

MUST contain exactly:

```json
{
  "witness_files": [],
  "count": 0,
  "hash_algorithm": "sha256",
  "canonicalization": "jq -cS",
  "ordering": "LC_ALL=C filename sort"
}
```

Rules:

- `witness_files` is a non-empty array of unique strings.
- Each witness file is a basename only.
- No `/`, `..`, empty string, or relative path component is allowed.
- `count` MUST equal the length of `witness_files`.
- `witness_files` MUST already be sorted with `LC_ALL=C sort`.

### merkle

MUST contain exactly:

```json
{
  "construction": "binary_sha256_raw_32_byte_concat_duplicate_last_if_odd",
  "leaf_hashes": [],
  "root": "0x..."
}
```

Rules:

- `leaf_hashes` length MUST equal `inputs.count`.
- Every hash MUST match `^0x[0-9a-f]{64}$`.
- `root` MUST match `^0x[0-9a-f]{64}$`.

### batch_root

MUST match:

```text
^0x[0-9a-f]{64}$
```

The verifier MUST recompute:

```text
batch_root = sha256(raw_32_byte_merkle_root)
```

### tx

MUST contain exactly:

```json
{
  "status": "NOT_SUBMITTED",
  "tx_hash": null,
  "basescan_url": null
}
```

Allowed `status` values:

```text
NOT_SUBMITTED
SUBMITTED
```

Rules:

- If `status` is `NOT_SUBMITTED`, `tx_hash` MUST be null and `basescan_url` MUST be null.
- If `tx_hash` is present, it MUST match `^0x[0-9a-fA-F]{64}$`.
- If `basescan_url` is present, it MUST match `^https://(www\.)?basescan\.org/tx/0x[0-9a-fA-F]{64}$`.

## 5. Forbidden

A V1 manifest MUST fail validation for:

1. Extra fields at any specified object level.
2. Missing fields.
3. `_comment`, `comment`, `description`, or `notes` fields anywhere.
4. Relative paths in `inputs.witness_files`.
5. Path separators in `inputs.witness_files`.
6. Float timestamps or any `created_at` field.
7. Unsupported hash algorithms.
8. Unsupported Merkle construction.
9. Unsupported canonicalization.
10. Unsupported tx status.

## 6. Zero-Mutation Proof

Verifier MUST enforce tx-free reconstruction.

Compute:

```bash
jq -cS 'del(.tx)' manifest.json
```

Then rebuild the same tx-free object from verified witness inputs and recomputed roots.

If unequal:

```text
FAIL manifest_no_tx_mismatch
```

## 7. Strict Mode

When:

```bash
STRICT_MODE=1
```

Any JSON witness file present in the witness directory but absent from the manifest MUST fail:

```text
FAIL unexpected_witness_files_present
```

## 8. Mutation Policy

Once frozen, this schema cannot change in place.

Any incompatible change requires:

1. New spec: `ALMS_BATCH_V2`
2. New verifier script or explicit version gate
3. Governance justification against Issue #28

No in-place edits to V1.

## 9. Boundary

The manifest format introduces:

- no RPC
- no signing
- no chain contact
- no financial surface
- no browser execution requirement

Terminal remains math only.
Browser remains the only signing surface.
