# MEDIA MESH ANCHOR SPEC v1

## Purpose

Anchor one canonical Media Mesh batch summary as publicly verifiable state.

This spec anchors roots, not narratives. It makes no claims about truth, intent, liability, or outcome.

## Anchor Unit

Input object:

```json
{
  "batch_id": "sha256(merkle_root:leaf_count:timestamp_utc)",
  "leaf_count": 0,
  "merkle_root": "",
  "timestamp_utc": ""
}
```

Canonicalization:

```bash
canonical_batch="$(printf '%s\n' "$batch_json" | jq -cS .)"
batch_hash="$(printf '%s' "$canonical_batch" | sha256sum | awk '{print $1}')"
```

The `batch_hash` is the onchain batch identity.

## EAS Schema

Schema name:

```txt
MEDIA_MESH_BATCH_V1
```

Fields:

```txt
bytes32 batchId
bytes32 merkleRoot
uint64 leafCount
string timestampUtc
```

Encoding:

- `batchId = 0x{batch_hash}`
- `merkleRoot = 0x{merkle_root}`
- `leafCount = batch.leaf_count`
- `timestampUtc = batch.timestamp_utc`

## ENS Pointer

Recommended ENS text record key:

```txt
media_mesh_latest_batch_v1
```

Recommended value:

```txt
EAS attestation UID for the latest anchored media batch
```

ENS gives the current head. EAS gives the historical trail.

## Anchor Flow

1. Produce batch summary with `watchers/media/batch_aggregator_v1.sh`.
2. Canonicalize the batch summary using `jq -cS`.
3. Compute `batch_hash = sha256(canonical_batch)`.
4. Submit EAS attestation using `MEDIA_MESH_BATCH_V1`.
5. Optionally update ENS text record with latest attestation UID.

## Verification Flow

Given an ENS name, EAS schema UID, and local `merged.jsonl`:

1. Resolve ENS text record to latest EAS attestation UID.
2. Fetch EAS attestation.
3. Recompute batch summary using `batch_aggregator_v1.sh`.
4. Canonicalize and hash local batch summary.
5. Verify:
   - local `batch_hash == batchId`
   - local `merkle_root == merkleRoot`
   - local `leaf_count == leafCount`

If all checks match, the local batch is identical to the anchored state.

## Machine State

```txt
MEDIA_MESH_V1:
  doctrine: LOCKED
  schema: LOCKED
  watcher: LIVE (v1.1)
  extractor: LIVE (v1)
  drift_engine: LIVE (v1)
  domain_cluster: LIVE (v1.1)
  break_detector: LIVE (v1)
  merged_receipt: LIVE (v1)
  batch_aggregator: LIVE (v1)
  anchor_spec: LOCKED (v1)
NEXT:
  anchor_publisher_v1
```
