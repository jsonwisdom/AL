# EPOCH 02 — Replay CLI Spec v1

## Purpose

Define the read-only, non-authoritative, deterministic command-line interface for interacting with the Epoch 02 replay engine.

The CLI:

- does not mutate state
- does not infer missing fields
- does not sign
- does not anchor
- does not override replay
- does not interpret results

The CLI is a witness, not an authority.

Replay is the authority.

---

## 1. Constitutional Basis

Explicit invariant:

```text
CLI != AUTHORITY
CLI = READ_ONLY_REPLAY_WITNESS
```

The CLI answers one question:

```text
Does this replay under the declared epoch rules?
```

It reports the answer.
It does not decide the answer.

---

## 2. Command Surface

All commands follow:

```text
epoch2 <command> [--flags]
```

All commands emit JSON only to stdout.
Exit codes are the canonical authority.

---

### 2.1 `replay-attestation`

```text
epoch2 replay-attestation --payload <file> --signature <file> --epoch <file>
```

#### Purpose

Verify that a signed payload replays deterministically under the declared epoch rules.

#### Inputs

- `--payload`: L0 payload file, raw bytes
- `--signature`: detached signature file
- `--epoch`: epoch definition file

#### Processing

1. Validate signature.
2. Validate payload schema.
3. Execute replay kernel.
4. Compute trace hash.
5. Compare to expected trace hash.

#### Output

JSON attestation result.

#### Exit Codes

- `0` — valid
- `1` — replay invalid
- `2` — bad input
- `4` — signature invalid
- `8` — epoch boundary violation
- `9` — internal error

---

### 2.2 `replay-anchor`

```text
epoch2 replay-anchor --anchor <file> --attestation <file> --epoch <file>
```

#### Purpose

Verify that an anchor commitment matches its attestation and is valid under epoch rules.

#### Inputs

- `--anchor`: anchor file
- `--attestation`: attestation file
- `--epoch`: epoch definition file

#### Processing

1. Verify attestation validity.
2. Verify anchor commitment.
3. Verify epoch boundaries.

#### Exit Codes

- `0` — valid
- `1` — invalid
- `2` — bad input
- `7` — anchor invalid
- `8` — epoch boundary violation
- `9` — internal error

---

### 2.3 `replay-epoch-closure`

```text
epoch2 replay-epoch-closure --closure <file> --epoch <file>
```

#### Purpose

Verify that an epoch closure record is complete and valid.

#### Inputs

- `--closure`: epoch closure file
- `--epoch`: epoch definition file

#### Processing

1. Validate closure fields.
2. Validate all anchors.
3. Validate closure timestamp.
4. Validate closure signature.

#### Exit Codes

- `0` — valid
- `1` — invalid
- `2` — bad input
- `6` — finality false
- `8` — epoch boundary violation
- `9` — internal error

---

### 2.4 `trace-attestation`

```text
epoch2 trace-attestation --payload <file> --signature <file> --epoch <file>
```

#### Purpose

Produce a deterministic constitutional trace of replay execution.

#### Processing

Same as `replay-attestation`, but emits the full trace.

#### Exit Codes

- `0` — trace emitted
- `1` — replay invalid
- `2` — bad input
- `4` — signature invalid
- `8` — epoch boundary violation
- `9` — internal error

---

### 2.5 `explain-error`

```text
epoch2 explain-error --code <ERROR_CODE>
```

#### Purpose

Return the canonical error definition for a given exit code.

#### Output

JSON error description.

#### Exit Codes

- `0` — explained
- `2` — unknown code

---

## 3. Output Format

### 3.1 Success

```json
{
  "command": "replay-attestation",
  "status": "VALID",
  "exit_code": 0,
  "payload_hash": "sha256:...",
  "trace_hash": "sha256:...",
  "epoch_id": "epoch_02",
  "kernel_hash": "sha256:...",
  "timestamp": "2026-05-08T00:00:00Z"
}
```

### 3.2 Failure

```json
{
  "command": "replay-attestation",
  "status": "INVALID",
  "exit_code": 1,
  "error_code": "TRACE_DIVERGENCE",
  "error_class": "REPLAY_FAILURE",
  "payload_hash": "sha256:...",
  "expected_trace_hash": "sha256:...",
  "observed_trace_hash": "sha256:...",
  "timestamp": "2026-05-08T00:00:00Z"
}
```

### 3.3 Error

```json
{
  "command": "replay-attestation",
  "status": "ERROR",
  "exit_code": 2,
  "error_code": "MALFORMED_PAYLOAD",
  "error_class": "INPUT_FAILURE",
  "detail": "Payload does not parse as valid epoch_02 input",
  "timestamp": "2026-05-08T00:00:00Z"
}
```

---

## 4. Exit Code Contract

| Code | Name | Class | Meaning |
|---:|---|---|---|
| 0 | PASS | — | Replay valid |
| 1 | FAIL | REPLAY_FAILURE | Replay invalid |
| 2 | INVALID_INPUT | INPUT_FAILURE | Malformed or schema-invalid input |
| 3 | NON_CANONICAL | INPUT_FAILURE | Input not canonical |
| 4 | SIGNATURE_INVALID | INPUT_FAILURE | Signature does not verify |
| 5 | UNAUTHORIZED_OPERATOR | ENV_FAILURE | Signer not authorized |
| 6 | FINALITY_FALSE | REPLAY_FAILURE | Closure not final |
| 7 | ANCHOR_INVALID | REPLAY_FAILURE | Anchor mismatch |
| 8 | EPOCH_BOUNDARY_VIOLATION | INPUT_FAILURE | Outside declared epoch |
| 9 | INTERNAL_ERROR | ENV_FAILURE | Unexpected non-replay error |

Exit codes are the only authority.
The CLI must not soften or reinterpret them.

---

## 5. Constitutional Prohibitions

The CLI MUST NOT:

1. mutate evidence
2. repair payloads
3. sign anything
4. anchor anything
5. override replay
6. infer missing fields
7. emit prose in the replay path

The CLI is a pure observer.

---

## 6. Invariants

```text
CLI != AUTHORITY
CLI = WITNESS
REPLAY = AUTHORITY
EXIT_CODES = CANONICAL
JSON = ONLY_OUTPUT
NO_REPAIR
NO_OVERRIDE
NO_INTERPRETATION
```
