# Zora Receipt Flywheel

Status: DESIGN SPEC — NO TOKEN OR CONTRACT CLAIMED

## Purpose

Use Zora as the public creative surface for verified ALMS receipts without confusing art, posts, or media with the underlying proof.

The receipt remains the source of truth. The image is the invitation.

## Core Loop

1. Verify a receipt in ALMS.
2. Render a visual proof card.
3. Publish the image/artifact to Zora.
4. Include receipt hash, manifest path, repo commit, and verification URL in the post metadata or caption.
5. Route collectors back to the verifier.
6. New users replay the proof and enter Constitution Quest / Meme Court.

## Non-Negotiable Rules

- Image != proof.
- Zora post != deed.
- Transaction hash != contract address.
- Contract address is UNVERIFIED_IDENTIFIER until confirmed from the platform or chain explorer.
- Root status cannot be upgraded from a Zora post alone.
- Every Zora artifact must point back to repo-visible receipts.

## Canonical Receipt Fields

```json
{
  "artifact": "ALMS_ZORA_RECEIPT_CARD",
  "title": "<human title>",
  "visual_asset_path": "docs/assets/<image>.png",
  "source_manifest_path": "_truth/us/constitution/<manifest>.json",
  "source_root_sha256": "<64_hex>",
  "repo_commit_sha": "<git_commit>",
  "zora_url": null,
  "zora_contract_address": "UNVERIFIED_IDENTIFIER",
  "zora_tx_hash": null,
  "verification_url": "https://jsonwisdom.github.io/AL/<verifier_path>",
  "status": "DRAFT|PUBLISHED_PENDING_CHAIN_CONFIRMATION|VERIFIED"
}
```

## Image Card Pattern

Each receipt image should show:

- title
- artifact id
- short root hash
- status badge
- QR/verifier pointer
- quote or drift challenge
- visual identity: Meme Court / Goblin Audit / Constitution Quest

## Flywheel

```text
Receipt → Image → Zora → Share → Verify → Quest → New Receipt → New Image
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

Root: <short_root>
Receipt: <receipt_path>
Verify: <url>

No Receipt. No Mercy. 🧌⚖️🧾
```

## Status

Zora flywheel is approved as a public engagement layer, not a trust boundary.

Proof > narrative.
