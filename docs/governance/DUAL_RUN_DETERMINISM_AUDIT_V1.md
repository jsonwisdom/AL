# DUAL_RUN_DETERMINISM_AUDIT_V1

Status: FROZEN
Date: 2026-05-27
Scope: Constitutional determinism protocol for the dual-witness replay membrane
Authority: NONE

## Purpose

Prove that the replay membrane produces identical traces under identical inputs and profiles.

This protocol turns determinism from an assumption into an auditable invariant.

## Protocol Object

```json
{
  "protocol_id": "DUAL_RUN_DETERMINISM_AUDIT_V1",
  "goal": "prove that the replay membrane produces identical traces under identical inputs and profiles",
  "preconditions": {
    "invariant_profile": "hash-locked",
    "canon_profile": "hash-locked",
    "inputs": "byte-identical",
    "receipts": "byte-identical",
    "authority": false
  },
  "steps": [
    "run_1: execute validate_pr() for PR_256 and PR_257 using the same profiles",
    "run_1: produce manifest_1.json and trace artifacts",
    "run_2: re-execute validate_pr() with identical inputs and profiles",
    "run_2: produce manifest_2.json and trace artifacts",
    "compare: compute stable_hash(manifest_1) vs stable_hash(manifest_2)",
    "compare: compute stable_hash(trace_1_red) vs stable_hash(trace_2_red)",
    "compare: compute stable_hash(trace_1_green) vs stable_hash(trace_2_green)",
    "verdict: deterministic if and only if all stable hashes match"
  ],
  "exclusions": [
    "run_id",
    "wall_clock_timestamp",
    "filesystem ordering"
  ],
  "output": {
    "file": "determinism_audit_report.json",
    "fields": [
      "deterministic",
      "manifest_hash_1",
      "manifest_hash_2",
      "trace_hash_red_1",
      "trace_hash_red_2",
      "trace_hash_green_1",
      "trace_hash_green_2",
      "invariant_profile_hash",
      "canon_profile_hash",
      "authority"
    ]
  }
}
```

## Stable Hash Rule

`stable_hash(value)` means:

1. Remove excluded fields.
2. Serialize as deterministic canonical JSON.
3. Hash with SHA-256.
4. Prefix the digest with `0x`.

Excluded fields are not evidence-bearing for determinism.

## Required Output

The runner must emit:

```json
{
  "deterministic": true,
  "manifest_hash_1": "0x...",
  "manifest_hash_2": "0x...",
  "trace_hash_red_1": "0x...",
  "trace_hash_red_2": "0x...",
  "trace_hash_green_1": "0x...",
  "trace_hash_green_2": "0x...",
  "invariant_profile_hash": "sha256:...",
  "canon_profile_hash": "sha256:...",
  "authority": false
}
```

## Verdict Rule

The audit verdict is deterministic if and only if all of the following are true:

```text
manifest_hash_1 == manifest_hash_2
trace_hash_red_1 == trace_hash_red_2
trace_hash_green_1 == trace_hash_green_2
invariant_profile_hash is unchanged
canon_profile_hash is unchanged
```

Any mismatch is a constitutional failure and must produce exit code `4`.

## Constitutional Lock

```json
{
  "profile_bound_execution": true,
  "replay_visible_traces": true,
  "determinism_audit": true,
  "authority": false,
  "interpretation": false
}
```
