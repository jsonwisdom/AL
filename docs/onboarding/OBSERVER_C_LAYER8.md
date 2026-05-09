# Observer C Onboarding — Resolver Witness Convergence

**Canon:** Layer 8 Sealed  
**Receipt:** `receipts/resolver_witness/convergence_run_021.json`  
**Receipt commit:** `80c14cf`  
**Repo state witnessed:** `jsonwisdom/AL@653aa95f4be188be9608c8ee13133ce766210476` (main)  
**Status:** `LAYER_8_SEALED — FREEZE_AS_CANON — OBSERVER_C_READY_FOR_STABLE_REPLAY`

## 1. Purpose

Reproduce the two-observer consensus from run #21 using only immutable artifacts. No network calls, no mutable registries. If your implementation produces the five hashes below, you have verified the same convergence that Python and TypeScript observers verified on main.

## 2. Required Artifacts

Use only these artifacts:

1. `receipts/resolver_witness/convergence_run_021.json`
2. `tests/resolver_witness/fixtures/`
3. `tests/resolver_witness/hash_registry.json`
4. `docs/specs/RESOLVER_WITNESS_SPEC_V1.md`

Do not pull later commits when reproducing the sealed surface. Check out `80c14cf` for the receipt surface and verify the witnessed repo state `653aa95f4be188be9608c8ee13133ce766210476`.

## 3. Canonical Serialization

Use exactly:

- `sort_keys: true`
- `separators: [",", ":"]`
- `ensure_ascii: false`
- `encoding: UTF-8`
- `line_ending: LF`
- `trailing_newline: false`

Any deviation breaks hash equivalence.

## 4. Reproduction Steps

1. Check out the sealed receipt surface: `git checkout 80c14cf`
2. Load fixtures 001-005 from `tests/resolver_witness/fixtures/`
3. Implement the resolver witness algorithm per `RESOLVER_WITNESS_SPEC_V1.md`
4. Serialize each fixture output with the canonical settings above
5. SHA-256 each serialized output
6. Compare to the registry and receipt

## 5. Expected Hashes

- `CONVERGENCE_001`: `ae4f530af2d5f4676dc9f0f102ed17bc465aa6824db69e69ecaf2249ccac71b3`
- `CONVERGENCE_002_HASH_MISMATCH`: `9b90567281c808d99f06fdb856cf6810cb36e8d51f4a5af53250118c3ce59974`
- `CONVERGENCE_003_REVOCABLE_PARENT`: `317c6594e7861bff755eb5f8901167a8f22c56db71b52a9eecedf8b8690b2296`
- `CONVERGENCE_004_MISSING_ATTESTATION`: `678470c5f4363a3f18fa9e41f7d812207434443bfb2a319e728ec7e0bf44b629`
- `CONVERGENCE_005_SCHEMA_VIOLATION`: `3ae2a0374b80a3a6c8e5b39b7292cd891a8ca9fee86f941d11a10e5399233f7f`

Match all five to verify `TWO_OBSERVER_CONSENSUS_VERIFIED_ON_MAIN`.

## 6. Non-Claim Boundary

Observer C must not assert three-observer canon from this document alone. A third independent implementation may extend verification coverage, but constitutional activation requires a separate activation receipt.

Current boundary:

- `TWO_OBSERVER_CONSENSUS_VERIFIED_ON_MAIN`
- `THREE_OBSERVER_CANON_NOT_YET_CLAIMED`
- `EXTERNAL_OBSERVER_PENDING`

## 7. Onchain Anchor Context

Audit Simulation attestation `0x49f0ce06b7119b796a063383beb3189b4da021327c112b6d1b63881689a3fd2b` on Base Mainnet provides immutable context that the fail-closed renderer behavior existed before this witness onboarding surface. It is informational for Observer C and not required for offline hash reproduction.

## 8. Verification Checklist

- [ ] Reproduced all five hashes exactly
- [ ] Used only the four artifacts listed
- [ ] Did not modify canonical serialization
- [ ] Recorded implementation language and runtime
- [ ] Preserved the non-claim boundary in the report
