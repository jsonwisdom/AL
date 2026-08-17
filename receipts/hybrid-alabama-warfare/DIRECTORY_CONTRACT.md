# Hybrid Alabama Warfare — Receipt Directory Contract v0.1

Authority created: `false`

Admitted:
- append-only replay receipts
- artifact digests
- source references
- CI/readback checkpoints
- explicit HOLD/GAP/CONFLICT states

Forbidden semantic promotions:
`RECEIPT != TRUTH`
`RECEIPT != AUTHORIZATION`
`RECEIPT != LEGAL_FINDING`
`CI_SUCCESS != WORLD_TRUE`

History is append-only. Corrective receipts supersede interpretation where stated but do not erase earlier states.
