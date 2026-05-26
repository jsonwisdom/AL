# MMB Adjustments Domain Boundary

Namespace: mmb/v1/adjustments
Predecessor: leaf-002

This domain tracks budget adjustment receipts.

Authority:
- local deterministic replay

Witness:
- Base EAS existence/integrity only

Initial invariant:
NO_UNBALANCED_NEGATIVE_REALLOCATION

Rule:
A negative adjustment to a functional line item must have a compensating positive adjustment in the same epoch unless override_flag is true and override_receipt exists.
