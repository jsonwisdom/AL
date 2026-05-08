# Seed Epistemic Kernel

Git for reasoning.

Fork an assumption.
Replay a derivation.
Diff the divergence.

## Constitutional Triangle

- Claim = epistemic state
- Transform = epistemic motion
- Viewport = epistemic jurisdiction (future primitive)

## Purpose

This is a minimal local-first provenance kernel.

Not a blockchain.
Not an ontology engine.
Not a governance cathedral.

A small replayable substrate proving that reasoning can be:

- claimed
- transformed
- replayed
- forked
- exported
- imported
- diffed

## MVP Scope

- SQLite or JSONL storage
- content-addressed claims
- transform receipts
- deterministic replay
- branch/fork support
- local-first operation

## Non-Goals

- no global registry
- no consensus engine
- no token
- no access-control framework
- no policy engine

## First Success Condition

```bash
python seed-kernel/demo/alice_bob_demo.py
```

…and a user can observe replayable reasoning divergence locally.

Origin:
- AL#136
