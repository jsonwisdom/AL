# ALMS ENS Pointer Manifest V1

Status: FROZEN
Version: ALMS_ENS_POINTER_V1
Boundary: Browser-signed ENS text pointer only

## 1. Purpose

The ALMS ENS Pointer Manifest V1 defines the canonical structure for mapping verified ALMS batch roots to public ENS text-record keys.

The pointer manifest proves:

- which ENS text key is intended
- which epoch it represents
- which batch root it points to
- which local batch manifest it binds to
- whether browser execution has submitted the pointer

It does not perform RPC, signing, chain contact, or wallet execution.

## 2. Canonicalization

All compliant implementations MUST canonicalize the pointer manifest with:

```bash
jq -cS '.' _truth/ens/alms_ens_pointers.json
```

No non-canonical representation is authoritative.

## 3. Canonical File

The canonical pointer manifest path is:

```text
_truth/ens/alms_ens_pointers.json
```

Initial state MUST be an empty array:

```json
[]
```

Entries are populated only after batch verification passes.

## 4. Pointer Entry Shape

Each pointer entry MUST contain exactly these keys:

```text
batch_manifest
batch_root
basescan_url
chain
ens_key
epoch
owner
status
tx_hash
value
version
```

No extra keys are allowed.

## 5. Field Rules

### version

MUST equal integer:

```text
1
```

### owner

MUST equal the canonical ENS identity root selected by the operator.

Example:

```text
jaywisdom.base.eth
```

### chain

MUST equal:

```text
base
```

### epoch

MUST use quarter form:

```text
YYYY-QN
```

Example:

```text
2026-Q2
```

### ens_key

MUST follow the frozen ENS key convention in Section 6.

### value

MUST equal `batch_root` exactly.

### batch_root

MUST match:

```text
^0x[0-9a-f]{64}$
```

### batch_manifest

MUST be the basename or canonical relative path to the verified local batch manifest.

Example:

```text
_truth/attest/batch/alms_batch_2026-Q2.json
```

### status

Allowed values:

```text
NOT_SUBMITTED
SUBMITTED
```

### tx_hash

If `status` is `NOT_SUBMITTED`, MUST be null.

If `status` is `SUBMITTED`, MUST match:

```text
^0x[0-9a-fA-F]{64}$
```

### basescan_url

If `status` is `NOT_SUBMITTED`, MUST be null.

If `status` is `SUBMITTED`, MUST match:

```text
^https://(www\.)?basescan\.org/tx/0x[0-9a-fA-F]{64}$
```

## 6. ENS Key Naming Convention — FROZEN

Rules:

1. Prefix: `witness.alms.` — literal
2. Chain: `base` — lowercase, canonical
3. Epoch: `YYYY.QN` — dot-separated, not hyphenated
4. No subdomains
5. No suffixes
6. No versioning in key

Pattern:

```text
^witness\.alms\.base\.[0-9]{4}\.Q[1-4]$
```

Example:

```text
witness.alms.base.2026.Q2
```

Properties:

- collision-proof
- lexicographically sortable
- predictable
- stable

## 7. ENS Value Format — FROZEN

Value is exactly the batch root:

```text
0x + 64 lowercase hex chars
```

Forbidden:

- JSON
- metadata
- wrappers
- prefixes beyond `0x`
- suffixes
- alternate encoding

Reason: minimal attack surface and maximal verifier compatibility.

## 8. Invariants Enforced by Verifier

`scripts/verify_alms_ens_pointer.sh` MUST check:

1. `ens_key` matches `witness.alms.base.YYYY.QN`
2. `ens_key` epoch matches `epoch` field
3. `batch_root` equals the referenced batch manifest `batch_root`
4. `batch_root` equals recomputed Merkle-derived batch root from witnesses
5. TX discipline: if `SUBMITTED`, `tx_hash` and `basescan_url` are required
6. No extra keys
7. `value` equals `batch_root` exactly

Failure modes include:

```text
FAIL invalid_pointer_manifest_json
FAIL invalid_pointer_keys
FAIL invalid_ens_key
FAIL epoch_mismatch
FAIL batch_root_mismatch
FAIL value_mismatch
FAIL invalid_tx_status
FAIL tx_required_when_submitted
FAIL tx_forbidden_when_not_submitted
```

## 9. Forbidden

A V1 ENS pointer manifest MUST fail validation for:

1. Extra keys at pointer-entry level
2. Missing required keys
3. `_comment`, `comment`, `description`, or `notes` fields anywhere
4. ENS keys outside the frozen naming convention
5. Values that are not exact batch roots
6. JSON-encoded ENS values
7. Terminal-submitted signing metadata
8. RPC-derived state inside the pointer manifest

## 10. Mutation Policy

Once frozen, this schema cannot change in place.

Any incompatible change requires:

1. New version: `ALMS_ENS_POINTER_V2`
2. New verifier script or explicit version gate
3. Governance justification against Issue #28

No in-place edits to V1.

## 11. Boundary Statement

ENS layer introduces:

- no new trust
- no new mutation paths
- no new execution surfaces
- no RPC
- no signing from terminal

Terminal generates calldata only.
Browser signs `setText`.
GitHub stores receipt.
ENS anchors public identity.
