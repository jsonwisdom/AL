# Invocation Canonicalization v0.1

## Purpose

This document defines the byte-exact canonicalization rules for `contracts/invocation/v0.1/invocation.schema.json`.

Invocation is the lawful bridge between sealed replay envelopes and `verify.sh` execution.

No other replay input surface is legal.

## Constitutional Rule

The invocation object must be deterministic before execution.

Runtime observations belong in Verdict and Receipt artifacts, never in Invocation.

## Canonicalization Rules

1. **UTF-8 only**
   - All invocation files MUST be encoded as UTF-8.

2. **NFC strings**
   - Every string value MUST be normalized to Unicode NFC before hashing.

3. **JCS-style JSON**
   - Keys MUST be sorted lexicographically at every object level.
   - JSON MUST be compact: no whitespace outside string literals.
   - Case MUST be preserved.

4. **Content-addressed invocation ID**
   - `invocation_id` MUST equal:

```text
sha256(canonical_json_without_invocation_id_field)
```

   - The stored form MUST be:

```text
sha256:<64 lowercase hex>
```

5. **Forbidden entropy fields**
   - The following field names are forbidden at invocation root:

```text
seed
nonce
timestamp_generated
debug
cache
env
uuid
random
created_at
updated_at
```

6. **Network disabled**
   - `options.network` MUST be `disabled`.
   - Any replay requiring network state is not invocation-admissible under v0.1.

## Handler Dependency

The future handler must follow this order:

```text
parse -> validate schema -> recompute invocation_id -> verify envelope_sha256 -> execute entrypoint -> emit Verdict v0.1
```

If any step fails, the handler must emit a typed invalid/error verdict, not a partial success.

## Non-Authority Clause

A valid invocation proves only that replay input was deterministic and well-formed.

It does not prove truth.

It does not prove legal authority.

It does not prove semantic correctness.

It only creates a lawful bridge into replay adjudication.
