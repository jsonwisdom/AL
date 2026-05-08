# Agent Manifest v0.1

Status: DESIGN_SPEC_ACTIVE
Operational status: ACTIVE_FOR_REVIEW
Scope: `agents/*/manifest.yaml` and agent runtime behavior

## Purpose

Define what an agent is allowed to observe, emit, and touch.

This turns agents into constitutional actors with explicit, replayable, CI-enforced scope.

This spec governs agent legitimacy, not implementation details.

## Manifest Object

Each agent MUST ship:

```text
agents/<name>/manifest.yaml
```

The manifest declares:

- agent identity
- agent kind
- constitutional basis
- allowed targets
- allowed verdicts
- allowed tags
- forbidden fields
- runtime limits
- output surfaces

## Agent Kinds

Allowed kinds:

- `observer`: crawls public records and emits bounded procedural states.
- `verifier`: compares hashes, manifests, timestamps, and replay surfaces.
- `detector`: identifies procedural gaps without accusation semantics.
- `tombstone`: watches for removal/tombstone/redirect patterns under a bounded verdict surface.

Forbidden kinds:

- `adjudicator`
- `accuser`
- `risk_scorer`
- `trust_scorer`
- `moderator`

No agent may adjudicate legitimacy, guilt, intent, corruption, morality, or institutional worth.

## Required Manifest Fields

```yaml
agent_id: "four04_crawler"
kind: "observer"
constitutional_basis:
  - "specs/proof_blob_v0.1.md"
  - "specs/targets_governance_v0.1.md"
  - "circuits/404_v1/README.md"
targets_file: "agents/four04_crawler/targets.yaml"
allowed_domains:
  - ".gov"
allowed_url_schemes:
  - "https"
allowed_tags:
  - "court_opinion"
  - "agency_publication"
allowed_verdicts:
  - "FOUND"
  - "NOT_FOUND"
  - "VERSION_DRIFT"
  - "CRAWLER_BLOCKED"
forbidden_fields:
  - "RISK_SCORE"
  - "TRUST_SCORE"
  - "CORRUPTION_SCORE"
runtime_limits:
  max_requests_per_run: 100
  timeout_seconds: 20
  network_required: true
output:
  receipts_dir: "receipts"
  circuit_id: "404_v1"
operational_state: "ACTIVE_FOR_REVIEW"
```

## Constitutional Requirements

For a manifest to be valid:

1. `constitutional_basis` must point to existing specs that bound its speech and attention surfaces.
2. `allowed_verdicts` must be a subset of the relevant AllowedSurface membrane.
3. `forbidden_fields` must include the semantic payload guard list required by the agent's public surface.
4. `targets_file` must exist and be governed by `targets_governance_v0.1.md`.
5. `runtime_limits` must declare hard limits. No agent runs unbounded.
6. `allowed_tags` must use the closed vocabulary from `targets_governance_v0.1.md`.

## Introducing New Agents

To add `agents/<name>/`:

1. Create `manifest.yaml` per this spec.
2. PR should be tagged `agent-introduction`.
3. PR description must answer:
   - What public records does it watch?
   - What constitutional verdicts does it emit?
   - Why cannot an existing agent do this?
4. CI validates manifest schema.
5. Reviewer confirms no semantic drift vs `proof_blob_v0.1.md`.

## Runtime Enforcement

The runtime loader should:

1. Parse manifest before execution.
2. Reject any receipt verdict not in `allowed_verdicts`.
3. Reject any receipt field in `forbidden_fields`.
4. Kill the agent if `max_requests_per_run` is exceeded.
5. Fail if the agent touches a domain outside `allowed_domains`.

## Auditability

```text
git log agents/*/manifest.yaml
```

is the registry of constitutional actors.

Changing an agent's scope is a constitutional amendment with a public diff.

## Forbidden Practices

- Agent emits fields not allowed by its manifest.
- Agent expands target scope via code without manifest update.
- Observer agent writes to RAP or decrypts anything.
- Manifest uses interpretive tags such as `controversial`, `suspicious`, `high_risk`, or `watchlist`.
- Agent uses `kind: adjudicator`.

## Non-Claims

An agent manifest does not prove an agent is trustworthy, correct, or authoritative.

It proves only that the declared runtime boundary is explicit and testable.

## State

```json
{
  "agent_manifest_v0_1": "DESIGN_SPEC_ACTIVE",
  "agents": "CONSTITUTIONAL_ACTORS",
  "runtime_scope": "DECLARED_AND_TESTABLE",
  "hard_ci": "PENDING",
  "no_ghost_anchor": true
}
```
