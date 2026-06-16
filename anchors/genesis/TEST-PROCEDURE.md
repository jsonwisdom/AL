# Genesis Witness Test Procedure

This procedure verifies that the Genesis witness root can be reproduced by independent observers from clean environments.

The test is not a convenience check.
It is the first live constitutional test of the witness procedure itself.

## Purpose

```text
Prove that independent observers converge on the same witness_root.
```

## Preconditions

```text
- scripts/generate_witness_anchor.py exists
- anchors/genesis/anchor-manifest.json exists
- repo is publicly fetchable
- protected core files are present
- telemetry heads are present
```

## Environment A

```bash
git clone https://github.com/jsonwisdom/AL.git AL-witness-A
cd AL-witness-A
python3 scripts/generate_witness_anchor.py
cat anchors/genesis/anchor-manifest.json
```

Record:

```text
environment_A_os:
environment_A_python:
witness_root_A:
repo_commit_A:
```

## Environment B

Use a separate clean clone, ideally a different OS, container, or runner.

```bash
git clone https://github.com/jsonwisdom/AL.git AL-witness-B
cd AL-witness-B
python3 scripts/generate_witness_anchor.py
cat anchors/genesis/anchor-manifest.json
```

Record:

```text
environment_B_os:
environment_B_python:
witness_root_B:
repo_commit_B:
```

## Required Convergence

```text
witness_root_A == witness_root_B == committed witness_root
repo_commit_A == repo_commit_B == committed repo_commit
```

## Pass Condition

```text
GENESIS_WITNESS_REPLAY_PASS
```

Requires:

```text
- matching witness roots
- matching repo commits
- no missing protected core files
- no missing telemetry heads
- no canonicalization divergence
```

## Failure Conditions

```text
GENESIS_WITNESS_REPLAY_FAIL
```

Use only when contradictory evidence is observed:

```text
- witness roots mismatch
- file hashes mismatch
- repo commits mismatch
- manifest cannot be regenerated
- canonicalization differs across environments
```

## Unobserved Conditions

```text
GENESIS_WITNESS_REPLAY_UNOBSERVED
```

Use when required evidence is missing or inaccessible:

```text
- one environment cannot be run
- repo cannot be fetched
- artifact unavailable
- output not captured
```

## Report Format

```text
ROUTE USED: B_PUBLIC_ARTIFACTS / A_LOCAL_EXECUTION
ENVIRONMENT_A: OBSERVED / UNOBSERVED
ENVIRONMENT_B: OBSERVED / UNOBSERVED
WITNESS_ROOT_A:
WITNESS_ROOT_B:
COMMITTED_WITNESS_ROOT:
ROOTS_MATCH: yes / no / unobserved
FINAL_VERDICT:
NEXT_ACTION:
```

## Guardrails

```text
The witness root does not create truth.
The witness root does not authorize payment.
The witness root does not erase contradiction.
The witness root does not replace replay.
```

## Invariant

```text
A witness root is only useful if independent observers can reproduce it.
```
