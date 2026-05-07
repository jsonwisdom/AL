# CostCutter Policy v1

## Authority
CostCutter Level 1 may auto-cancel subscriptions under $5.00 only when all gates pass.

## Human Approval Required
- Any action greater than or equal to $5.00
- New vendor authorization
- Wallet limit change
- Policy change

## Freeze Conditions
- Policy hash mismatch
- Missing execution pointer
- Unauthorized vendor
- Spend or cancel amount greater than or equal to $5.00
- Three failed replays

## Receipt Discipline
Every action must emit a receipt.
No receipt means no authority.
No policy hash means no execution.
