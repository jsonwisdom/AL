# War Board Renderer Audit Simulation

**Simulation ID:** `WAR_BOARD_RENDERER_AUDIT_SIMULATION_V1`  
**Renderer Spec:** `RENDERER_SPEC_V1`  
**Purpose:** Prove the civic dashboard fails closed before dedicated onchain schema registration.

## Scenarios

| Scenario | Fixture | Expected Result |
|---|---|---|
| Valid inherits | `truth.valid-inherits.json` | Render tree with dashed gray `INHERITS` edges only |
| Ghost claim | `truth.ghost-claim.json` | Halt render with red breach banner |
| Corrupt source | `truth.corrupt.json` | Halt render as unreadable source |

## Pass Criteria

The renderer passes the simulation only if:

1. Current valid state renders no green edges.
2. Missing UID with dedicated onchain status produces `BREACH: Ghost Claim`.
3. Corrupt JSON produces `RENDER HALTED`.
4. No error path defaults to green.

## Constitutional Rule

No pixel may imply a receipt that does not exist.

The map is a servant of the law.
