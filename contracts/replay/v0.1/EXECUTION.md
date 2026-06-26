# Replay Execution Contract v0.1

## Purpose

Signature verification proves attribution over a replay envelope.

Execution proves whether the replay output reproduces under the declared invocation.

Without execution, the Replay Court is only a notary. With execution, it becomes an adjudication surface.

## Dependency Order

```text
Extractor -> Fixture -> Envelope -> Signature Check -> Invocation -> Execution -> Verdict -> Receipt
```

Execution may not redefine upstream objects.

Execution consumes a valid invocation and emits a verdict.

## CLI Surface

The only legal execution entrypoint is:

```bash
./verify.sh --invocation <invocation.json>
```

No other flags, pipes, shell fragments, or ambient commands are admissible under v0.1.

## Allowed Command

Execution is restricted to one binary:

```text
/usr/local/alms/bin/replay-bin
```

The handler must invoke it directly. Shell expansion is forbidden.

Target model:

```text
execve("/usr/local/alms/bin/replay-bin", ["replay-bin"], sealed_env)
```

Invocation JSON is provided on stdin.

No command-line claim content is allowed.

## Pre-Execution Gates

Before execution, the handler must:

1. Parse invocation JSON.
2. Validate invocation schema.
3. Recompute `invocation_id` from canonical JSON without `invocation_id`.
4. Verify referenced envelope bytes match `envelope_sha256`.
5. Verify the envelope signature.
6. Refuse if any schema, hash, signature, or registry check fails.

## Deterministic Environment

The execution environment must be minimal and deterministic.

Allowed environment variables:

```text
PATH=/usr/local/alms/bin:/usr/bin
LANG=C.UTF-8
LC_ALL=C.UTF-8
PYTHONHASHSEED=0
ALMS_INVOCATION_ID=<invocation_id>
```

Forbidden environment classes:

```text
HOME
*_PROXY
HTTP_PROXY
HTTPS_PROXY
ALL_PROXY
NO_PROXY
LD_*
PYTHONPATH
VIRTUAL_ENV
CONDA_*
NPM_*
NODE_*
```

Any unapproved ambient variable must be stripped before execution.

## Network

Network must be disabled for v0.1 execution.

Preferred mechanisms:

```text
unshare -n
seccomp socket deny
container network=none
```

If network isolation cannot be enforced, execution must return:

```text
REPLAY_QUARANTINED
```

## Filesystem

Execution should use:

```text
read-only repository checkout
read-write tempdir: /tmp/alms/<invocation_id>
```

The tempdir must be deleted after execution.

## Clock

No runtime clock value may affect replay output.

If future fixtures require time, the declared time must come from invocation input and be frozen before execution.

If clock isolation cannot be enforced for a time-dependent replay, execution must return:

```text
REPLAY_QUARANTINED
```

## Output Contract

`replay-bin` must write replay result bytes to stdout only.

Rules:

1. stdout is the only admissible output channel.
2. stderr must be empty.
3. non-zero exit code means quarantine.
4. trailing single newline is stripped before hashing.
5. if output is valid UTF-8, normalize to NFC before hashing.
6. if output is not valid UTF-8, hash raw bytes after newline trim.

## Expected Output

Invocation v0.1 must declare an expected output hash before execution can converge.

Future schema field:

```json
{
  "expected_outputs": {
    "stdout_sha256": "sha256:<64 hex>"
  }
}
```

Until that field exists, execution handler must refuse or quarantine rather than invent expectations.

## Verdict Mapping

| Condition | Verdict |
|---|---|
| pre-execution schema/hash/signature failure | `REPLAY_REFUSED` |
| `replay-bin` missing | `REPLAY_QUARANTINED` |
| network/sandbox cannot be enforced | `REPLAY_QUARANTINED` |
| non-zero exit code | `REPLAY_QUARANTINED` |
| stderr not empty | `REPLAY_QUARANTINED` |
| actual stdout hash equals expected stdout hash | `REPLAY_CONVERGED` |
| actual stdout hash differs from expected stdout hash | `REPLAY_DIVERGED` |

## Minimal Verdict Fields

Execution verdicts must include:

```json
{
  "verdict_version": "replay-verdict-v0.1",
  "invocation_id": "sha256:...",
  "envelope_sha256": "sha256:...",
  "witness": "PYTHON_3.12|DOCKER_3.12_SLIM|...",
  "state": "REPLAY_CONVERGED|REPLAY_DIVERGED|REPLAY_REFUSED|REPLAY_QUARANTINED",
  "actual_stdout_sha256": "sha256:...|null",
  "expected_stdout_sha256": "sha256:...|null",
  "reason": "..."
}
```

## Non-Authority Clause

A converged execution proves only that a signed, deterministic invocation reproduced the expected bytes under the declared witness.

It does not prove truth.

It does not prove legal authority.

It does not prove semantic completeness.

It only proves replay convergence for the sealed execution surface.
