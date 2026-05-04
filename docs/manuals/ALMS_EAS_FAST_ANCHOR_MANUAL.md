# ALMS EAS Fast Anchor Manual

## Canon Rule

When the operator says **anchor**, do not recreate infrastructure by default.

**Anchor = insert proof into an existing Jay branch, leaf, or receipt chain.**

This manual supersedes contract-deploy-first behavior for ordinary ALMS receipts.

## Default Anchor Path

```json
{
  "default_anchor_path": "GitHub commit/root -> EAS Base attestation -> verify script -> optional ENS or Zora pointer",
  "custom_contract": "ONLY_IF_EXECUTABLE_LOGIC_REQUIRED",
  "wallet_signing": "PREFERRED_FOR_EAS_ATTESTATIONS"
}
```

## Existing Base EAS Config

Use the existing Base EAS config first:

```json
{
  "chain": "base-mainnet",
  "chain_id": 8453,
  "eas_contract": "0x4200000000000000000000000000000000000021",
  "schema_registry": "0x4200000000000000000000000000000000000020",
  "schema": "string identity,bytes32 root,string cid,string commit,bytes32 archiveSha256",
  "schema_uid": "0xfa94377476d86a25585e7da7889adf60f5a34fe09e1744f98626ad66bb686baa"
}
```

## Branch Discipline

Before anchoring:

1. Identify the active Jay branch, leaf, or track.
2. Do not create a new branch unless explicitly requested or technically required.
3. Insert receipt artifacts into the existing branch path.
4. Preserve lineage.

## Standard Receipt Fields

```json
{
  "identity": "jaywisdom.eth|jaywisdom.base|domain",
  "root": "0x32_BYTE_ROOT",
  "cid": "external pointer or archive pointer",
  "commit": "GITHUB_COMMIT_SHA",
  "archiveSha256": "0x32_BYTE_SHA256"
}
```

For SAM.gov:

```json
{
  "identity": "jaywisdom.eth|jaywisdom.base|sam.gov",
  "cid": "sam.gov:ENTITY_ID_OR_URL"
}
```

## Acceptable EAS Receipt

```json
{
  "schema_uid": "0x...",
  "attestation_uid": "0x...",
  "tx_hash": "0x...",
  "chain_id": 8453,
  "signer": "0xa380552a27b0a5a2874ea7aa52cac09f542002e8"
}
```

## Anchor 001 Pattern

The proven verification surface is:

```json
{
  "github_commit": "...",
  "sha256_root": "...",
  "keccak_leaf": "0x...",
  "eas_schema_uid": "0x...",
  "eas_attestation_uid": "0x...",
  "chain": "Base",
  "ens_status": "DEFERRED",
  "rule": "NO_GHOST_ANCHOR"
}
```

## No Ghost Anchor Rule

Do not promote unless the required receipt exists.

| Claim | Required receipt |
|---|---|
| GitHub proof | commit SHA |
| Root proof | deterministic root hash |
| EAS proof | schema UID + attestation UID + tx hash |
| Contract proof | deployment tx hash + contract address |
| ENS/Basename proof | visible record or profile pointer |
| Zora proof | Zora URL + contract/token address + publish or mint tx |

## What Not To Do

- Do not recreate contracts for ordinary anchors.
- Do not create new branches when an active Jay branch exists.
- Do not call a tx hash a contract.
- Do not call ENS complete unless the pointer is visibly set.
- Do not publish to Zora before the Base or EAS receipt exists.

## Fast Operator Sequence

1. Work on the existing Jay branch.
2. Generate canonical receipt/root using repo scripts.
3. Commit receipt to the existing branch.
4. Use EAS browser signer to attest on Base.
5. Capture schema UID, attestation UID, and tx hash.
6. Insert receipt into `_truth/...` and a verify script.

## Final ALMS State Format

```json
{
  "artifact": "ALMS_ANCHOR",
  "operator_identity": ["jaywisdom.eth", "jaywisdom.base"],
  "chain_id": 8453,
  "anchor_type": "EAS_ATTESTATION",
  "github_commit": "...",
  "root": "0x...",
  "schema_uid": "0x...",
  "attestation_uid": "0x...",
  "tx_hash": "0x...",
  "status": "DOUBLE_ANCHORED_VERIFICATION_SURFACE_COMPLETE"
}
```

## Current Policy

EAS is the default ALMS anchor rail. Custom contracts are used only when executable logic is required.
