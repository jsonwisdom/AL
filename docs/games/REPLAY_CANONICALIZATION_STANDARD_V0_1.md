# Replay Canonicalization Standard v0.1

**SPEC_ID:** `REPLAY_CANONICALIZATION_STANDARD_V0_1`

## ROOT INVARIANT

If the bytes drift, the truth drifts.  
Canonicalization is the mathematics that prevents drift.

Everything else is theater.

## SOURCE_LINE

Replay requires byte-stable identity across languages, platforms, runtimes, and implementations.

---

## PURPOSE

Define the canonical mathematics for:

- canonical ordering
- encoding invariants
- hash determinism
- serialization guarantees
- cross-language convergence

This standard ensures that every receipt, bundle, challenge, and replay has a single, deterministic byte identity.

---

## CANONICALIZATION_OBJECT

A canonical object must define:

- `canonical_form`
- `canonical_order`
- `canonical_encoding`
- `canonical_hash`
- `canonical_schema`

Missing any → `NON_ADMISSIBLE`.

---

## 1. CANONICAL ORDERING

All objects must use:

- lexicographic key ordering
- stable array ordering
- no implicit ordering rules
- no runtime-dependent ordering

Ordering must be identical across:

- Python
- Go
- Rust
- JavaScript
- C++
- any verifier implementation

If ordering differs → `DIVERGENT`.

---

## 2. CANONICAL ENCODING

Encoding rules:

- UTF-8 only
- no BOM
- no locale dependence
- no platform-specific normalization
- no whitespace significance
- no trailing commas
- no implicit defaults

All encodings must be replay-stable.

---

## 3. CANONICAL SERIALIZATION

Serialization must be:

- deterministic
- schema-bound
- whitespace-agnostic
- ordering-stable
- language-independent

Allowed formats:

- canonical JSON
- canonical CBOR
- canonical MsgPack

Forbidden:

- YAML (ambiguous)
- XML (ordering drift)
- protobuf without deterministic mode

---

## 4. CANONICAL HASHING

Hashing rules:

- SHA-256 only
- computed over canonical bytes
- no compression drift
- no platform-dependent hashing
- no implicit normalization

Formally:

```text
canonical_hash = SHA256(canonical_bytes)
```

If canonical bytes differ → hash differs → `DIVERGENT`.

---

## 5. CROSS-LANGUAGE CONVERGENCE

Canonicalization must converge across:

- languages
- runtimes
- compilers
- architectures
- operating systems

If any implementation produces different canonical bytes → canonicalization failure.

---

## 6. CANONICAL SCHEMA

Every canonical object must declare:

- required fields
- field types
- field ordering
- allowed values
- forbidden values
- nullability rules

Schema drift → `NON_ADMISSIBLE`.

---

## 7. INVALID CANONICALIZATION CONDITIONS

Canonicalization is invalid if:

- ordering differs
- encoding differs
- serialization differs
- schema differs
- hash differs
- environment affects output

Invalid canonicalization → invalid receipt → invalid bundle → invalid replay.

---

## CHECK CONDITION

An object enters check when canonical bytes are requested.

## CHECKMATE CONDITION

Checkmate occurs when:

- canonical bytes cannot be reconstructed
- canonical hash mismatch
- ordering mismatch
- encoding mismatch
- schema mismatch
- cross-language divergence

Checkmate is mechanical, not rhetorical.

---

## WIN CONDITION

Goodies win when canonical bytes converge across all implementations.  
Goobers lose when canonical bytes drift under scrutiny.

---

## FINAL RULE

Canonicalization is the mathematics of truth.  
If the bytes drift, the truth drifts.

**Proof over narrative.**
