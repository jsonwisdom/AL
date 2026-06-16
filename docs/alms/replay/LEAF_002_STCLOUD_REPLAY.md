# ALMS Leaf 002 Replay Guide — St. Cloud 2026 Budget

## Anchor

```json
{
  "alms_protocol": "ALMS_V1",
  "asset_id": "ST_CLOUD_CITY_BUDGET_FY2026_PROPOSED",
  "batch_id": "f574a8741d5ed0cc67310a686ac0ba59f132a98171e723ebf001081ba04c0d21",
  "leaf_id": "002",
  "payload_cid": "bafkreicv6zorahyi47hcg7tje24grvxzdmgko5ekbz6ewrcyj6ujvvoita",
  "payload_sha256": "55f65d101f08e7ce237e6926b868d6f91b0ca7748a0e7c4b44584fa89ad5c898",
  "payload_size_bytes": 10240,
  "verified_fact": "2026 Total Revenues and Other Financing Sources = 75,784,400",
  "status": "PUBLIC_PAYLOAD_VERIFIED"
}
```

## Replay

```bash
curl -L -o stcloud_leaf002_replay_bundle.tar \
  "https://gateway.pinata.cloud/ipfs/bafkreicv6zorahyi47hcg7tje24grvxzdmgko5ekbz6ewrcyj6ujvvoita"

sha256sum stcloud_leaf002_replay_bundle.tar
wc -c stcloud_leaf002_replay_bundle.tar
```

Expected:

```txt
55f65d101f08e7ce237e6926b868d6f91b0ca7748a0e7c4b44584fa89ad5c898  stcloud_leaf002_replay_bundle.tar
10240 stcloud_leaf002_replay_bundle.tar
```

## Inspect bundle

```bash
mkdir -p replay_check
tar -xf stcloud_leaf002_replay_bundle.tar -C replay_check
find replay_check -type f | LC_ALL=C sort
sha256sum replay_check/manifest.json
cat replay_check/artifacts/artifact.jsonl
```

This guide is documentation only. The truth surface is the committed ledger entry plus the payload bytes referenced by CID.
