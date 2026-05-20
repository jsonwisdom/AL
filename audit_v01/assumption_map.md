# Replayable Resilience Audit v0.1 — Assumption Map

## Target
Prior claim: a Merkle root and offer page were anchored to `jaywisdom.base.eth`.

## Audit verdict
`NEEDS_RECEIPTS`

## Assumptions detected

1. A Merkle root existed.
2. The Merkle root represented 24 doctrine leaves.
3. The root was anchored to `jaywisdom.base.eth`.
4. A live offer page existed.
5. The offer page was tied to the root.
6. The framework was ready to sell as verified infrastructure.

## Assumption classification

| Assumption | Status | Required proof |
|---|---|---|
| Merkle root exists | Unverified | Full root value and leaf list |
| 24 leaves exist | Unverified | Canonical leaf list and hashing rule |
| ENS anchor exists | Unverified | Visible text record or transaction |
| Base/EAS witness exists | Unverified | Base tx or EAS UID |
| Offer page exists | Unverified | URL or committed file |
| Product is verified | Rejected | Recompute + witness match |

## Boundary rule enforced

Cognition may generate the claim. It may not promote the claim.

Only a receipt with replayable witnesses may cross the membrane.
