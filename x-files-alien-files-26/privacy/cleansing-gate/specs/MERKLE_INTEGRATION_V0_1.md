# Merkle Integration v0.1

## Purpose
Define branch-scoped Merkle commitments for approved memory fragments and Gray Baby creative transformations. The design supports replayable lineage verification, parallel branches, and fail-closed detection of mutation or cross-branch proof reuse.

## Status
- `SPECIFICATION_STATUS = DEFINED`
- `SCHEMA_INTEGRATION_STATUS = NOT_IMPLEMENTED`
- `VALIDATOR_IMPLEMENTATION_STATUS = NOT_IMPLEMENTED`
- `FIXTURES_006_007_STATUS = NOT_PRESENT`
- `TEST_SUCCESS = NOT_CLAIMED`
- `AUTHORITY = FALSE`

## Hash Representation
All hashes are lowercase hexadecimal strings of exactly 64 characters with no `0x` prefix.

## Domain Separation
The following UTF-8 prefixes are normative:

- `CG:LEAF:V0.1`
- `CG:NODE:V0.1`
- `CG:CREATIVE:V0.1`

## Canonicalization
Structured objects MUST be serialized with JCS (RFC 8785) before hashing.

## Approved Fragment Leaf
An approved source fragment is committed as:

```text
leaf_hash = SHA256(
  UTF8("CG:LEAF:V0.1") ||
  JCS({
    "fragment_sha256": "<64-hex>",
    "memory_tag": "REMEMBERED",
    "fragment_id": "<stable-id>"
  })
)
```

Requirements:

- `fragment_sha256` MUST be the SHA-256 digest of the raw approved fragment bytes.
- `memory_tag` MUST be `REMEMBERED` for source-memory leaves in v0.1.
- `fragment_id` MUST be stable, non-empty, and unique within the branch revision.

## Internal Node
Internal nodes preserve explicit left/right order:

```text
node_hash = SHA256(
  UTF8("CG:NODE:V0.1") ||
  left_child_hash_bytes ||
  right_child_hash_bytes
)
```

Lexicographic child sorting is forbidden in v0.1. Proofs MUST preserve sibling position.

## Creative Transformation Commitment
A Gray Baby transformation is committed as:

```text
creative_leaf = SHA256(
  UTF8("CG:CREATIVE:V0.1") ||
  JCS({
    "parent_root": "<64-hex>",
    "transformation_sha256": "<64-hex>",
    "content_tag": "IMAGINED",
    "branch_id": "<branch-context>"
  })
)
```

Requirements:

- `transformation_sha256` MUST bind the resulting creative artifact bytes.
- `content_tag` MUST be `IMAGINED` for v0.1 creative leaves.
- `branch_id` MUST equal the manifest root-level `branch_context`.

## Proof Object
A branch proof MUST include the selected leaf, ordered siblings, declared root, branch binding, and path depth.

```json
{
  "leaf_hash": "<64-hex>",
  "siblings": [
    {
      "position": "left",
      "hash": "<64-hex>"
    },
    {
      "position": "right",
      "hash": "<64-hex>"
    }
  ],
  "root": "<64-hex>",
  "branch_id": "<branch-context>",
  "depth": 2
}
```

Validation requirements:

- `depth` MUST equal the number of sibling entries.
- Each sibling MUST declare `left` or `right`.
- The path MUST be recomputed in listed order.
- Malformed, impossible, or ambiguous paths MUST fail closed.

## Branch Binding
Runtime validation MUST enforce:

```text
merkle.branch_id == branch_context
export_target.branch_id == branch_context
recomputed_root == merkle.root
```

A schema may require the fields, but runtime code is responsible for enforcing equality.

## Parallel Branches
Each branch maintains an independent root and proof set.

A shared ancestor root MAY be referenced as metadata, but:

- it does not replace the current branch root;
- it does not merge branch authority;
- one branch root MUST NOT silently replace another.

## Revocation and Successor Roots
Existing roots are immutable.

Revocation MUST be represented as an append-only event that produces a successor root:

```text
old_root = immutable
revocation_event = append-only
new_root = recomputed successor
prior_root = retained
```

The phrase `prune leaf` refers only to constructing the successor tree. It does not authorize mutation or deletion of historical roots.

## Runtime Validation Order

```text
SCHEMA
→ KEY_BINDING
→ SIGNATURE
→ TIME_WINDOW
→ BRANCH_BINDING
→ MERKLE_PROOF
→ FILE_HASHES
```

## Deterministic Error Mapping

| Pure Error | CLI Exit Code | Meaning |
| :--- | :--- | :--- |
| `MERKLE_MISMATCH` | 8 | Proof structure, path, branch, or recomputed-root failure |

`MERKLE_MISMATCH` includes:

- malformed proof structure;
- depth mismatch;
- invalid sibling direction;
- invalid hash format;
- branch mismatch;
- cross-branch proof reuse;
- recomputed-root mismatch;
- mutated-leaf detection.

## Negative Fixtures

### Fixture 006 — Mutated Leaf

Path:

```text
tests/cleansing_gate/fixtures/negative/fixture-006-merkle-mutated-leaf/
```

Expected result:

```text
REJECT
PURE_ERROR = MERKLE_MISMATCH
CLI_EXIT_CODE = 8
```

### Fixture 007 — Cross-Branch Proof Forgery

Path:

```text
tests/cleansing_gate/fixtures/negative/fixture-007-cross-branch-proof-forgery/
```

Expected result:

```text
REJECT
PURE_ERROR = MERKLE_MISMATCH
CLI_EXIT_CODE = 8
```

## Invariants

- `HISTORY_MUTATION = FALSE`
- `ROOT_REPLACEMENT_WITHOUT_SUCCESSOR_EVENT = FALSE`
- `PARALLEL_BRANCH_COLLAPSE = FALSE`
- `CROSS_BRANCH_PROOF_REUSE = REJECT`
- `TEST_SUCCESS = NOT_CLAIMED`
- `AUTHORITY = FALSE`
