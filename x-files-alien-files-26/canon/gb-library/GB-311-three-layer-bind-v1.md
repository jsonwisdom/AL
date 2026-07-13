# AL Witness Receipt — GB-311-THREE-LAYER-BIND-V1

```text
AUTHORITY = FALSE
CANON_STATUS = CANDIDATE_FOR_CANON
WITNESS_VERSION = AL-WITNESS-V1
RECEIPT_TYPE = EXTERNAL_LAYER_BINDING_RECEIPT
REVOCABLE = TRUE
REVOKED = FALSE
```

## 1. EAS Anchor

```text
CHAIN_ID = 8453
SCHEMA_NUMBER = 1695
ATTESTATION_UID = 0xf160261955ed7f3cd72d566f09963b53d449049b1d8dc9574eae1113c93ecb84
TRANSACTION_HASH = 0x94f8433fe40596e7c9a9c534b3acfaafefcbdaab9b2010dcc55c824e08b74841
ATTESTER = 0xC345B26094c63C69222Ee775189a3d3eaead5a84
RECIPIENT = 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
EAS_BROADCAST = OBSERVED
EAS_DECODED_FIELDS_MATCH = REPORTED_MATCH
```

This witness records the supplied on-chain attestation details. Independent AL replay of the transaction remains a separate gate.

## 2. Source Repository Anchor

```text
SOURCE_REPOSITORY = jsonwisdom/GENESIS
SOURCE_BRANCH = gray-baby-canon-preservation
SOURCE_PR = 8
SOURCE_MERGE_COMMIT_SHA = a1c6a6438cc70c771a2e8bdd795b8038ebec0221
MEDIA_COMMIT_SHA = b2631876e2859abd0b19b4f0b410c0522fff7bb5
RECEIPT_UPDATE_COMMIT_SHA = 2ce927788deb359093c8aed9da63f926c97d9e95
```

The media commit is not the PR merge commit. The merge commit above is the repository-level anchor for the merged candidate package.

## 3. Bound Artifacts

```text
MAP_PATH = x-files-alien-files-26/canon/three-layer-map-proposal-v0.1.md
MAP_SHA256 = 112caa6f7d9c99bfdf97ff4ac8f7360e035ef84dedda5f415c68036706efd7bb

GB311_RECEIPT_PATH = x-files-alien-files-26/canon/GB-311/receipt.yaml
GB311_RECEIPT_SHA256 = f88b288cae773b855f6dda6c95236429eed90a87d4c0999582a2210a92af2838

IMAGE_PATH = x-files-alien-files-26/canon/GB-311/media/gb-311-receipt-baby-vs-hype-baby.png
IMAGE_SHA256 = 973636f7470f240ec25da7722eaa063bcc17448e537e0db860a33ca667001cec
```

## 4. Repository Presence Boundary

```text
SOURCE_IMAGE_PRESENT_IN_GENESIS = TRUE
SOURCE_IMAGE_BYTES_BOUND = TRUE
IMAGE_COPIED_INTO_AL = FALSE
AL_WITNESS_RECEIPT_PRESENT = TRUE
```

This AL artifact witnesses the GENESIS source package. It does not claim that the image bytes were copied into AL.

## 5. Witness Statement

This receipt records that:

- a Base EAS attestation was reported with the UID and transaction hash above;
- the decoded attestation fields were reported to match the GENESIS merge commit, architecture map, GB-311 receipt, and image hash;
- the source image is present in the merged GENESIS package;
- no authority is granted;
- no ownership, factual truth, wallet-control, or institutional-authority claim is made;
- no canon promotion is implied by this witness receipt.

## 6. Current State

```text
TIER_1_VISUAL = PASS
TIER_2_INDEPENDENT = UNRESOLVED
EAS_BROADCAST = OBSERVED
EAS_ONCHAIN_REPLAY_BY_AL = PENDING
EAS_DECODED_FIELDS_MATCH = REPORTED_MATCH
SOURCE_IMAGE_BYTES_BOUND = TRUE
SOURCE_REPOSITORY_REPLAY = VERIFIED
AL_WITNESS_ANCHOR = PRESENT_ON_BRANCH
CANON_STATUS = CANDIDATE_FOR_CANON
AUTHORITY = FALSE
```

## 7. Promotion Boundary

Promotion remains fail-closed until the project-defined independent replay and review gates are completed.

```text
CANON_PROMOTION = PENDING
AUTHORITY = FALSE
```
