# MEDIA_MESH_V1 Public Verification Guide

## Purpose

MEDIA_MESH_V1 is a portable receipt system for verifying that media-derived artifacts match their recorded, batched, and anchored state.

It does not prove that a media claim is true. It proves that a recorded artifact:

1. existed in canonical form,
2. was included in a Merkle batch,
3. matched a batch root,
4. matched an anchor record when anchor metadata is present,
5. can be independently replayed.

## Core Rule

```txt
Truth is not asserted.
Artifacts are replayed.
```

## What This System Does

MEDIA_MESH_V1 converts source observations into deterministic artifacts:

```txt
watcher -> extractor -> drift -> cluster -> break -> merged receipt -> batch -> proof -> bundle -> verifier
```

Every layer emits canonical JSON using `jq -cS`.
Every hash is computed over exact bytes.
Every failure must be explicit.

## What This System Does Not Do

MEDIA_MESH_V1 does not:

- determine whether a news claim is true,
- assign credibility scores,
- infer intent,
- interpret motives,
- replace court records,
- treat Reddit, X, or social consensus as proof,
- make screenshots primary evidence,
- silently repair malformed input.

## Requirements

A verifier needs:

- Bash
- jq
- curl for source/network helpers when used
- sha256sum
- canonical JSON artifacts produced by MEDIA_MESH_V1

The core bundle verifier does not require network access.

## Verify a Portable Bundle

A portable bundle is the easiest public verification path.

Input:

```txt
bundle.json
```

Command:

```bash
bash watchers/media/bundle_verifier_v1.sh bundle.json
```

Expected success:

```json
{"verify_status":"BUNDLE_VALID"}
```

The actual output includes the bundle ID, leaf hash, computed root, batch root, and timestamp.

If verification fails, the script emits `HARD_FAIL` with an explicit reason.

## What Bundle Verification Checks

`bundle_verifier_v1.sh` verifies:

1. the bundle is canonical JSON,
2. the embedded leaf recomputes to the declared leaf hash,
3. the Merkle proof reconstructs the batch root,
4. the batch root matches the proof root,
5. anchor metadata root matches the batch root when present,
6. all required hashes are 64-character lowercase SHA-256 hex strings.

A bundle is rejected if any binding fails.

## Verify a Single Merkle Proof

Input:

```txt
proof.json
```

Command:

```bash
bash watchers/media/proof_verifier_v1.sh proof.json
```

This checks only:

```txt
leaf_hash + sibling path -> expected_root
```

It does not recompute the leaf from the receipt.

## Generate a Proof for a Leaf

Input:

```txt
merged.jsonl
leaf_index
batch.json optional
```

Command:

```bash
bash watchers/media/batch_proof_v1.sh merged.jsonl 0 batch.json > proof.json
```

The output contains:

- `leaf_hash`
- `sibling_hashes[]`
- `positions[]`
- `computed_root`
- `root_match`

## Verify a Batch Offline

Input:

```txt
merged.jsonl
anchored_batch.json
```

Command:

```bash
bash watchers/media/anchor_verifier_v1.sh merged.jsonl anchored_batch.json
```

This recomputes the batch locally and compares it to the provided anchor-format batch object.

Statuses:

```txt
MATCH
MISMATCH
HARD_FAIL
```

A mismatch reports the exact fields that failed.

## Verify an Anchor Through ENS/EAS

The network wrapper remains thin by design.

Command shape:

```bash
export MEDIA_MESH_RESOLVE_ENS_CMD="your_ens_resolver"
export MEDIA_MESH_FETCH_EAS_CMD="your_eas_fetcher"

bash watchers/media/anchor_verifier_v1_net.sh \
  merged.jsonl \
  media-mesh.alms.eth \
  media_mesh_latest_batch_v1 \
  <EAS_SCHEMA_UID>
```

The network wrapper:

1. resolves ENS to an EAS attestation UID,
2. fetches EAS attestation data,
3. validates schema UID and revoked status,
4. converts attestation fields into `anchored_batch.json`,
5. calls the offline verifier.

It does not perform Merkle logic.
It does not sign.
It does not mutate state.

## Create a Portable Proof Bundle

Inputs:

```txt
leaf.json
proof.json
batch.json
anchor.json
```

Command:

```bash
bash watchers/media/portable_proof_bundle_v1.sh \
  leaf.json \
  proof.json \
  batch.json \
  anchor.json > bundle.json
```

The bundle contains:

- embedded leaf,
- Merkle proof,
- batch summary,
- anchor metadata,
- bundle ID,
- leaf hash.

## Failure Means Something Specific

Failures are not vague.

Common examples:

| Failure | Meaning |
|---|---|
| `BUNDLE_NOT_CANONICAL` | The bundle bytes do not equal `jq -cS` canonical form. |
| `LEAF_HASH_RECOMPUTE_MISMATCH` | The embedded leaf does not hash to the declared leaf hash. |
| `PROOF_BATCH_ROOT_MISMATCH` | The proof root does not match the batch root. |
| `ANCHOR_BATCH_ROOT_MISMATCH` | Anchor metadata points to a different root. |
| `MERKLE_PROOF_ROOT_MISMATCH` | The proof path does not reconstruct the batch root. |
| `MISMATCH` | Offline replay completed but anchored fields differ. |

## Verification Philosophy

MEDIA_MESH_V1 is intentionally narrow.

It proves artifact integrity, not factual truth.
It proves inclusion, not correctness.
It proves replayability, not authority.

That boundary is the point.

## Minimal Public Claim

The strongest honest claim is:

```txt
This artifact can be independently replayed and checked against its recorded batch, proof, and anchor metadata.
```

Do not overstate it.

## Final Summary

MEDIA_MESH_V1 lets any verifier move from a portable bundle or local batch to an explicit result:

```txt
VALID / MATCH
or
INVALID / MISMATCH / HARD_FAIL with reason
```

No reputation required.
No private server required.
No operator trust required.

Only bytes, hashes, proofs, and replay.
