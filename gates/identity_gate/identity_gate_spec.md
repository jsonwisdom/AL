# Identity Gate Specification

## Version 1.0

## Purpose

Provide mechanical, non-authoritative identity anchoring for registry entries. Signers are witnesses, not rulers.

## State Boundary

- A witness declaration records who claimed to observe an entry.
- A GitHub commit proves repository state, not human identity or intent.
- A username lookup proves account resolution only.
- A declaration without a cryptographic signature is `DECLARED_UNVERIFIED`.
- No witness declaration changes `authority_status`; it remains `false`.

## Required Witness Fields

Each witness record must contain:

- `witness_id`
- `entry_id`
- `signer.type`
- signer identity data appropriate to that type
- `timestamp`
- `attestation_status`
- a commit or artifact reference

Witness identifiers must be unique. Referenced registry entries and commits must exist.

## Verification Profiles

### GitHub

A GitHub witness is mechanically valid only when:

1. the username resolves;
2. the referenced commit exists in `jsonwisdom/AL`;
3. the witness record is well formed.

This does not prove that the account holder personally authored the declaration. A signed commit or another signature proof is required for that stronger claim.

### PGP

The detached signature must verify over specified bytes and the fingerprint must appear in the witness registry.

### DID

The DID document and verification method must resolve, and the proof must verify over specified bytes.

### Ethereum

The address must be valid and the signature must recover that address over the specified message bytes.

## Fail-Closed Rule

Missing, malformed, unresolved, or unverifiable evidence leaves the witness unverified. CI must never translate a placeholder, skipped check, or declaration into `VERIFIED` or `ACTIVE`.

## Authority

Witnessing is evidence of observation only. It creates no execution, governance, adjudicative, or publication authority.
