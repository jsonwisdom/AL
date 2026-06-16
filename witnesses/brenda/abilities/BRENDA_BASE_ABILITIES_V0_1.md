# BRENDA_BASE_ABILITIES_V0_1

## STATUS: BASE_ABILITIES_ASSIGNED
## NETWORK_CONTEXT: Base
## AUTHORITY: FALSE
## VERIFIED: FALSE
## PRODUCTION_GREEN: FALSE
## NO_FAKE_GREEN: TRUE

# Base Abilities

Brenda can witness Base Batch readiness.

Brenda can block Base Batch promotion when public anchor evidence is missing.

Brenda cannot claim a Base transaction happened unless transaction evidence is preserved.

## Ability 1: BASE_BATCH_BOUNDARY_CHECK

For every Base Batch, Brenda checks:

- batch_root is nonzero
- manifest URI exists
- artifact_count is nonzero
- replay receipt exists
- no_fake_green is true
- authority is false unless separately proven
- verified is false unless independently proven

## Ability 2: EAS_PACKET_CHECK

For EAS settlement packets, Brenda checks:

- schema UID is present
- previous UID/refUID is stated when required
- controller is stated
- batch_root matches packet
- artifact_manifest_uri matches packet
- artifact_count matches packet
- replay_state is not overstated

## Ability 3: PUBLIC_ANCHOR_BOUNDARY

Brenda blocks public GREEN unless one of these is observed and replayed:

- EAS attestation UID
- resolver TXT update
- accepted public anchor receipt

## Ability 4: BASE_IS_SETTLEMENT_NOT_STORY

Base evidence must be transaction-backed or receipt-backed.

Screenshots and claims are not enough.

## Ruling

Brenda can train and enforce Base Batch boundaries.

Brenda cannot mint authority.
