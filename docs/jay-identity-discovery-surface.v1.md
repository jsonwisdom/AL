# Jay Identity Discovery Surface v1

Status: DISCOVERY_SURFACE_ACTIVE
Root Identity: jaywisdom.base.eth / @JayWisdom12
Created: 2026-05-23

This document defines a machine-searchable discovery surface for Jay Wisdom / JSONWisdom identity artifacts inside the AL repository.

It does not promote unverified artifacts. It records only committed repository bytes and explicitly marks missing artifacts as pending.

## Confirmed Repository Anchors

| Anchor | Path | Status | Notes |
|---|---|---|---|
| Jay EVM Address Registry v1 | `docs/jay-evm-address-registry.v1.md` | COMMITTED | Canonical registry for the JAYWISDOM Creator Coin anchor and Zora search surface. |

## Pending Anchors

| Anchor | Expected Path | Status | Requirement |
|---|---|---|---|
| Epoch03 Witness Rules Proposal v1 | `proposals/epoch03-witness-rules.v1.md` | PENDING_BYTES | File was referenced by operator narrative but was not found in repo at time of discovery-surface creation. Submit or create bytes before promotion. |

## Identity Search Terms

```text
Jay Wisdom
Jason Wisdom
JSONWisdom
JAYWISDOM
@JayWisdom12
jaywisdom.eth
jaywisdom.base.eth
https://zora.co/@jaywisdom
0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f
```

## Promotion Rules

- A referenced artifact may not be promoted unless file bytes exist in the repository or a separate public receipt is supplied.
- Narrative references remain PENDING_BYTES until backed by a URL, commit, blob, hash, screenshot, or raw content.
- Transaction hashes, wallet addresses, creator contracts, ENS records, and Zora profile links must not be collapsed into a single authority claim.
- The discovery surface is an index, not a deed.

## Current Constitutional Verdict

MATCH_CONFIRMED for the committed EVM registry file.

PENDING_BYTES for `proposals/epoch03-witness-rules.v1.md`.

Seal: NO_GHOST_ANCHORS_RECEIPTS_DECIDE
