# Family State Vault v1 — Hash Mismatch Blocked

Status: `HASH_MISMATCH_BLOCKED`

Vault v1 has a real IPFS folder CID:

```text
bafybeichf2q4fvxknpaq3v5g5gl5m76eiwzmadz6pgkamemhupvcfoolbm
```

But the local truth bytes and IPFS truth bytes have not yet been shown to converge.

## Rule

No manifest promotion, EAS payload generation, or onchain sealing occurs until:

```text
LOCAL_TRUTH == IPFS_TRUTH == MANIFEST
```

## Required operator evidence

Paste both hash sets and the canonical source decision:

```text
LOCAL_TRUTH
<sha256>  _truth/family_state/vault/vault_core_values_v1.md
<sha256>  _truth/family_state/vault/vault_emergency_protocol_v1.md
<sha256>  _truth/family_state/vault/vault_origin_story_v1.md

IPFS_TRUTH
<sha256>  vault_core_values_v1.md
<sha256>  vault_emergency_protocol_v1.md
<sha256>  vault_origin_story_v1.md

CANONICAL_SOURCE=LOCAL|IPFS
```

## Policy

If the hash sets differ, the Vault remains blocked. No ghosts. No drift. No approximate legacy.
