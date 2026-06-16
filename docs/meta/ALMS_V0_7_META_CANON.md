# ALMS v0.7 Meta Canon

**Status:** `BASE_EAS_ANCHORED`  
**Canon state:** `LOCKED`  
**Tagline:** Proof over narrative.

This document completes the top-level canon record linking GitHub, Base, Replay, and Zora.

## Proof Surface

```json
{
  "manifest_sha256": "6d8c5e6a99b245a95ac58f63517da625384df251b4a912c48d34b5f0acdcf845",
  "bundle_sha256": "4bb783166d542bf29db96c79d5de09e1ab5c626cf11b98466f8a8260bae5ad0b",
  "annotated_tag_reference": "alms-v0.7-rc1 @ 5ecf15fbb67c5de433fdf85e66e81ed062bf8147",
  "tag_object_id": "da43ad42e747162a3716295b8f7ad1ffbd19bbdc",
  "tag_object_format": "git_sha1",
  "schema_uid": "0x888696abb9a0914ede908a6b6dea82b80f27400ba734ad2cfd656809d40f5415",
  "attestation_uid": "0xB7F89F0CF84390A4B962CC15068F10FCFB9F3982A1E8A262A363FC86691A041D",
  "base_tx_hash": "0x2e23e1e6deea5dc08b80c2ee230874571d7767c9deb7bd9df8b7af12ccd0d5e8",
  "public_pr": "https://github.com/jsonwisdom/AL/pull/239"
}
```

## Stack Separation

- **GitHub = distribution** — PR #239, release docs, code mirrors
- **Base EAS = commitment** — onchain attestation of hashes only
- **Replay = legitimacy** — independent reconstruction via bundle hash
- **Zora = cultural propagation** — public narrative and distribution layer

## Enforcement Chain

```text
kernel_observation → canonical_frame → parent_linkage → merkle_inclusion → external_anchoring → cross_org_challenge → challenge_market → slashing → institutional_receipt → policy_gate → block_deploy
```

## Constitutional Meaning

A claim is legitimate only when its execution history can be reconstructed, challenged, and converged upon by independent observers.

GitHub is not the trust root. The organization is not the trust root. The signer is not the trust root. The trust root is portable replay receipts.

## Final Lock Phrase

> v0.7 is not complete because it describes replay.  
> v0.7 is complete because it fails unreplayable claims.

## Linked Canon Docs

- Base Anchor: `docs/base/alms_v0_7_base_eas_anchor.md` (commit `daf202a`)
- Zora Canon: `docs/zora/ALMS_V0_7_ZORA_CANON.md` (commit `c59bd75`)

**Proof over narrative.**
