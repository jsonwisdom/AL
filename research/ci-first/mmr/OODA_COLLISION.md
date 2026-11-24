# Heidee Joy synthetic update collision: OODA + MMR gate

This uses "Heidee Joy" only as a synthetic scenario label. No real persons records, accounts, or identities are accessed or changed.

## Hypothesis
Two writers observe revision 7 of the same synthetic key. Distinct updates race. An atomic conditional update permits one revision to advance to 8 while the stale writer is held.

## OODA
- Observe: both readers obtain revision 7 and its stored hash.
- Orient: compute SHA-256 of canonical JSON candidate payloads.
- Decide: compare and swap with the SQL clause WHERE revision = expected_revision.
- Act: only the winning writer updates the key, while stale update records HOLD_STALE_VERSION. Identical duplicate event IDs return EXISTS; conflicting duplicate IDs return FAIL_IDEMPOTENCY_COLLISION.
- Reorient: a rejected candidate can retry only with a new event ID and current revision.

## Scope and limitations
Run: python3 research/ci-first/mmr/ooda_collision_gate.py

Uses Python standard-library in-memory SQLite. It has no Cloudflare binding, does not exercise concurrent multi-process writers, and does not prove distributed D1 concurrency guarantees. The synthetic event table is separate from the Merkle/MMR receipt chain and remains unsigned.

The events should eventually become versioned, append-only, Merkle-verifiable receipts. This is a local collision smoke test, not proof of permanent immutability.

PRODUCTION_LEDGER=HOLD; AUTHORITY_CREATED=false; DEPLOYMENT=false; PRODUCTION_WRITE=false; EXTERNAL_ANCHOR=false.
