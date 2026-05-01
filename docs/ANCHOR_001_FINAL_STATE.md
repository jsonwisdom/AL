# Anchor 001 — Final State

## Status: DOUBLE-ANCHORED — VERIFICATION SURFACE COMPLETE

Anchor 001 is complete at the verification-surface layer using GitHub plus EAS on Base.

ENS is intentionally deferred. The Basename UI did not expose editable text records for `jaywisdom.base.eth`, so no ENS text record is claimed here.

Rule: no ghost anchor.

## Current Canonical State

| Layer | Value |
|---|---|
| GitHub Commit | `13004719dd0c34f765ca95dfe8566b6feb2bf6cf` |
| Merkle Root (SHA-256) | `ff55160908ff41d23f7af0df8873ef7a0dcf8163d1a308f58941e87b5a95bad9` |
| Leaf Keccak-256 | `0xb7e55f9e1f4f27cd96f38d74e6510e184a14772ef3f9f628d5acc68531dd185d` |
| EAS Schema UID | `0x3bab210b4da3faff084e146075caf9168efb5c9c87f18509bca2c07d7f2e49c` |
| EAS Attestation UID | `0x18b5b00c62c648df2ccf4a746645493fa2a0b0dcda6697052d8c3a3d1586c142` |
| Chain | Base |
| Record | `examples/sample-record.json` |
| ENS | `DEFERRED` — Basename text records not editable on `jaywisdom.base.eth` |

## Verification Path

1. Clone `jsonwisdom/Welcome-to-JSONWISDOM`.
2. Check out commit `13004719dd0c34f765ca95dfe8566b6feb2bf6cf`.
3. Recompute the JCS canonical bytes.
4. Recompute SHA-256 and confirm Merkle root `ff55160908ff41d23f7af0df8873ef7a0dcf8163d1a308f58941e87b5a95bad9`.
5. Recompute Keccak-256 for `examples/sample-record.json` and confirm `0xb7e55f9e1f4f27cd96f38d74e6510e184a14772ef3f9f628d5acc68531dd185d`.
6. Verify the EAS attestation UID `0x18b5b00c62c648df2ccf4a746645493fa2a0b0dcda6697052d8c3a3d1586c142` on Base.

## Binding

Both the SHA-256 and Keccak-256 values are bound to the same RFC 8785 JCS canonical record bytes.

## Canonical Repo

`jsonwisdom/Welcome-to-JSONWISDOM` is the canonical source of truth for Anchor 001.

This repo, `jsonwisdom/AL`, preserves the reference for operational continuity and historical alignment.

## Boundary

ENS is not required for trust here. ENS would add human-readable discovery only.

The cryptographic trust path is:

```text
GitHub commit → JCS canonical bytes → SHA-256 → Keccak-256 → EAS attestation on Base
```
