# 001 — Witness Protocol

**Question:** How does AL handle replay divergence?  
**Authority:** false  
**Memory type:** procedural

A court in AL does not decide who is right.

A court determines which replay survives.

When two replays diverge:

1. Collect the receipts.
2. Reconstruct each replay.
3. Compare the resulting transitions.

If one replay reconstructs and the other does not, the reconstructable replay stands.

If both reconstruct but diverge, preserve both branches.

If neither reconstructs, reject both.

The court does not interpret intent.
The court does not elevate claims.
The court does not generate authority.

Witnesses are not people.

Witnesses are receipts.

Authority remains false.
