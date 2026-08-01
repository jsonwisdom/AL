# Witness Registry Specification

## Version 1.0

The witness ledger is append-only by policy. Corrections are added as new records referencing the superseded witness; existing records are not silently rewritten.

## Allowed Statuses

- `DECLARED_UNVERIFIED`
- `SIGNATURE_VERIFIED`
- `DISPUTED`
- `SUPERSEDED`

## Uniqueness

`witness_id` must be globally unique within the ledger. A witness identity may appear more than once, but each declaration must identify one registry entry and one evidence reference.

## Identity Separation

Account resolution, commit existence, signature verification, and authority are separate predicates. None implies another.

## Promotion Boundary

Witness counts are descriptive. Quorum, promotion, and authority decisions require a separate versioned policy and cannot be inferred from count alone.
