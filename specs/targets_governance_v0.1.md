# Targets Governance v0.1

Status: DESIGN_SPEC_ACTIVE
Operational status: SOFT_ENFORCEMENT_PENDING

## Purpose

Targets governance defines how AGW / ALMS agents choose what public records to observe.

This governs attention, not speech.

The machine must not only be bounded in what it can say; it must also be bounded in what it chooses to watch.

## Core Principle

```json
{
  "governance_surfaces_must_be_governed": true,
  "targets_yaml": "CONSTITUTIONAL_ATTENTION_SURFACE",
  "target_selection": "PROCEDURAL_NOT_POLITICAL"
}
```

## Scope

This specification applies to target lists such as:

- `agents/four04_crawler/targets.yaml`
- future agent target manifests
- target changelogs
- target metadata used by dashboards or workflows

## Allowed Target Criteria

Targets must satisfy all of the following:

1. Public-record or public-institutional source.
2. HTTPS URL.
3. No authentication required for baseline observation.
4. No user-uploaded evidence.
5. Within the declared agent manifest scope.
6. Added with procedural rationale.

## Forbidden Target Practices

Targets must not be added or removed because of:

- political disagreement
- perceived guilt
- perceived corruption
- perceived trustworthiness
- institutional reputation
- social-media controversy
- desire to pressure a person or institution
- too many `CRAWLER_BLOCKED` results
- attempt to create a narrative pattern

## Closed Tag Vocabulary v0.1

Targets may use only these tags:

```json
[
  "court_opinion",
  "court_docket",
  "agency_publication",
  "foia_page",
  "state_ag_record",
  "legislative_report",
  "budget_report",
  "public_manifest",
  "public_index"
]
```

Tags such as `controversial`, `suspicious`, `high_risk`, `watchlist`, or political labels are forbidden.

## Required Target Entry Shape

```yaml
- url: "https://example.gov/public-record.pdf"
  tags:
    - "agency_publication"
  rationale: "Public record endpoint used to verify accessibility and replayability."
  added_by_pr: "PR_NUMBER_OR_PENDING"
  operational_state: "ACTIVE"
```

## Agent Manifest Requirement

Each crawler agent should declare its scope in a machine-readable manifest, for example:

```yaml
agent_id: "four04_crawler"
allowed_domains:
  - ".gov"
  - ".mil"
allowed_url_schemes:
  - "https"
allowed_tags:
  - "court_opinion"
  - "court_docket"
  - "agency_publication"
  - "foia_page"
  - "state_ag_record"
  - "legislative_report"
  - "budget_report"
  - "public_manifest"
  - "public_index"
```

Scope should be enforced by tests before target changes become hard-fail CI.

## Target Change PR Requirements

A PR that changes target lists must include:

```text
Added:
- <url> — <procedural rationale>

Removed:
- <url> — <procedural rationale>
```

Recommended PR title prefix:

```text
TARGETS:
```

Recommended label:

```text
targets-change
```

## Deprecate Over Delete

When feasible, targets should be deprecated rather than silently deleted.

Preferred form:

```yaml
- url: "https://example.gov/old-record.pdf"
  tags:
    - "agency_publication"
  rationale: "Deprecated because endpoint retired; retained for audit history."
  added_by_pr: "123"
  deprecated_by_pr: "456"
  operational_state: "DEPRECATED"
```

Deletion is allowed only when:

- duplicate target exists,
- URL was malformed,
- target is outside declared agent scope,
- legal or safety requirement mandates removal,
- removal rationale is recorded.

## Changelog Requirement

A rendered governance changelog should be maintained once multiple target-changing PRs exist:

```text
agents/four04_crawler/targets_changelog.md
```

Git remains the source of truth, but a rendered changelog improves observer auditability.

## Soft CI Checks v0.1

Initial target governance checks should annotate or fail in stages:

1. PR touches `**/targets.yaml` -> requires `targets-change` label.
2. PR description must include `Added:` or `Removed:`.
3. YAML validator checks each target has HTTPS URL.
4. YAML validator checks each target has allowed tags only.
5. YAML validator checks each target has procedural rationale.

After the checks are proven stable, promote them to hard-fail CI.

## Non-Claims

Targets governance does not assert:

- a watched institution is suspicious,
- a watched source is defective,
- a watched URL is more important than another,
- target inclusion is a legal or moral claim,
- target removal is censorship.

A target means only:

```text
This endpoint is within agent scope and is eligible for procedural replay observation.
```

## State

```json
{
  "targets_governance": "DESIGN_SPEC_ACTIVE",
  "target_selection": "PROCEDURAL_NOT_POLITICAL",
  "runtime_targets": "GOVERNED_ATTENTION_SURFACE",
  "hard_ci": "PENDING",
  "no_ghost_anchor": true
}
```
