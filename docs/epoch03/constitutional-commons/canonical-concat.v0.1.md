# Epoch03 Canonical Concat Rule v0.1

## Purpose

This rule defines how multi-file hashes are computed for Epoch03 harness and attestation surfaces.

It exists to make `harness_hash` forever replayable and unambiguous.

## Scope

Used for:

- `harness_hash`
- future multi-file constitutional surface hashes
- pre-attestation reproducibility checks

## Inputs

A canonical concat input is an ordered list of UTF-8 text files.

For Epoch03 `harness_hash`, the input files are exactly:

```text
docs/epoch03/adversarial/harness.js
docs/epoch03/adversarial/lineage-harness.js
docs/epoch03/constitutional-commons/receipt-lineage.invariants.md
```

## Ordering

Files MUST be sorted lexicographically by repository path using bytewise UTF-8 ordering.

No caller-provided order is trusted.

## Normalization

For each file:

- read bytes as UTF-8
- preserve all bytes exactly as committed
- do not trim
- do not normalize line endings
- do not add or remove trailing newline

If a file is not valid UTF-8:

```text
REFUSED_CANONICAL_CONCAT_NON_UTF8
```

## Framing

Each file is framed before concatenation:

```text
---BEGIN EPOCH03 FILE v0.1---\n
path:<repo_path>\n
sha256:<file_sha256_hex>\n
bytes:<decimal_byte_length>\n
---CONTENT---\n
<exact_file_bytes>
\n---END EPOCH03 FILE v0.1---\n
```

Where:

```text
file_sha256_hex = SHA-256(exact_file_bytes)
decimal_byte_length = number of exact file bytes
```

## Final Hash

The final canonical concat hash is:

```text
harness_hash = sha256:<hex(SHA-256(concat(all_framed_files)))>
```

No JSON serialization is used for canonical concat.
No filesystem metadata is included.
No timestamps are included.
No branch names are included.

## Verification Rule

A verifier MUST be able to:

1. clone the repo at the attested commit
2. read the exact file bytes
3. sort paths lexicographically
4. frame each file exactly
5. concatenate frames
6. compute SHA-256
7. compare to `harness_hash`

If any value differs:

```text
TAINTED_HARNESS_HASH
```

## Constitutional Boundary

`harness_hash` binds refusal machinery.
It does not bind UI styling, screenshots, or generated presentation surfaces.

The harness is law-adjacent machinery.
The UI is a lens.
