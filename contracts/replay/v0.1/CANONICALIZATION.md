# Replay Envelope Canonicalization v0.1

## Purpose

This document defines the byte-exact canonicalization regime for `Replay Envelope v0.1`.

The envelope is the minimal unit of replay adjudication. Invocation contracts and verdict states must reference the envelope; they must not redefine it.

## Constitutional Rule

No runtime entropy may enter the replay envelope.

The envelope is law only if its canonical bytes are reproducible by a public stranger.

## Canonicalization Rules

1. **Encoding**
   - All envelope bytes MUST be UTF-8.

2. **Unicode**
   - All string values MUST be normalized to NFC before canonical JSON serialization.

3. **JSON Canonicalization**
   - Objects MUST use lexicographic key ordering at every object level.
   - JSON MUST be compact: no whitespace outside string literals.
   - String content MUST be preserved after NFC normalization.
   - Case MUST be preserved.

4. **Runtime Fields Forbidden**
   - The following fields are forbidden anywhere inside an envelope:
     - `timestamp_generated`
     - `generated_at`
     - `created_at`
     - `updated_at`
     - `uuid`
     - `random`
     - `rand`
     - `nonce`

5. **Hashing**
   - `envelope_canonical_hash` MUST equal SHA-256 of the canonical JSON envelope with `integrity.envelope_canonical_hash` omitted.
   - The stored form MUST use `sha256:<64 lowercase hex>`.
   - `SHA256SUMS` entries MUST be computed over byte-exact file contents.

6. **Verdicts Excluded**
   - Replay verdicts are outputs of replay, not inputs to replay.
   - The envelope may specify expected replay result for test purposes, but final verdict objects must be defined separately.

## Dependency Order

Replay subtree order is fixed:

```text
Envelope -> Invocation Contract -> Verdict States -> CI Gate
```

Changing this order creates drift because invocation and verdicts depend on envelope fields.

## Public Stranger Test

A stranger must be able to:

1. Clone the repository.
2. Read `contracts/replay/v0.1/envelope.schema.json`.
3. Canonicalize a replay envelope according to this document.
4. Recompute the envelope hash.
5. Run the declared entrypoint.
6. Compare replay output against the expected replay result.

If any of those steps requires private state, the envelope is not admissible.

## Non-Authority Clause

A valid envelope proves only that the replay input was well-formed and hashable.

It does not prove truth.

It does not prove legal authority.

It does not prove semantic correctness.

It only creates a stable surface for replay adjudication.
