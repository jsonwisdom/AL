# JAYWISDOM Lattice V2

Status: EVIDENCE_INDEX
Authority: false
No Fake Green: active

## Purpose

Index current JAYWISDOM identity, economic, and attestation surfaces without promoting unresolved claims.

## Identity Layer

- `jaywisdom.eth`
- `jaywisdom.base.eth`
- `@JayWisdom12`

## Economic Registry Layer

The JAYWISDOM Creator Coin is recorded in:

- `docs/jay-evm-address-registry.v1.md`

Recorded anchor:

- Contract: `0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f`
- Network: Base
- Context: JAYWISDOM Creator Coin
- Verdict: MATCH_CONFIRMED

Boundary: this lattice does not add payment mechanics, payout claims, tax claims, governance authority, wallet control, or trading advice.

## EAS Schema Registration Layer

EAS schema registration is represented in repo code by:

- `scripts/deploy-eas-schema.ts`
- `scripts/deploy-link-schema.ts`

Observed implementation pattern:

- Registry address: `0x4200000000000000000000000000000000000020`
- Schema registration through `SchemaRegistry.register(...)`
- Resolver address currently set to `ethers.ZeroAddress`
- Revocable flag set to `true`

Recorded schema strings in repo:

```text
bytes32 actionHash,address signer,bytes signature,uint64 timestamp,string payloadRef
```

```text
bytes32 parentUID,bytes32 childUID,bytes32 parentActionHash,bytes32 childActionHash,address parentSigner,address childSigner,string relation,uint64 timestamp,string payloadRef
```

Boundary: this file records scripts and intended schema registration surface only. It does not claim any schema UID, deployed resolver, attestation count, or Base mainnet execution unless separately evidenced by receipt.

## EAS Resolver Contracts Layer

Resolver contracts are treated as optional EAS validation hooks.

Current repo evidence:

- The observed schema deployment scripts use `ethers.ZeroAddress` as resolver.
- No JAYWISDOM-specific deployed resolver is promoted by this lattice.

Allowed future evidence:

- schema UID
- resolver address
- attestation UID
- transaction hash
- explorer link
- receipt file

## Cross-Links v2.1

- [COMPUTERWISDOM observer/replay](./../COMPUTERWISDOM/)
- [EAS Schema Registry + Attest Hub](https://attest.org/) — PROOF_007 gated
- [EAS Scan](https://easscan.org) — schema/resolver explorer
- [Smart Wallet AA flows](jaywisdom.eth)
- Historical contracts: null surface post-audit

Boundary: cross-links route observers to evidence surfaces only. They do not promote PROOF_007, payment mechanics, resolver deployment, schema UID, attestation count, governance authority, or wallet control.

## Proof Boundary

- PROOF_007 is not active canon in this lattice.
- JAYWISDOM Creator Coin remains recorded through the cleaned registry anchor.
- Additional EAS, resolver, payment, or coin-mechanics claims require separate receipt-bearing artifacts.

Seal: RECEIPTS_DECIDE_REALITY
