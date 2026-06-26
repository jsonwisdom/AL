# ALMS Replay Invocation Doctrine v0.1

## Purpose

An Invocation is the formal act of submitting a sealed Replay Envelope to the Replay Court.

The Invocation Contract defines what may be passed into replay. It does not define the verdict and it does not contain runtime execution facts.

## Constitutional Rule

The envelope must be immutable before invocation.

The invocation must be deterministic before execution.

Runtime facts belong in verdict and receipt artifacts, not in invocation input.

## Invocation Flow

```text
Extractor -> Fixture(s) -> Replay Envelope -> Invocation -> verify.sh / Docker Chamber -> Verdict -> Receipt
```

## Required Inputs

An invocation contains:

1. `invocation_id`
   - Deterministic identifier matching `INV_YYYYMMDD_HHMMSS_#####`.

2. `envelope`
   - Embedded Replay Envelope v0.1.
   - Must validate against `contracts/replay/v0.1/envelope.schema.json`.

3. `regime`
   - `canonicalizer: ALMS_REPLAY_V1`
   - declared witness target
   - `strict_mode: true`

4. `options`
   - `require_convergence: true`
   - bounded `timeout_seconds`

## Forbidden Inputs

The following fields are forbidden inside invocation input:

```text
invoked_at
timestamp_generated
generated_at
created_at
updated_at
uuid
random
rand
nonce
```

These values may appear later in receipt/verdict artifacts if they are explicitly marked as runtime observations.

They may not enter the deterministic invocation object.

## Witnesses

Allowed witnesses:

```text
PYTHON_3.8
PYTHON_3.9
PYTHON_3.10
PYTHON_3.11
PYTHON_3.12
PYTHON_3.13
DOCKER_3.12_SLIM
```

## CLI Contract Placeholder

Future CLI surface:

```bash
./verify.sh --invocation path/to/invocation.json
```

Until the CLI handler is implemented, CI validates the existence of the invocation schema and continues to run the claim extractor golden acceptance gate.

## Non-Authority Clause

A valid invocation proves only that a replay request was well-formed and deterministic.

It does not prove truth.

It does not prove legal authority.

It does not prove semantic correctness.

It only creates a stable request surface for replay adjudication.

## Dependency Order

The replay subtree remains ordered:

```text
Envelope -> Invocation Contract -> Verdict States -> Receipt -> CI Gate
```

No downstream artifact may redefine upstream fields.
