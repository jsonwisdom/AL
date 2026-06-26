# Replay Command Grammar v0.2

## Purpose

v0.2 adds exactly one new replay dimension:

```text
replay_command
```

Everything else remains frozen.

No shell.
No pipes.
No globbing.
No ambient environment passthrough.
No dynamic dispatch.

## Allowlist

Only these commands are admissible under v0.2:

```text
echo_golden
check_policy
```

Any other command MUST produce:

```json
{
  "state": "REPLAY_QUARANTINED",
  "reason": "COMMAND_NOT_ALLOWED"
}
```

## Execution Model

Allowed binary remains:

```text
/usr/local/alms/bin/replay-bin
```

The handler invokes it directly as:

```text
/usr/local/alms/bin/replay-bin <replay_command> <replay_args...>
```

Invocation JSON is passed on stdin.

## Arguments

`replay_args` is optional.

Rules:

1. It must be an array.
2. Every argument must be a string.
3. Arguments are passed verbatim.
4. No shell expansion is permitted.
5. No globbing is permitted.
6. No environment interpolation is permitted.

## Output Contract

All commands must:

1. Read invocation JSON from stdin.
2. Write canonical replay bytes to stdout only.
3. Write nothing to stderr.
4. Exit 0 on success.

Non-zero exit or stderr output means:

```text
REPLAY_QUARANTINED
```

## Canonical Output Hash

Output canonicalization remains:

1. Strip one trailing newline if present.
2. If valid UTF-8, normalize NFC.
3. If invalid UTF-8, hash raw bytes after newline trimming.
4. Compute SHA-256.
5. Compare against `expected_outputs.stdout_sha256`.

## Non-Authority Clause

Allowed command execution proves only that the declared command reproduced the declared bytes under the sealed invocation.

It does not prove truth.
It does not prove legal authority.
It does not prove semantic completeness.
