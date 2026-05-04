# Zora Receipt Flywheel

Status: DESIGN SPEC — NO TOKEN OR CONTRACT CLAIMED

## Purpose

Use Zora as the public creative surface for verified ALMS receipts without confusing art, posts, or media with the underlying proof.

The receipt remains the source of truth. The image is the invitation.

## Identity Anchor

Primary operator identity:

```text
jaywisdom.base → resolves to jaywisdom.eth
```

Rules:

- `jaywisdom.base` is the Base-facing public anchor / social routing name.
- `jaywisdom.eth` is the canonical ENS root identity.
- Base/Zora/public captions may display `jaywisdom.base` for accessibility.
- Verification receipts should bind back to `jaywisdom.eth` when recording canonical identity.
- Do not claim ENS text-record anchoring unless a visible ENS/Basename record or transaction receipt exists.

## Core Loop

1. Verify a receipt in ALMS.
2. Render a visual proof card.
3. Publish the image/artifact to Zora.
4. Include receipt hash, manifest path, repo commit, and verification URL in the post metadata or caption.
5. Route collectors back to the verifier.
6. New users replay the proof and enter Constitution Quest / Meme Court.

## Base Settlement Layer

Base is the public settlement / attestation layer for publication events.

Base does not replace GitHub, ALMS, or replay verification.

Base records publication events that point back to repo-visible proof.

Updated loop:

```text
ALMS Receipt → GitHub Manifest → Image Card → Zora Post → Base Tx / Attestation → Public Verifier → Quest → New Receipt
```

## Layer Separation

| Layer | Role | Trust Boundary |
|---|---|---|
| GitHub | Source bytes, manifests, replay scripts | Primary proof surface |
| ALMS | Canonicalization, hashing, Merkle rules | Verification logic |
| Base | Public settlement / attestation record | Publication timestamp + chain receipt |
| Zora | Media and collector surface | Distribution layer |
| Browser verifier | Client-side replay | Public proof interface |
| Meme Court / Quest | Game layer | Education + engagement |

## Base Receipt Fields

```json
{
  "artifact": "ALMS_BASE_PUBLICATION_RECEIPT",
  "network": "base",
  "chain_id": 8453,
  "operator_base_name": "jaywisdom.base",
  "canonical_ens_root": "jaywisdom.eth",
  "identity_resolution": "jaywisdom.base -> jaywisdom.eth",
  "source_root_sha256": "<64_hex>",
  "source_manifest_path": "_truth/us/constitution/<manifest>.json",
  "repo_commit_sha": "<git_commit>",
  "zora_url": "<url_or_null>",
  "base_tx_hash": "UNVERIFIED_IDENTIFIER",
  "base_attestation_uid": "UNVERIFIED_IDENTIFIER",
  "explorer_url": null,
  "verification_url": "https://jsonwisdom.github.io/AL/<verifier_path>",
  "status": "DRAFT|SUBMITTED_PENDING_CHAIN_CONFIRMATION|CHAIN_CONFIRMED|REPLAY_VERIFIED"
}
```

## Base Rules

- Base tx hash proves a transaction event, not the content itself.
- Base attestation UID proves an attestation event, not canonical text by itself.
- Base records must point back to repo-visible proof.
- Base identity display may use `jaywisdom.base`, but canonical identity resolves to `jaywisdom.eth`.
- Do not call a Base tx a contract.
- Do not call an attestation verified until the UID is fetched and matched.
- Do not upgrade root status from Base alone.
- Chain evidence is additive, not substitutive.

## Non-Negotiable Rules

- Image != proof.
- Zora post != deed.
- Transaction hash != contract address.
- Contract address is UNVERIFIED_IDENTIFIER until confirmed from the platform or chain explorer.
- Root status cannot be upgraded from a Zora post alone.
- Every Zora artifact must point back to repo-visible receipts.
- Every Base artifact must point back to repo-visible receipts.

## Canonical Receipt Fields

```json
{
  "artifact": "ALMS_ZORA_RECEIPT_CARD",
  "title": "<human title>",
  "operator_base_name": "jaywisdom.base",
  "canonical_ens_root": "jaywisdom.eth",
  "visual_asset_path": "docs/assets/<image>.png",
  "source_manifest_path": "_truth/us/constitution/<manifest>.json",
  "source_root_sha256": "<64_hex>",
  "repo_commit_sha": "<git_commit>",
  "zora_url": null,
  "zora_contract_address": "UNVERIFIED_IDENTIFIER",
  "zora_tx_hash": null,
  "base_publication_receipt_path": "_truth/base/<receipt>.json",
  "verification_url": "https://jsonwisdom.github.io/AL/<verifier_path>",
  "status": "DRAFT|PUBLISHED_PENDING_CHAIN_CONFIRMATION|CHAIN_CONFIRMED|REPLAY_VERIFIED"
}
```

## Image Card Pattern

Each receipt image should show:

- title
- artifact id
- identity: `jaywisdom.base → jaywisdom.eth`
- short root hash
- status badge
- QR/verifier pointer
- quote or drift challenge
- visual identity: Meme Court / Goblin Audit / Constitution Quest
- optional Base status: PENDING / CHAIN CONFIRMED / REPLAY VERIFIED

## Flywheel

```text
Receipt → GitHub Manifest → Image → Zora → Base Receipt → Share → Verify → Quest → New Receipt → New Image
```

## First Campaign

Meme Court: Internal Goblin Quest Audit

Initial drops:

1. good Behaviour vs good Behavior
2. supreme Court vs Supreme Court
3. Affirmation:--" vs smart quote / em dash drift
4. Place or Places vs Place
5. Federal Root: A1+A2+A3 verified

## Caption Template

```text
Meme Court Receipt: <TITLE>

The goblin tried to mutate the record.
The verifier caught the drift.

Identity: jaywisdom.base → jaywisdom.eth
Root: <short_root>
Receipt: <receipt_path>
Base: <base_tx_or_uid_or_PENDING>
Verify: <url>

No Receipt. No Mercy. 🧌⚖️🧾
```

## Status

Zora flywheel is approved as a public engagement layer, not a trust boundary.

Base is approved as a settlement / attestation layer, not the canonical truth boundary.

`jaywisdom.base` is the Base-facing anchor and resolves to the canonical ENS identity `jaywisdom.eth` for receipt identity purposes.

Proof > narrative.
