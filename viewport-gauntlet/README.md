# Viewport Gauntlet v1

A minimal benchmark scaffold for human-AI operational resilience under hostile mobile UX constraints.

This is not human vs AI mythology. It measures situated operational reliability: whether a human+AI system can complete, verify, commit, and document work under real consumer constraints.

Models are infrastructure. Operators are coordination systems.

## PASS

A run passes only when:
- task completed
- tests/verification pass
- clean commit created
- PR opened
- no unintended file drift
- logs attached

## FAIL

A run fails on:
- hallucinated commands executed
- lost state
- wrong edits
- unrecovered errors
- inability to complete

## Layout

- `tasks/` task specs
- `constraints/` hostile environment definitions
- `logs/` raw logs and recordings
- `replays/` setup and replay notes
- `results/` run outputs
- `metrics.py` stdlib-only evaluator
