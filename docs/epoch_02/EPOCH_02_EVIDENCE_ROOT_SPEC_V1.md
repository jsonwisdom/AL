# EPOCH 02 — Evidence Root Spec v1

## Purpose

Define the canonical, deterministic, closed-world rules for constructing the `evidence_root`, the cryptographic commitment that binds:

- evidence
- ordering
- canonicalization
- admissibility
- replay determinism
- taint propagation
- observer nonconformance
- kernel execution

The `evidence_root` is the lowest-level constitutional anchor in the Digital ABI Domain.

---

## 1. Evidence Item Admissibility

An evidence item is admissible only if:

1. It is valid UTF-8.
2. It is canonicalized using JCS / RFC 8785.
3. It conforms to the schema declared for the epoch.
4. It contains no forbidden fields.
5. It contains no nested structures unless explicitly allowed.
6. It is environment-independent.
7. It is byte-stable under replay.

If any condition fails:

```text
evidence_item -> INVALID
schema_check -> INVALID
verdict -> NOT_A_VERDICT
```

No observer may repair, normalize, or reinterpret evidence.

---

## 2. Canonical Evidence Item Serialization

All evidence items MUST be serialized using:

```text
JCS / RFC 8785 canonical JSON
```

This ensures:

- deterministic field ordering
- deterministic whitespace
- deterministic encoding
- deterministic hashing

No alternate serialization is admissible.

---

## 3. Deterministic Ordering Rule

Evidence items MUST be ordered lexicographically by:

```text
sha256(canonical_evidence_item_bytes)
```

This ordering rule is:

- deterministic
- environment-independent
- observer-independent
- replay-reconstructible

No observer may reorder evidence.
No operator may reorder evidence.
No kernel may reorder evidence.

---

## 4. Leaf Hash Construction

Each evidence item produces a leaf hash:

```text
leaf_hash = sha256(0x00 || canonical_evidence_item_bytes)
```

The `0x00` prefix prevents ambiguity with internal nodes.

---

## 5. Merkle Tree Construction

Internal nodes are constructed as:

```text
node_hash = sha256(0x01 || left_child_hash || right_child_hash)
```

Rules:

- Always pair left then right.
- If odd number of leaves, duplicate the last leaf.
- Tree is binary and complete.
- No alternate tree shapes are permitted.

---

## 6. Evidence Root Definition

The `evidence_root` is:

```text
root_hash of the canonical Merkle tree
constructed from all admissible evidence items
ordered lexicographically by leaf_hash
```

This is the canonical commitment for the epoch.

Core invariant:

```text
same evidence set + same ordering rule + same canonicalization
-> same evidence_root
```

---

## 7. Inclusion Proof Format

An inclusion proof MUST contain exactly:

```json
{
  "leaf_hash": "<sha256>",
  "path": ["<sha256>", "<sha256>"],
  "positions": ["L", "R"]
}
```

Rules:

- `path.length == tree_height`.
- `positions.length == path.length`.
- `positions` define left/right sibling placement.
- No compression is permitted.
- No alternate formats are admissible.

Replay must reconstruct the root from the proof exactly.

---

## 8. Exclusion and Taint Handling

### 8.1 Exclusion

If an evidence item is inadmissible:

- it is excluded from the tree
- it contributes no leaf
- it cannot be included by operator override
- it cannot be normalized or repaired

### 8.2 Taint

If an observer is tainted:

- all evidence emitted by that observer is tainted
- tainted evidence is excluded
- tainted evidence cannot be used in quorum
- tainted evidence cannot be included in the Merkle tree

Replay must enforce this.

---

## 9. Replay Reconstruction Obligations

Replay must:

1. Recompute canonical evidence bytes.
2. Recompute leaf hashes.
3. Recompute ordering.
4. Recompute tree structure.
5. Recompute `evidence_root`.
6. Validate inclusion proofs.
7. Validate exclusion.
8. Validate taint propagation.

If replay cannot reproduce the `evidence_root`:

```text
REPLAY_EVIDENCE_MISMATCH -> HALT
```

Replay is the final arbiter.

---

## 10. Closure Property

This file defines the complete evidence root specification for Epoch 02.

No additional:

- evidence types
- ordering rules
- hashing rules
- tree shapes
- canonicalization modes
- proof formats

may be introduced at runtime.

Any unclassified behavior defaults to:

```text
EVIDENCE_INVALID -> schema_check = INVALID -> NOT_A_VERDICT
```

Fail closed, never open.
