# Computer Wisdom Public Proof — Verify It Yourself

## The idea (plain English)

You don’t have to trust a post, a person, or a platform.

You can check the proof yourself.

- GitHub holds the exact files (the bytes)
- A hash (Merkle root) summarizes those files
- This page recomputes the hash in your browser and compares it to what was posted

If they match → it’s real
If they don’t → it’s not

## Quick verify (30 seconds)

1. Open the verifier page in this folder: `verify.html`
2. Paste the **GitHub commit SHA** from the post
3. Paste the **Merkle root / SHA-256** from the post
4. Click **Verify**

You’ll see:

- **VERIFIED** (green) if the bytes match
- **MISMATCH** (red) if they don’t

No login. No wallet. No platform permission.

## Why this works

Platforms (Meta/Facebook, X, etc.) can:

- throttle reach
- remove posts
- change feeds

They **cannot** change the bytes in GitHub or the hash you recompute locally.

That’s why proof is portable.

## What you’re checking

The verifier pulls JSON files from:

```
_truth/tasks/queue/
```

at the exact commit you provide, converts them to a canonical format (sorted keys), and computes a SHA-256 hash.

It compares that to the hash in the post.

## Optional: on-chain witness

Sometimes a post will also include an on-chain link (Base / EAS).

That’s a **witness** — a timestamped pointer to the same hash.

It’s helpful, but not required to verify the bytes.

## Bottom line

- GitHub = source of truth (bytes)
- This page = verification tool (recompute hash)
- Chain = optional witness (public timestamp)
- Platforms = distribution only

**If the hash matches, the proof is real.**
