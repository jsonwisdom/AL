# ALMS-v1-EPOCH-CHECK-CONTRACT.md

```yaml
status: CANONICAL_CANDIDATE
surface_role: EPOCH_CHECK_RUNTIME_CONTRACT
epoch_id: ALMS_v1
global_state: NO_DRIFT
```

## 1. Purpose

This surface defines the constitutional runtime contract for `alms-epoch-check`:

- exact CLI invocation,
- exact PASS / REFUSE payloads,
- deterministic exit codes,
- canonical JSON emission format,
- hash binding for emitted objects,
- stdout / stderr law,
- and the machine-readable replay contract.

REFUSE is a lawful denial of execution, not a runtime failure.

## 2. CLI Invocation

### 2.1 Command Form

The tool MUST be invocable as:

```bash
alms-epoch-check \
  --epoch-id <EPOCH_ID> \
  --claim-or-receipt <PATH> \
  --provenance <PATH>
```

### 2.2 Required Arguments

- `--epoch-id`: REQUIRED. String, for example `ALMS_v1`.
- `--claim-or-receipt`: REQUIRED. Filesystem path to the claim or receipt under evaluation.
- `--provenance`: REQUIRED. Filesystem path to the provenance file.

No positional arguments are allowed.

No environment variables may alter semantics.

Missing any required argument MUST result in an applicable REFUSE payload, not a generic runtime error.

## 3. Exit Codes

The process exit code space is:

```text
0      PASS
10     REFUSE
>100   RUNTIME_FAILURE
```

### 3.1 Constitutional Constraint

Exit codes `0` and `10` are lawful outcomes and MUST always be accompanied by a valid JSON payload on stdout.

Exit codes greater than `100` indicate the tool failed to apply the constitution at all. They MUST NOT be used to encode refusal semantics.

## 4. JSON Emission Format

All constitutional outcomes MUST be emitted as a single JSON object on stdout.

No additional text is permitted on stdout.

### 4.1 Common Envelope

Both PASS and REFUSE payloads share this envelope:

```json
{
  "tool": "alms-epoch-check",
  "epoch_id": "ALMS_v1",
  "status": "PASS | REFUSE",
  "claim_or_receipt_path": "<string>",
  "provenance_path": "<string>",
  "refusal": null,
  "payload_hash": "<sha256-hex>",
  "emitted_at": "<RFC3339 timestamp>",
  "tool_version": "<string>"
}
```

For REFUSE, `refusal` MUST be a non-null object:

```json
{
  "code": "<REFUSE-...>",
  "name": "<UPPER_SNAKE_CASE>",
  "message": "<machine-readable string>"
}
```

### 4.2 PASS Payload

On PASS:

- `status` MUST be `PASS`.
- `refusal` MUST be `null`.
- exit code MUST be `0`.

### 4.3 REFUSE Payload

On REFUSE:

- `status` MUST be `REFUSE`.
- `refusal` MUST be non-null.
- `refusal.code` MUST be one of the seated v1 refusal codes.
- exit code MUST be `10`.

## 5. Hash Binding

### 5.1 payload_hash

`payload_hash` MUST be the SHA-256 hash of the canonical JSON serialization of the payload with the `payload_hash` field set to the empty string `""` during computation.

Canonical JSON serialization MUST use:

- UTF-8 encoding,
- sorted keys,
- no trailing commas,
- minimal whitespace.

This makes each PASS / REFUSE object hash-bound, replayable, and constitutionally enumerable.

### 5.2 Replay Requirement

Any later verifier MUST be able to:

1. Parse the emitted JSON.
2. Recompute `payload_hash` under the canonical rules.
3. Confirm equality with the embedded `payload_hash`.

If this fails, the emission is inadmissible as a constitutional act.

## 6. stdout / stderr Law

stdout:

- MUST contain exactly one JSON object: PASS or REFUSE payload.
- MUST NOT contain human-oriented commentary.

stderr:

- MAY contain human-readable diagnostics, logs, or stack traces.
- MUST NOT be used to encode constitutional semantics.
- MUST NOT be required for machine replay.

Any consumer that ignores stderr and reads only stdout MUST still obtain the full constitutional story.

## 7. Machine-Readable Replay Contract

Given:

- `epoch_id`,
- the original claim_or_receipt file,
- the original provenance file,
- and a stored PASS / REFUSE JSON payload,

a replay verifier MUST be able to:

1. Re-run `alms-epoch-check` with the same inputs.
2. Obtain a new PASS / REFUSE payload.
3. Confirm:
   - status matches,
   - refusal.code matches when present,
   - payload_hash differs only when `emitted_at` or `tool_version` differ.

If a successor epoch changes law, it MUST do so via a new `epoch_id` and a new contract. ALMS_v1 emissions remain replayable under v1.

## 8. Constitutional State

```yaml
epoch_id: ALMS_v1
epoch_check_contract: CLOSED
output_space:
  PASS: 0
  REFUSE: 10
runtime_failures:
  exit_code: ">100"
global_state: NO_DRIFT
```

End of ALMS-v1-EPOCH-CHECK-CONTRACT.md
