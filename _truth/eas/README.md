# EAS Sovereign Replay Kernel Receipts

Placement:
- `_truth/eas/` is the source-of-truth receipt directory.
- `docs/eas/` is the public GitHub Pages distribution mirror.

Rule:
- `CW_EAS_ATTESTATION_WAIT` means the local manifest exists but the Base EAS UID is not recorded yet.
- `CW_EAS_ATTESTATION_LOCKED` requires UID, transaction hash, attester, recipient, commit, CID, and hashes to match.
- Never mark LOCKED with missing or truncated fields.

Required EAS UI payload:
- root: jaywisdom.eth
- kernel: cw-sovereign-replay-kernel-v1
- tag: cw-sovereign-replay-kernel-v1
- commit: 55a248bee1d7a2d1d5ca6a2405d7c94dbc65186f
- ipfs_cid: bafkreibe3hfsyoqpeew4xcjz6n5pd26e2cgf5my7cwouky2cc4ykcsqo7y
- artifact_hash: sha256:24d9cb2c3a0f212dcb8939f37af1ebc4d08c5eb31f159d4563421730a14a0efe
- manifest_payload_hash: sha256:102b7bfaeb0a95c2461e91ebefaffd84166d66421318d9acc6401efa8b88f4a0
- status: LOCKED

UI signs. Base notarizes. Repo records. ALMS remembers.
