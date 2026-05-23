# E05 Resolver Replay Checklist

Status: ACTIVE
Epoch: E05
Purpose: Define the deterministic replay checklist for verifying the E05 ENS/IPFS discovery pointer against repository receipts.

## Canonical Inputs

| Field | Value |
|---|---|
| ENS TXT key | `E05` |
| ENS TXT value | `E05|FINALIZED|cid=bafkreieybfrnhy4qwkmgnjumt7xzmai5ms5u2cmm7kfhjmw5x4744qvpou|commit=5b69b24f9010d1f0817be3bd81479e24b58f0fa8|root=60e117e759cf1f19375233dd59a5eac6076b1f4b0d7fe5d07dc0352dd778141c` |
| Repo | `jsonwisdom/AL` |
| E05 bundle commit | `5b69b24f9010d1f0817be3bd81479e24b58f0fa8` |
| E05 bundle path | `bundles/e05/e05.discovery.bundle.json` |
| E05 root hash | `60e117e759cf1f19375233dd59a5eac6076b1f4b0d7fe5d07dc0352dd778141c` |
| IPFS CID | `bafkreieybfrnhy4qwkmgnjumt7xzmai5ms5u2cmm7kfhjmw5x4744qvpou` |
| Artifact path | `artifacts/epoch03/IMG_9629.png` |
| Artifact SHA256 | `36f3a099fe616ebd73f642b90d30b1dc9d05a4d65d8ad9e56070b36b55515b7e` |

## Replay Steps

1. Resolve ENS TXT key `E05` from `jaywisdom.base.eth`.
2. Parse TXT fields: epoch, status, cid, commit, root.
3. Fetch commit `5b69b24f9010d1f0817be3bd81479e24b58f0fa8` from `jsonwisdom/AL`.
4. Fetch `bundles/e05/e05.discovery.bundle.json` at that commit.
5. Compute SHA256 of the fetched bundle bytes.
6. Confirm computed bundle hash equals `60e117e759cf1f19375233dd59a5eac6076b1f4b0d7fe5d07dc0352dd778141c`.
7. Fetch `receipts/e05/e05.discovery.bundle.sha256.txt` and confirm it records the same root hash.
8. Fetch IPFS object `ipfs://bafkreieybfrnhy4qwkmgnjumt7xzmai5ms5u2cmm7kfhjmw5x4744qvpou`.
9. Confirm IPFS object content corresponds to the same E05 bundle payload.
10. Fetch `artifacts/epoch03/IMG_9629.png` from the bound artifact commit referenced inside the E05 bundle.
11. Compute SHA256 of `artifacts/epoch03/IMG_9629.png`.
12. Confirm artifact hash equals `36f3a099fe616ebd73f642b90d30b1dc9d05a4d65d8ad9e56070b36b55515b7e`.
13. Confirm invalidated path `docs/epoch03_visual_layer_receipt.md` remains non-authoritative and is not used as a promotion surface.

## Acceptance Criteria

The resolver may return `MATCH_CONFIRMED` only if:

- ENS TXT parses cleanly.
- Commit exists.
- Bundle path exists at the commit.
- Bundle SHA256 equals the root hash.
- Receipt file records the same root hash.
- IPFS CID resolves to the expected E05 bundle payload.
- Artifact path exists at its bound commit.
- Artifact SHA256 matches the declared artifact hash.
- No identity surface is treated as authority.

## Failure States

| Failure | Meaning |
|---|---|
| `FAIL_ENS_TXT_MISSING` | TXT key does not resolve. |
| `FAIL_COMMIT_NOT_FOUND` | GitHub commit is unavailable. |
| `FAIL_BUNDLE_PATH_MISSING` | Bundle path does not exist at commit. |
| `FAIL_ROOT_HASH_MISMATCH` | Bundle hash differs from root. |
| `FAIL_CID_MISMATCH` | IPFS object does not match bundle payload. |
| `FAIL_ARTIFACT_HASH_MISMATCH` | Visual artifact hash differs from declaration. |
| `FAIL_AUTHORITY_PROMOTION` | ENS, operator identity, Zora, or repo ownership is treated as authority instead of discovery. |

## Constitutional Rule

ENS is discovery. IPFS is availability. GitHub is anchor surface. Authority remains commit plus bytes plus hash plus replay.

Seal: E05_RESOLVER_REPLAY_CHECKLIST_ACTIVE
