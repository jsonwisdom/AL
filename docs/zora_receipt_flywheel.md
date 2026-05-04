# Zora Receipt Flywheel

Status: DESIGN SPEC — NO TOKEN OR CONTRACT CLAIMED

## Purpose

Use Zora as the public creative surface for verified ALMS receipts without confusing art, posts, or media with the underlying proof.

The receipt remains the source of truth. The image is the invitation.

## Jay Wisdom Operator Layer

Jay Wisdom is the human operator and philosophy layer of this system.

Core identity:

```text
Jay Wisdom / JSONWisdom / Zero Cool
jaywisdom.base → resolves to jaywisdom.eth
```

Guiding doctrine:

```text
Proof > narrative
Verify > announce
Receipts over vibes
If it does not verify, it does not exist
```

Jay Wisdom is represented in the public surface as the operator of the verification machine, not as a substitute for verification.

The machine proves. Jay routes attention to the proof.

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

## ALMS Machine Speed

Machine Speed means the system moves at the speed of verified state transitions, not the speed of announcements.

The goal is fast public output without skipping proof gates.

```text
CAPTURE → HASH → COMMIT → FETCH → REPLAY → PUBLISH → CHAIN_CONFIRM
```

Speed rules:

- Fast capture is allowed.
- Fast publishing is allowed.
- Fast status upgrades are not allowed.
- A root is not real until it is repo-visible and replay-confirmed.
- A Base transaction is not real until chain evidence is fetched.
- A Zora post is not proof unless it points back to receipts.

Machine Speed is achieved by reducing friction, not by weakening verification.

### Monotonic Stage Rule

A stage can only be marked complete if every prior stage is complete.

```json
{
  "stage_order": [
    "CAPTURE",
    "HASH",
    "COMMIT",
    "FETCH",
    "REPLAY",
    "PUBLISH",
    "CHAIN_CONFIRM"
  ],
  "rule": "cannot skip forward; cannot regress without a new receipt"
}
```

## Core Loop

1. Verify a receipt in ALMS.
2. Render a visual proof card.
3. Publish the image/artifact to Zora.
4. Include receipt hash, manifest path, repo commit, Base status, identity binding, and verification URL in the post metadata or caption.
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
| Jay Wisdom | Human operator / narrative router | Not a proof boundary |
| GitHub | Source bytes, manifests, replay scripts | Primary proof surface |
| ALMS | Canonicalization, hashing, Merkle rules | Verification logic |
| Base | Public settlement / attestation record | Publication timestamp + chain receipt |
| Zora | Media and collector surface | Distribution layer |
| Browser verifier | Client-side replay | Public proof interface |
| Meme Court / Quest | Game layer | Education + engagement |

## Meme Court Runtime Integration

Zora posts should be able to route into Meme Court case logic.

Current runtime module:

```text
docs/meme-court.js
```

Supported charges:

- GHOST_PROMOTION
- NORMALIZATION_TREASON
- IDENTITY_DRIFT
- FAKE_CHAIN_CONFIRM
- HASH_THEATER
- SKIPPED_REPLAY

Zora should display these as case outcomes, not as proof outputs.

Meme Court teaches the failure mode. ALMS receipts decide the truth.

## Base Receipt Fields

```json
{
  "artifact": "ALMS_BASE_PUBLICATION_RECEIPT",
  "network": "base",
  "chain_id": 8453,
  "operator": "Jay Wisdom",
  "operator_base_name": "jaywisdom.base",
  "canonical_ens_root": "jaywisdom.eth",
  "identity_resolution": "jaywisdom.base -> jaywisdom.eth",
  "machine_speed_stage": "CAPTURE|HASH|COMMIT|FETCH|REPLAY|PUBLISH|CHAIN_CONFIRM",
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

- Jay Wisdom narrative != proof.
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
  "operator": "Jay Wisdom",
  "operator_base_name": "jaywisdom.base",
  "canonical_ens_root": "jaywisdom.eth",
  "visual_asset_path": "docs/assets/<image>.png",
  "source_manifest_path": "_truth/us/constitution/<manifest>.json",
  "source_root_sha256": "<64_hex>",
  "repo_commit_sha": "<git_commit>",
  "machine_speed_stage": "REPLAY_VERIFIED",
  "meme_court_case_id": "MC-<id-or-null>",
  "meme_court_charge": "<charge-or-CLEAN_PASS>",
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
- operator: Jay Wisdom
- identity: `jaywisdom.base → jaywisdom.eth`
- machine speed stage: CAPTURE / HASH / COMMIT / FETCH / REPLAY / PUBLISH
- Meme Court charge or CLEAN PASS
- short root hash
- status badge
- QR/verifier pointer
- quote or drift challenge
- visual identity: Meme Court / Goblin Audit / Constitution Quest
- optional Base status: PENDING / CHAIN CONFIRMED / REPLAY VERIFIED

## Flywheel

```text
Jay Wisdom Signal → ALMS Receipt → Meme Court Check → GitHub Manifest → Image → Zora → Base Receipt → Share → Verify → Quest → New Receipt → New Image
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

Operator: Jay Wisdom
Identity: jaywisdom.base → jaywisdom.eth
Stage: <machine_speed_stage>
Charge: <meme_court_charge_or_CLEAN_PASS>
Root: <short_root>
Receipt: <receipt_path>
Base: <base_tx_or_uid_or_PENDING>
Verify: <url>

No Receipt. No Mercy. 🧌⚖️🧾
```

## Zora Caption Auto-Generator Contract

Any generated caption must include:

```json
{
  "operator": "Jay Wisdom",
  "identity": "jaywisdom.base -> jaywisdom.eth",
  "stage": "<machine_speed_stage>",
  "charge": "<meme_court_charge_or_CLEAN_PASS>",
  "root": "<short_root>",
  "receipt": "<receipt_path>",
  "base": "<base_tx_or_uid_or_PENDING>",
  "verify": "<url>"
}
```

If any field is missing, the caption status is `DRAFT_INCOMPLETE`.

## Jay Wisdom Public Voice

Use direct proof language:

```text
Bring receipts.
Verify the root.
Keep the chain clean.
No vibes. Just rights.
```

Avoid claiming finality before replay.

Avoid turning the Constitution into partisan scoring.

The game is precision. The win condition is proof.

## Status

Zora flywheel is approved as a public engagement layer, not a trust boundary.

Base is approved as a settlement / attestation layer, not the canonical truth boundary.

`jaywisdom.base` is the Base-facing anchor and resolves to the canonical ENS identity `jaywisdom.eth` for receipt identity purposes.

ALMS Machine Speed is approved as the throughput model: move fast, but only promote verified state.

Meme Court charge detection is approved as an enforcement and education layer.

Proof > narrative.
