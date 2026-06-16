# Arcade ZK Rule Engine v0.2

## Status

SCAFFOLD_NOT_PROVEN

## Rule

A SnapBack Easter egg is valid only if:

1. It belongs to the declared episode.
2. It matches the declared public egg ID.
3. Replay count meets the minimum threshold.
4. Player, episode, replay count, and egg ID are bound into the Merkle leaf.
5. The leaf is included in the public Merkle root.

## No Fake Green

This circuit is not considered GREEN until:

- Noir project compiles.
- Witness generation succeeds.
- Proof generation succeeds.
- Tower verifier accepts proof.
- zk-receipt records actual proof metadata.
