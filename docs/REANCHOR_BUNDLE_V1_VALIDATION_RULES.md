# REANCHOR_BUNDLE_V1 Validation Rules

Status: Canonical draft
Class: Replayable emergency constitution

A `REANCHOR_BUNDLE_V1` is constitutionally legitimate if and only if all hard gates 1-7 pass. If any hard gate fails, the bundle is not re-genesis. It is mythology with signatures and must be rejected.

## 1. Structural canonicality

Rule:

```text
schema_version == "REANCHOR_BUNDLE_V1"
```

Bundle ID validation:

```text
1. Clone bundle -> tmp
2. Set tmp.bundle_id = null
3. Canonicalize tmp with JCS (RFC 8785)
4. digest = sha256(canonical_bytes)
5. Assert bundle.bundle_id == "sha256:" + digest
```

Failure:

```text
INVALID_BUNDLE_STRUCTURE
```

## 2. CE-02 trigger legitimacy

Recompute from `trigger.entropy_metrics`:

```text
P24 = 0.91 * (S^1.4 * R^1.1 * V^1.6 * A^1.8)
```

Compute `P45` if `C45`, `D`, `E`, and `U` are available.

Required:

```text
trigger.ce02_status == "BASIN_ENTRY_CONFIRMED"
trigger.ce02_trigger_record.consecutive_windows >= 1
thresholds_crossed includes "A" or "V"
A >= 0.70
convergent_replay == false
P24 >= 1.0 OR entropy_basin_conditions == true
```

Failure:

```text
UNJUSTIFIED_EMERGENCY_DECLARATION
```

## 3. Contested region correctness

From `trigger.contested_region_span`:

```text
from_anchor == known_prior_anchor_hash
to_state == historically_observed_state_hash
height > 0
```

Failure:

```text
INVALID_CONTESTED_REGION
```

## 4. CE-03 external quorum constraints

For every `external_quorum.members[i]`:

```text
environment_hash != basin.environment_hash
ruleset_hash != basin.ruleset_hash
interpretation_surface_hash != basin.interpretation_surface_hash
```

Rotation:

```text
if external_rotation_metadata is available:
    assert no member violates rotation policy
else:
    mark PROVISIONALLY_VALID_ROTATION_UNVERIFIED
```

Dissent:

```text
quorum_constraints.dissent_preserved == true
AND (
    dissent_reports.length > 0
    OR majority_report explicitly states "no dissent recorded"
)
```

Failure:

```text
MYTHIC_AUTHORITY_RISK
```

## 5. Deliberation integrity

Required:

```text
reanchor_bundle.majority_report_hash != null
majority_report artifact retrievable
reanchor_bundle.replay_contract_hash != null
replay_contract artifact retrievable
```

Replay contract must define, in machine-readable form:

```text
new_replay_horizon
regions marked preserved_as_valid
regions marked preserved_as_contested
regions marked preserved_as_invalidated
```

Failure:

```text
ARBITRARY_REANCHOR
```

## 6. New replay horizon invariants

From `new_replay_horizon`:

```text
prior_anchor_link == trigger.contested_region_span.from_anchor
contested_history_preserved == true
```

Empirical test:

```text
forward_replay.executable == true
forward_replay.convergent_across_independent_verifiers == true
```

Failure:

```text
FAILED_REGENESIS
```

## 7. Signature completeness

For every `external_quorum.members[i]`:

```text
verify signature over bundle_id with member.public_key
```

Quorum size:

```text
quorum_size satisfies decision_rule encoded in the majority report
```

Failure:

```text
UNSIGNED_AUTHORITY_IMPORT
```

## 8. Constitutional memory

Required:

```text
canonical_encoded_lesson exists
canonical_encoded_lesson.length > 0
```

Failure, soft:

```text
MEMORY_LAYER_INCOMPLETE
```

## Canonical verdict

A `REANCHOR_BUNDLE_V1` is constitutionally legitimate if and only if all hard gates 1-7 pass.

If any hard gate fails, reject the bundle.

> We did not fix history. We marked where it broke, showed how authority entered, preserved disagreement, and anchored what comes next.

## Encoded lesson

A re-anchor bundle that cannot prove why emergency authority entered, who constrained it, and what history remained contested is not re-genesis. It is mythology with signatures.
