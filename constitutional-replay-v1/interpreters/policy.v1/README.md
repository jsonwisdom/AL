# policy.v1 Interpreter Contract

This directory defines the frozen `policy.v1` surface for `constitutional-replay-v1`.

## Kernel Rule

```text
Same policy + same input + same interpreter = same verdict forever.
```

## Authority

The schema and golden vectors define the expected behavior.

The interpreter must conform to them.

The vectors do not bend to implementation convenience.

## Required Policy Fields

A `policy.v1` object must declare:

- `version`
- `policy_id`
- `required_inputs`
- `allowed_actions`
- `blocked_actions`
- `limits`
- `refusal_codes`

## Amount Discipline

Amounts must be decimal strings.

Floats are forbidden.

Unsafe integers are forbidden.

## Refusal Discipline

Refusals must use the fixed enum from `schema.json`.

Free-text refusal reasons are forbidden.

## v0.1 Decision Order

A conforming interpreter should evaluate in this order:

1. Missing required input → `UNKNOWN_REFUSAL`.
2. Action not explicitly allowed → `ACTION_NOT_ALLOWED`.
3. Action explicitly blocked → `ACTION_NOT_ALLOWED`.
4. Transfer amount exceeds `limits.transfer_usdc_day` → `SPEND_LIMIT_EXCEEDED`.
5. Otherwise → `SUCCESS`.

## v0.1 Golden Vectors

The interpreter must satisfy:

- `approve-transfer-001` → `SUCCESS`
- `refuse-limit-001` → `SPEND_LIMIT_EXCEEDED`
- `refuse-action-001` → `ACTION_NOT_ALLOWED`
- `refuse-missing-input-001` → `UNKNOWN_REFUSAL`

## Failure Behavior

Allowed failure states:

- `POLICY_SCHEMA_VIOLATION`
- `UNHANDLED_REFUSAL`
- `UNKNOWN_ACTION`
- `INTERPRETER_HASH_MISMATCH`

Forbidden behavior:

- free-text refusal output
- probabilistic verdicts
- network lookups
- live clock reads
- fallback to latest policy version

## Final Rule

The interpreter is not allowed to be clever.

It must be boring, deterministic, and replayable.
