# TARGETS Change Request

This PR proposes a governed attention change.

Contributors may propose changes. The membrane decides whether the change is representable.

## Purpose

This template is the human-readable doorway for `specs/targets_governance_v0.1.md`.

CI will enforce the machine-readable boundary using:

- `schemas/targets_v1.schema.json`
- `schemas/target_tags_v1.json`
- `tests/membrane/test_targets_governance.py`

## Required PR Metadata

- Title prefix: `TARGETS:`
- Label: `targets-change`

## Added

List each added target and procedural rationale.

```text
- URL:
  Tag:
  Public-record basis:
  Procedural rationale:
```

## Removed / Deprecated

List each removed or deprecated target.

Deletion should be avoided. Prefer tombstones using `deprecated: true`.

```text
- URL:
  Action: DEPRECATED | REMOVED
  Reason:
  deprecated_by_pr: #PENDING
```

## Target Entry Shape

Every new target must match this shape:

```yaml
- url: "https://example.gov/public-record.pdf"
  tags: ["agency_publication"]
  rationale: "Public record endpoint for procedural replay observation."
  added_by_pr: "#PENDING"
  operational_state: "ACTIVE"
```

## Representability Checklist

- [ ] Every URL starts with `https://`
- [ ] Every target uses only tags from `schemas/target_tags_v1.json`
- [ ] Every target has `added_by_pr`
- [ ] Every target has procedural `rationale`
- [ ] No unknown fields were added
- [ ] No interpretive metadata was added
- [ ] No target was removed without a deprecation/tombstone rationale

## Forbidden Fields

This PR must not introduce:

- `priority`
- `risk_level`
- `risk_score`
- `sensitive`
- `editorial_note`
- `interpretation`
- `concern_level`
- `trust_level`
- `watch_priority`
- `threat_level`

## Maintainer Review Scope

Maintainers review only:

- Is the URL a public-record endpoint?
- Is the target within declared agent scope?
- Is the procedural rationale accurate enough?

Maintainers do not manually enforce schema shape. CI does that.

## Membrane Decision Log

CI result:

```json
{
  "targets_schema": "PENDING",
  "closed_tag_vocabulary": "PENDING",
  "forbidden_fields": "PENDING",
  "unknown_fields": "PENDING",
  "attention_membrane": "PENDING"
}
```

## Non-Claims

Adding a target does not imply suspicion, wrongdoing, priority, risk, trust, or institutional judgment.

A target means only:

```text
This endpoint is within agent scope and eligible for procedural replay observation.
```
