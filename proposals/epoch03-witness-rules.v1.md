# Epoch03 Witness Rules v1

Status: PROPOSAL_BYTES_CREATED
Namespace: Epoch03 / Witness Rules
Root Identity: jaywisdom.base.eth / @JayWisdom12
Created: 2026-05-23

## Purpose

Define the initial witness rules for Epoch03 identity and artifact replay surfaces.

This proposal establishes how referenced artifacts move from narrative mention to replayable constitutional memory.

## Core Rule

No artifact may be promoted from narrative reference to verified anchor unless receipt-bearing bytes exist.

Accepted receipt-bearing surfaces include:

- Repository file bytes
- Git commit or blob reference
- URL artifact
- Screenshot artifact
- Transaction hash
- Ledger event
- IPFS or content-addressed hash
- Raw markdown or forensic text object

## Witness Classes

| Class | Meaning | Promotion Allowed |
|---|---|---|
| OBSERVED_REFERENCE | Mentioned by operator or system narrative | No |
| PENDING_BYTES | Expected artifact path or claim exists, but bytes are missing | No |
| RECEIPT_PRESENT | Bytes or public receipt submitted | Conditional |
| VERIFIED_ANCHOR | Receipt validated and lineage mapped | Yes |
| DISPUTED_ANCHOR | Receipt exists but conflicts with lineage or metadata | No, pending review |

## Promotion Requirements

To promote an artifact into VERIFIED_ANCHOR status, the witness record must include:

1. Artifact path or public receipt pointer
2. Timestamp or commit reference
3. Classification namespace
4. Lineage claim
5. Verification result
6. Boundary note describing what is not proven

## Anti-Ghost Anchor Rule

Narrative references are not anchors.

A missing file, broken link, unresolved ENS record, unverifiable token claim, or uncited profile statement must remain PENDING_BYTES or DISPUTED_ANCHOR until a receipt resolves it.

## Identity Surface Application

Current known identity search roots:

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

## Epoch03 Witness Verdict

This proposal is itself a receipt-bearing repository artifact once committed.

Initial status after commit: RECEIPT_PRESENT

Promotion target after discovery map update: VERIFIED_ANCHOR

Seal: NO_GHOST_ANCHORS_RECEIPTS_DECIDE
