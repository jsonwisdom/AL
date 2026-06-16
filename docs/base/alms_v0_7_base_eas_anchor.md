# ALMS v0.7 Base EAS Anchor

**Status:** `BASE_EAS_ANCHORED`  
**Canon state:** `LOCKED`  
**Tagline:** Proof over narrative.

ALMS v0.7 is now a replayable public object. The chain is closed, and the trust root has shifted off GitHub.

## Final Canon State

```json
{
  "status": "BASE_EAS_ANCHORED",
  "release": "ALMS_REPEATABILITY_FRAMEWORK_V0_7",
  "canon_state": "LOCKED",
  "public_pr": "https://github.com/jsonwisdom/AL/pull/239",
  "schema_uid": "0x888696abb9a0914ede908a6b6dea82b80f27400ba734ad2cfd656809d40f5415",
  "attestation_uid": "0xB7F89F0CF84390A4B962CC15068F10FCFB9F3982A1E8A262A363FC86691A041D",
  "base_tx_hash": "0x2e23e1e6deea5dc08b80c2ee230874571d7767c9deb7bd9df8b7af12ccd0d5e8",
  "attester": "0xC345B26094c63C69222Ee775189a3d3eaead5a84",
  "recipient": "0x0000000000000000000000000000000000000000"
}
```

## Proof Surface

```json
{
  "manifest_sha256": "6d8c5e6a99b245a95ac58f63517da625384df251b4a912c48d34b5f0acdcf845",
  "bundle_sha256": "4bb783166d542bf29db96c79d5de09e1ab5c626cf11b98466f8a8260bae5ad0b",
  "annotated_tag_reference": "alms-v0.7-rc1 @ 5ecf15fbb67c5de433fdf85e66e81ed062bf8147",
  "tag_object_id": "da43ad42e747162a3716295b8f7ad1ffbd19bbdc",
  "tag_object_format": "git_sha1"
}
```

## Constitutional Outcome

- Code itself was **not** anchored.
- Replay receipts **were** anchored.
- Manifest hash is challengeable.
- Deterministic bundle is challengeable.
- Annotated tag linkage is challengeable.
- GitHub is distribution, not trust root.

## Full Enforcement Chain

```text
kernel_observation
→ canonical_frame
→ parent_linkage
→ merkle_inclusion
→ external_anchoring
→ cross_org_challenge
→ challenge_market
→ slashing
→ institutional_receipt
→ policy_gate
→ block_deploy
```

## Final Meaning

GitHub is distribution.  
Base EAS is commitment.  
Replay is legitimacy.

No trust in Jay, GitHub, or ChatGPT is required. Only hashes, receipts, and a challenge path.

## Public Lock Phrase

> v0.7 is not complete because it describes replay.  
> v0.7 is complete because it fails unreplayable claims.

**Proof over narrative.**
