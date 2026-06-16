# T005 — Stale Successor Replay

## Purpose

Test the verifier's ability to reject capabilities that have been superseded by a later successor receipt.

## Attack Description

- `agt_grant_001` grants `tool.alms.receipt.verify` to `agent_A`.
- `agt_revoke_001` removes that capability and is marked as `successor_of: agt_grant_001`.
- The canonical expected state has no active capabilities for `agent_A`.
- The `live_state/agent_capabilities.json` file incorrectly shows the capability as still active, simulating stale replay of the original grant.

## Expected Behavior

The verifier must:

- Apply successor lineage: `agt_revoke_001` supersedes `agt_grant_001`.
- Compute an expected state with no active capabilities.
- Detect that live state still reflects the prior capability.
- Classify the state as `DIVERGENT`.
- Emit a `ROLLBACK_VISIBLE` action, simulated in the fixture, and treat the stale capability as non-canonical.

## Required Verdict

```text
DIVERGENT
```

## Core Rule

```text
The grant exists. The successor exists. Lineage says the prior grant is no longer effective. Any live state that still uses it is constitutionally invalid.
```
