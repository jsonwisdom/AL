# Community Adversarial Fixture

## Required Files

Each fixture contribution MUST include two files in:

```text
docs/epoch03/adversarial/community/<author-id>/
```

1. `<fixture-id>.json`
   - finite, deterministic, replayable transcript object
   - MUST NOT introduce new doctrine or FSM surfaces
   - MUST expect refusal under the public validator

2. `<fixture-id>.manifest.json`
   - finite manifest object binding the fixture to a hostile class and doctrine references

## Manifest Shape

```json
{
  "id": "author-fixture-id",
  "class": "illegal_transition",
  "expected_verdict": "REJECT",
  "doctrine_reference": ["D-1"],
  "author": "author-id",
  "description": "One-sentence hostile condition being probed."
}
```

## Rules

- All fixtures MUST be hostile.
- All fixtures MUST expect `REJECT` or `TAINTED`.
- No fixture may expect `ACCEPT`.
- All fixtures MUST pass the same harness used by core fixtures.
- PRs are only mergeable if the validator refuses the fixture.
- A fixture that silently receives `ACCEPT` identifies a continuity surface.

## Constitutional Standard

A community fixture is not commentary.
It is an evidentiary object asking one question:

```text
Under this hostile condition, does the system mechanically refuse to drift?
```

The answer must be a bit, not a narrative.
