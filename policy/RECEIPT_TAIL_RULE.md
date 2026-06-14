# RECEIPT_TAIL_RULE

## STATUS: ACTIVE_POLICY
## AUTHORITY: FALSE
## VERIFIED: FALSE
## PRODUCTION_GREEN: FALSE
## NO_FAKE_GREEN: TRUE

Every CI receipt commit can trigger another CI run.

This creates an infinite receipt tail unless bounded.

## Rule

A receipt tail may be observed up to depth 3.

After depth 3, the tail is treated as a tail witness, not as a new proof obligation.

## Definitions

Depth 0:
The artifact or enforcement change.

Depth 1:
The first CI run proving the artifact or enforcement change.

Depth 2:
The receipt preserving the first CI run.

Depth 3:
The CI run triggered by the receipt commit.

## Stop Condition

If depth 3 passes, the system may record:

`TAIL_BOUND_REACHED`

This does not create production GREEN.

## Brenda Boundary

Brenda may block failed tail receipts.

Brenda may not create truth or authority from tail recursion.

## Ruling

No infinite CI receipt recursion.
No fake green.
