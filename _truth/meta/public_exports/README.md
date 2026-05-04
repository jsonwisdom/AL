# Computer Wisdom Public Proof — Verification Guide

## What this is

This folder defines how Computer Wisdom proof works **outside of any platform (Meta/Facebook, X, etc.)**.

Platforms can distribute content. They do not control truth.

## Core Rule

```
GitHub = source of truth (bytes)
ALMS = proof (hashes)
Public chain = witness (optional pointer)
Platforms = distribution only
```

## How to Verify a Post

When you see a Computer Wisdom post, it should include:

- GitHub commit link
- Merkle root or receipt hash
- Optional on-chain pointer

### Step 1 — Open GitHub

Follow the commit link and view the files in the repo.

### Step 2 — Check the bytes

Look at:

- `_truth/tasks/queue/`
- `_truth/tasks/merkle/root.txt`
- `_truth/meta/policies/`

These are the canonical artifacts.

### Step 3 — Recompute the root (advanced)

Run:

```bash
jq -cS '.' _truth/tasks/queue/*.json | sha256sum
```

Compare with:

```
_truth/tasks/merkle/root.txt
```

If they match, the task set is valid.

### Step 4 — Optional: Check on-chain pointer

If provided, open the Base/EAS link.

Confirm the Merkle root or hash matches the repo.

## Why this matters

- If a platform deletes the post → proof still exists
- If a platform suppresses reach → proof is still verifiable
- If a platform lies → the bytes win

## Key Guarantee

Computer Wisdom proof **does not depend on platform permission**.

Anyone can verify independently using GitHub and (optionally) the public chain.

## Status

```
INTENT_DEFINED — public proof path established
```

On-chain export will be added only when the operator explicitly chooses to publish a pointer.
