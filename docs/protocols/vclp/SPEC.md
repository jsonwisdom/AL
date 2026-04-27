# VCLP v1.0

## Inputs

- source.pdf
- source.txt (byte-exact extraction)
- ledger.jsonl (append-only)

## Invariants

1. claim_text must match source bytes exactly
2. text_hash = sha256(claim_text)
3. prev_hash = sha256(previous ledger line)
4. append-only (no edits, no reorder, no delete)

## Verification

1. verify PDF hash
2. verify ledger hash
3. verify prev_hash chain
4. recompute text hashes

## Failure

Any mutation breaks at least one invariant.
