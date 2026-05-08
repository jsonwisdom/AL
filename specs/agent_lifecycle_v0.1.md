# Agent Lifecycle v0.1

Status: DESIGN_SPEC_ACTIVE
Operational status: ACTIVE_FOR_REVIEW
Scope: `agents/*/manifest.yaml`, agent introduction, amendment, deprecation, and retirement

## Purpose

Agent lifecycle governance defines how constitutional agents are born, amended, deprecated, and retired.

Birth, operation, amendment, and death must all be replay-visible.

No agent may appear, expand, disappear, or be disabled silently.

## Core Principle

```json
{
  "agent_birth": "PROPOSED_BY_PR",
  "agent_operation": "MANIFEST_BOUND",
  "agent_amendment": "SCOPE_CHANGE_REQUIRES_PUBLIC_DIFF",
  "agent_deprecation": "AUDITABLE_NOT_SILENT",
  "agent_retirement": "HISTORY_PRESERVED",
  "no_ghost_anchor": true
}
```

## Lifecycle States

Allowed lifecycle states:

```json
[
  "proposed",
  "active_for_review",
  "active",
  "deprecated",
  "retired"
]
```

## 1. Proposal

A new agent must be introduced by PR.

Required PR label:

```text
agent-introduction
```

Required PR description:

```text
Agent name:
Agent kind:
Public records observed:
Constitutional verdicts emitted:
Why existing agents cannot do this:
Runtime limits:
Targets file:
Constitutional basis:
```

A proposed agent must include:

- `agents/<name>/manifest.yaml`
- target file if it observes public endpoints
- tests for runtime surface
- no operational secrets
- no RAP access unless explicitly specified by a future RAP implementation spec

## 2. Amendment

Changing any of the following requires an amendment PR:

- `kind`
- `allowed_domains`
- `allowed_url_schemes`
- `allowed_tags`
- `allowed_verdicts`
- `forbidden_fields`
- `runtime_limits`
- `targets_file`
- output surfaces

Required PR label:

```text
agent-amendment
```

Required rationale:

```text
Amended fields:
Prior scope:
New scope:
Reason amendment is necessary:
Membrane impact:
Tests updated:
```

Scope may only expand through amendment.

Scope must not expand through code alone.

## 3. Deprecation

An agent enters `deprecated` state by PR.

Required PR label:

```text
agent-deprecation
```

Deprecation requirements:

- manifest remains in place
- runtime refuses to load deprecated agents
- deprecation rationale is recorded
- replacement agent, if any, is named
- final active receipt count is recorded when available

No agent may be disabled only by commenting it out of a workflow.

## 4. Retirement

After deprecation, an agent may be retired by PR.

Required PR label:

```text
agent-retirement
```

Retirement requirements:

- code may be removed after deprecation window
- manifest must move to `agents/_retired/<agent_id>/manifest.yaml`
- retirement receipt or changelog entry should record:
  - final lifecycle state
  - final receipt count when available
  - replacement agent if any
  - retirement rationale

Retirement preserves history.

Retirement is not deletion from constitutional memory.

## 5. Forbidden Practices

The following are forbidden:

- adding an agent without manifest
- expanding scope in code without manifest amendment
- disabling agent by comment-only workflow change
- deleting agent history without retirement path
- introducing `kind: adjudicator`
- adding verdicts outside manifest scope
- adding hidden output fields
- using lifecycle changes to erase constitutional debt

## 6. Runtime Loader Requirements

A runtime loader should refuse to execute an agent when:

- manifest is missing
- manifest schema validation fails
- lifecycle is `deprecated`
- lifecycle is `retired`
- operational_state is `DISABLED` or `DEPRECATED`
- runtime limits are absent
- allowed verdicts are absent

## 7. Auditability

The constitutional actor registry is:

```text
git log -- agents/*/manifest.yaml agents/_retired/*/manifest.yaml
```

This registry must remain sufficient to answer:

- when an agent was proposed
- when it became active
- when its scope changed
- when it was deprecated
- when it was retired
- what it was allowed to emit at each point in time

## 8. Non-Claims

Agent lifecycle state does not prove:

- correctness
- trustworthiness
- authority
- legitimacy
- institutional endorsement

Lifecycle state proves only that the agent's constitutional status is explicit and replay-visible.

## State

```json
{
  "agent_lifecycle_v0_1": "DESIGN_SPEC_ACTIVE",
  "birth": "GOVERNED",
  "operation": "GOVERNED",
  "amendment": "GOVERNED",
  "deprecation": "GOVERNED",
  "retirement": "GOVERNED",
  "no_ghost_anchor": true
}
```
