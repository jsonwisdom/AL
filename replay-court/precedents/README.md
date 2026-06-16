# Replay Court Precedents

Replay Court precedents are reference fixtures for constitutional enforcement behavior.

They preserve observed outcomes so future validator changes can be tested against known cases.

## Purpose

```text
Turn live governance events into regression fixtures.
```

## Precedent Pair Pattern

```text
FAIL precedent:
  protected-core drift rejected

PASS precedent:
  lawful amendment admitted
```

Both sides must use:

```text
- same protected-core surface
- same validator family
- deterministic receipt shape
- replayable evidence
```

## Current Planned Fixtures

```text
233-FAIL.json
  PR #233: protected-core edit without amendment metadata or contradiction reference

234-PASS.json
  future paired PR: same surface with lawful amendment metadata and valid contradiction reference
```

## Guardrail

Do not edit old precedent fixtures to make history clean.
Add a new fixture when doctrine, validator behavior, or evidence changes.

## Invariant

```text
A precedent is useful only if future validators can replay it and reach the same verdict.
```
