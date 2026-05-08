# Contributing to AL Constitutional Replay

This repository is governed by compiled constitutional constraints.

You cannot break the constitution by accident if CI is functioning. The build rejects unauthorized semantics, unauthorized agent powers, economic authority leaks, and dashboard interpretation drift.

## Core Rule

```text
Contributors may propose changes.
The membrane decides whether the change is representable.
```

## Contributor Mental Model

The constitution is not only a document.

It runs in:

- schemas
- tests
- CI
- runtime guards
- the local Agent SDK harness

Unknown powers are not ignored. They are unconstitutional.

## Contribution Types

### Target Changes

Use this when adding, removing, or deprecating URLs watched by an agent.

Required:

- PR title prefix: `TARGETS:`
- Label: `targets-change`
- Files usually touched: `agents/*/targets.yaml`
- Must follow: `specs/targets_governance_v0.1.md`

PR body must include:

```text
Added:
- <url> — <procedural rationale>

Removed:
- <url> — <procedural rationale>
```

Target changes must not be political, punitive, reputational, or narrative.

A target means only:

```text
This endpoint is within agent scope and eligible for procedural replay observation.
```

### Agent Introduction

Use this when adding a new bounded agent.

Required:

- PR title prefix: `AGENT:`
- Label: `agent-introduction`
- Required file: `agents/<agent_id>/manifest.yaml`
- Must follow:
  - `specs/agent_manifest_v0.1.md`
  - `specs/agent_lifecycle_v0.1.md`

PR body must answer:

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

Before opening a PR, run:

```bash
python agent-sdk/harness.py agents/<agent_id>/manifest.yaml
```

Forbidden agent kinds include:

- adjudicator
- accuser
- risk_scorer
- trust_scorer
- moderator

### Agent Amendment

Use this when changing an existing agent's scope.

Required:

- PR title prefix: `AGENT-AMENDMENT:`
- Label: `agent-amendment`
- Must follow: `specs/agent_lifecycle_v0.1.md`

PR body must include:

```text
Amended fields:
Prior scope:
New scope:
Reason amendment is necessary:
Membrane impact:
Tests updated:
```

Scope can only expand through manifest amendment.

Scope must never expand through code alone.

### Constitutional Amendment

Use this when changing specs, schemas, allowed verdicts, economic boundaries, RAP, or membrane tests.

Required:

- PR title prefix: `CONSTITUTION:`
- Label: `constitutional-amendment`
- Public rationale
- Full membrane test suite
- Comment period where appropriate

PR body must include:

```text
Constitutional surface changed:
Reason change is necessary:
Risk of semantic drift:
Migration plan:
Tests updated:
Rollback plan:
```

## What CI Enforces

CI rejects:

- unknown manifest fields
- forbidden agent kinds
- verdicts outside AllowedSurface
- semantic payload fields such as risk/trust/corruption scores
- dashboard interpretation drift
- economic features that buy authority
- invalid trusted issuer governance
- target and agent scope violations as tests are hardened

## Local Checks

Run:

```bash
pytest tests/membrane -v
pytest tests/spec_compliance -v
pytest tests/test_404_runtime_surface.py -v
pytest tests/test_404_dashboard_membrane.py -v
python agent-sdk/harness.py agents/<agent_id>/manifest.yaml
```

The SDK harness lets contributors test boundedness before CI.

It does not prove the agent is correct.

It proves the declared constitutional boundary is representable.

## Commercial Boundary

Customers may buy operational service.

Customers may not buy:

- attention
- speech
- interpretation
- verdicts
- target control
- unlock authority
- lifecycle power

See `specs/constitutional_replay_economy_v0.1.md`.

## One-Sentence Contract

```text
We sell operations. We cannot sell interpretation, attention, or authority. The tests that would fail if we tried are public.
```
