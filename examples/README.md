# MEDIA_MESH_V1 — Example Bundles

## Minimal Verification Surface

This directory contains three portable proof bundles for independent verification using the MEDIA_MESH_V1 toolchain.

These examples demonstrate deterministic success and failure conditions.

---

## Files

### `valid_bundle.json`

A fully consistent, untampered portable proof bundle.

- Leaf hash matches leaf content
- Merkle proof reconstructs the batch root
- Batch root matches anchor metadata (if present)
- Structure is canonical and hex-valid

Expected result:

```txt
verify_status: BUNDLE_VALID
```

---

### `invalid_bundle_tampered.json`

A valid bundle with one byte changed in the leaf content.
Hashes and proofs are not updated.

This tests leaf integrity.

Expected result:

```txt
verify_status: HARD_FAIL
reason: LEAF_HASH_RECOMPUTE_MISMATCH
```

---

### `invalid_bundle_bad_proof.json`

Leaf content and leaf hash are intact, but one sibling hash in the Merkle proof is corrupted.

This tests proof integrity.

Expected result:

```txt
verify_status: HARD_FAIL
reason: MERKLE_PROOF_ROOT_MISMATCH
```

---

## How to Verify

Run:

```bash
bash watchers/media/bundle_verifier_v1.sh <bundle.json>
```

The verifier is fully offline and deterministic.

It recomputes:

- leaf hash
- Merkle path
- batch root
- anchor consistency (if present)
- structural integrity

One failure means full rejection.

---

## What This Demonstrates

These bundles show:

- Consistency: valid bundle passes
- Tamper detection: modified leaf fails
- Proof correctness: bad Merkle path fails

No interpretation.
No heuristics.
No trust in the creator.

```txt
run it or don't
```
