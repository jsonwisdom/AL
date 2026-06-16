# Jay Identity Discovery Surface v1

Status: DISCOVERY_SURFACE_ACTIVE
Root Identity: jaywisdom.base.eth / @JayWisdom12
Created: 2026-05-23
Last Updated: 2026-05-23

This document defines a machine-searchable discovery surface for Jay Wisdom / JSONWisdom identity artifacts inside the AL repository.

It records committed repository bytes and distinguishes between verified anchors and unresolved references.

## Confirmed Repository Anchors

| Anchor | Path | Status | Notes |
|---|---|---|---|
| Jay EVM Address Registry v1 | `docs/jay-evm-address-registry.v1.md` | VERIFIED_ANCHOR | Canonical registry for the JAYWISDOM Creator Coin anchor and Zora search surface. |
| Jay Identity Discovery Surface v1 | `docs/jay-identity-discovery-surface.v1.md` | VERIFIED_ANCHOR | Current discovery index for Jay identity artifacts inside this repository. |
| Epoch03 Witness Rules Proposal v1 | `proposals/epoch03-witness-rules.v1.md` | VERIFIED_ANCHOR | Witness rule proposal bytes committed after prior absence verification cycle. |

## Historical Absence Checks

| Check | Path | Result | Constitutional Meaning |
|---|---|---|---|
| CHECK_001 | `proposals/epoch03-witness-rules.v1.md` | NOT_FOUND | Narrative reference only at time of first replay check. |
| CHECK_002 | `proposals/epoch03-witness-rules.v1.md` | NOT_FOUND | Repeated verification preserved PENDING_BYTES boundary. |
| CHECK_003 | `proposals/epoch03-witness-rules.v1.md` | FOUND_AND_COMMITTED | Receipt-bearing bytes now exist and lawful promotion occurred. |

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
- Repeated absence checks may strengthen the pending classification but may not promote the missing artifact.
- Promotion from PENDING_BYTES to VERIFIED_ANCHOR requires committed bytes and replay-safe verification.

## Current Constitutional Verdict

MATCH_CONFIRMED for the committed EVM registry file.

MATCH_CONFIRMED for the committed discovery surface file.

MATCH_CONFIRMED for `proposals/epoch03-witness-rules.v1.md` after lawful byte creation and replay verification.

Seal: NO_GHOST_ANCHORS_RECEIPTS_DECIDE
