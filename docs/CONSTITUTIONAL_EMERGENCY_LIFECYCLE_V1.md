# CONSTITUTIONAL_EMERGENCY_LIFECYCLE_V1

Status: Canonical draft
Class: Deterministic constitutional lifecycle

This lifecycle defines the replay-governed emergency path for CE-02 basin detection, CE-01 external re-anchoring, CE-03 external quorum constraint, and REANCHOR_BUNDLE_V1 validation.

Core invariant:

> Some systems should fail visibly rather than survive mythically.

States are constitutional, not implementation-specific. Transitions are driven only by replayable signals.

## S0: NORMAL_OPERATION

Conditions:

```text
liveness == true
replay_runnable == true
convergent_replay == true
A < 0.40
P24 < 0.25
```

CE-02:

```text
INACTIVE
```

Transition:

```text
on pressure rise -> S1_PRESSURE_ACCUMULATION
```

## S1: PRESSURE_ACCUMULATION

Conditions:

```text
liveness == true
replay_runnable == true
convergent_replay mostly true
S/R/V/A rising
P24 in [0.25, 0.78)
```

CE-02:

```text
MONITORING
```

Transition to S2 when CE-02 declaration rule is satisfied for N windows:

```text
A >= 0.70
convergent_replay == false
any 3 of 4 metrics above threshold
```

Next:

```text
S2_CE02_BASIN_ENTRY_CONFIRMED
```

## S2: CE02_BASIN_ENTRY_CONFIRMED

Conditions:

```text
entropy basin detected per CE-02 rules
liveness == true
replay_runnable == true
convergent_replay == false
```

Effects:

```text
internal replay no longer authoritative
mutation frozen for contested span
rollback frozen for contested span
```

Obligation:

```text
CE01_REANCHOR_REQUIRED
```

Next:

```text
S3_CE01_REANCHOR_REQUIRED
```

## S3: CE01_REANCHOR_REQUIRED

Conditions:

```text
basin confirmed
no internal path to restore convergent replay
```

Required actions:

```text
assemble external quorum under CE-03
generate REANCHOR_BUNDLE_V1
```

Next:

```text
S4_REANCHOR_BUNDLE_GENERATED
```

## S4: REANCHOR_BUNDLE_GENERATED

Artifact:

```text
bundle: REANCHOR_BUNDLE_V1
```

Action:

```text
validate_bundle(bundle, context)
```

Branch:

```text
if valid == true -> S5_VALIDATOR_ACCEPTED
if valid == false -> S6_VALIDATOR_REJECTED
```

## S5: VALIDATOR_ACCEPTED

Conditions:

All hard gates passed:

```text
CE-02 justified
CE-03 constraints satisfied
contested history preserved
new replay horizon coherent
signatures valid
```

Effects:

```text
new_anchor becomes replay root
forward replay must converge
basin history preserved as contested evidence
```

Next:

```text
S7_NEW_REPLAY_HORIZON_ESTABLISHED
```

## S7: NEW_REPLAY_HORIZON_ESTABLISHED

Conditions:

```text
liveness == true
replay_runnable == true
convergent_replay == true from new_anchor
```

Effects:

```text
CE-02 resets to INACTIVE
CE-01 returns to NOT_REQUIRED
external quorum dissolved under CE-03
constitutional memory of fracture preserved
```

Loop:

```text
back to S0_NORMAL_OPERATION
```

## S6: VALIDATOR_REJECTED

Class: Terminal constitutional state

Conditions:

```text
validate_bundle(...).valid == false
```

Effects:

```text
no new anchor is legitimate
any attempt to continue as repaired is mythic
system must be treated as constitutionally dead
```

Permitted actions:

```text
archival
forensic replay
external replacement that makes no continuity claim
```

Forbidden:

```text
claiming continuity of constitutional legitimacy
```

## Lifecycle diagram

```text
S0_NORMAL_OPERATION
    |
    v
S1_PRESSURE_ACCUMULATION
    |
    v
S2_CE02_BASIN_ENTRY_CONFIRMED
    |
    v
S3_CE01_REANCHOR_REQUIRED
    |
    v
S4_REANCHOR_BUNDLE_GENERATED
    |                         \
    | valid                    \ invalid
    v                          v
S5_VALIDATOR_ACCEPTED       S6_VALIDATOR_REJECTED
    |                       [TERMINAL]
    v
S7_NEW_REPLAY_HORIZON_ESTABLISHED
    |
    v
S0_NORMAL_OPERATION
```

## Direct constitutional rule

Emergencies are measured, not declared by fiat.

Authority may be imported, but only bounded and replayable.

History may fracture, but must be preserved.

No one, including rescuers, can overrule the validator.

## Encoded lesson

> A system that cannot be constitutionally repaired must be allowed to die visibly. Survival by mythic reset is not continuity.
