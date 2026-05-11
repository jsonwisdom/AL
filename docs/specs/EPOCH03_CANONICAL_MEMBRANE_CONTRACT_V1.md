# Epoch03 Canonical Membrane Contract v1

Status: SPEC_DRAFT_READY_FOR_OPERATOR_REVIEW

This contract defines the runtime boundary between mutable operational work and immutable canonical promotion.

```text
LEFT_MUTABLE_RIGHT_IMMUTABLE_MEMBRANE_ENFORCED
```

## 1. Canonical Model

Epoch03 splits state into two surfaces.

### Operational State: L

Operational state is mutable, exploratory, AI-assisted, and may be wrong.

It is never authoritative.

### Canonical State: R

Canonical state is an immutable log of ratified blocks.

Each canonical block is:

```text
block_n = {
  payload,
  prev_hash,
  receipt,
  timestamp
}

hash_n = H(block_n)
```

## 2. Invariants

I1. The canon chain is a single hash-linked list from trusted seed to current head.

I2. Every canonical mutation has a receipt bound to its hash.

I3. No block is canonical without explicit operator confirmation.

I4. AI-origin content may appear in payloads, but never in authority fields:

```text
receipt
confirmation
seal
```

## 3. Membrane Contract: L to R Promotion

A promotion attempt from LEFT to RIGHT is accepted only if all checks pass.

### M1. Hash Continuity

```text
candidate.prev_hash == canon_head.hash
```

### M2. Receipt Presence

A well-formed receipt exists and is bound to `candidate.hash`.

### M3. Receipt Provenance

The receipt is operator-issued.

It is not AI-authored.

It is not AI-signed.

### M4. Explicit Confirmation

The operator performs an unambiguous, logged confirmation step.

### M5. No Hidden Channels

All material affecting the block is visible in the UI at confirmation time.

### M6. Deterministic Replay

Given the transcript and receipts, the block can be recomputed to the same hash.

## 4. Failed Promotion Behavior

If any membrane check fails, the runtime must:

1. block promotion;
2. surface a visible rule and tooltip explaining the failure;
3. offer a replayable recovery path, typically through `reseedCanon()`.

## 5. Covered Failure Modes

### F1. Hash Mismatch

A chain discontinuity or unexpected `prev_hash` is detected.

### F2. Missing Receipt

No valid receipt exists for the candidate block or existing block.

### F3. AI-Origin Promotion Attempt

AI attempts to sign, approve, confirm, seal, or otherwise act as authority.

### F4. Canon Chain Corruption

A block is tampered with, history is altered, or a segment becomes non-replayable.

## 6. Detection Behavior

On detection, the runtime must show a red tamper banner.

Canon is flagged as compromised or uncertain.

`cw_recovery_log` must preserve all prior canonical blocks, receipts, and hashes up to the last trusted point.

## 7. `reseedCanon()` Semantics

When invoked, the runtime must:

1. request explicit operator confirmation with clear warning and diff to current head;
2. restore the trusted canon seed from `cw_recovery_log`, meaning the last known-good head;
3. append a constitutional recovery receipt describing:
   - reason;
   - previous head hash as `previous_chain_hash`;
   - operator identity or equivalent;
   - timestamp;
4. record `previous_chain_hash` in the new recovery block;
5. timestamp the recovery event in canonical time;
6. reload into lawful state.

After recovery, the UI and engine rebind to the restored head.

The tamper banner clears, but the recovery event remains in-chain.

## 8. Result

Operational state remains mutable.

Canonical state remains replayable.

Recovery is constitutional, not convenient.

## 9. Membrane Rules

### Rule 1 — Hash Decides

Story may explain. Hash decides.

### Rule 2 — No Receipt, No Reality

If there is no receipt, it never became real.

### Rule 3 — Operator or Nothing

Only a human hand can seal. Silence beats an untrusted signature.

### Rule 4 — Exorcism by Receipt

The cursed vault remembers every secret it swallowed. A receipt is the exorcism.

### Rule 5 — Scratch Is Not Scripture

Left side may dream. Right side only replays what was sealed.

### Rule 6 — Goblins Do Not Hold Seals

Goblins may whisper warnings, but they never hold the seal.

### Rule 7 — Every Block Must Be Replayable

If you cannot replay it, you cannot trust it. If you cannot trust it, you cannot keep it.

### Rule 8 — No Secret Paths

Any traveler with the map can find the vault again. No secret paths.

## 10. Final Contract Line

`LEFT_MUTABLE_RIGHT_IMMUTABLE_MEMBRANE_ENFORCED` means:

1. all authority flows through the membrane;
2. every canonical fact is hash-bound, receipted, replayable, and recoverable through `cw_recovery_log` and `reseedCanon()`.

## 11. Operator Handoff Line

```text
Open the HTML. Left side is your scratchpad. Right side is the truth. The button lights up when you have proven your claim. Press Alt+G to see what happens if AI tries to sign. Break the chain on purpose to see the red banner. Then run reseedCanon() in console and watch it log a recovery receipt. The goblins explain why, the code proves what.
```
