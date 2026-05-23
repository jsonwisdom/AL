# E05 ENS TXT Payload

Status: READY_FOR_ENS_PUBLICATION
Target Identity: jaywisdom.base.eth
Suggested TXT Key: E05

## Canonical TXT Value

```text
E05|FINALIZED|cid=bafkreieybfrnhy4qwkmgnjumt7xzmai5ms5u2cmm7kfhjmw5x4744qvpou|commit=5b69b24f9010d1f0817be3bd81479e24b58f0fa8|root=60e117e759cf1f19375233dd59a5eac6076b1f4b0d7fe5d07dc0352dd778141c
```

## Full Canonical JSON

```json
{
  "epoch": "E05",
  "status": "FINALIZED",
  "cid_sync": "VERIFIED_BY_OPERATOR",
  "commit": "5b69b24f9010d1f0817be3bd81479e24b58f0fa8",
  "root_hash_sha256": "60e117e759cf1f19375233dd59a5eac6076b1f4b0d7fe5d07dc0352dd778141c",
  "verification_path": "ipfs://bafkreieybfrnhy4qwkmgnjumt7xzmai5ms5u2cmm7kfhjmw5x4744qvpou",
  "artifact": "artifacts/epoch03/IMG_9629.png",
  "artifact_sha256": "36f3a099fe616ebd73f642b90d30b1dc9d05a4d65d8ad9e56070b36b55515b7e",
  "authority_model": "COMMIT_PLUS_BYTES_PLUS_HASH_PLUS_REPLAY_ONLY",
  "seal": "E05_FINALIZED_REPLAY_VERIFIABLE"
}
```

## Publication Rule

The ENS TXT record is a discovery pointer only. Authority remains with commit + bytes + hash + replay.

Seal: E05_ENS_TXT_READY_NO_AUTHORITY_PROMOTION
