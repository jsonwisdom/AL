# ALMS v0 Execution

## Purpose

ALMS Execution defines deterministic replay jurisdiction for verifier runtimes, model artifacts, decoding graphs, and execution environments.

Once execution keys are real, infrastructure is evidence.

## Execution Environment Manifest

`exec_env_hash` commits to an execution environment manifest.

Canonicalization: JCS.

```text
exec_env_hash = SHA256(JCS(exec_env_manifest))
```

Hex encoding is lowercase.

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://alms.dev/schema/v0/exec-env-manifest.json",
  "title": "ALMS v0 Execution Environment Manifest",
  "type": "object",
  "required": [
    "alms_version",
    "exec_env_id",
    "verifier_binary_hash",
    "runtime_hash",
    "cpu",
    "os",
    "math",
    "rng",
    "tee"
  ],
  "properties": {
    "alms_version": { "type": "string", "const": "alms-v0" },
    "exec_env_id": { "type": "string" },
    "verifier_binary_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "runtime_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "cpu": {
      "type": "object",
      "required": ["arch", "vendor", "features"],
      "properties": {
        "arch": { "type": "string" },
        "vendor": { "type": "string" },
        "features": { "type": "array", "items": { "type": "string" } }
      },
      "additionalProperties": false
    },
    "os": {
      "type": "object",
      "required": ["name", "version", "abi"],
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "string" },
        "abi": { "type": "string" }
      },
      "additionalProperties": false
    },
    "math": {
      "type": "object",
      "required": ["blas", "fma", "fp_contract"],
      "properties": {
        "blas": { "type": "string" },
        "fma": { "type": "boolean" },
        "fp_contract": { "type": "string", "enum": ["off", "on", "fast"] }
      },
      "additionalProperties": false
    },
    "rng": {
      "type": "object",
      "required": ["name", "version"],
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "string" }
      },
      "additionalProperties": false
    },
    "tee": {
      "type": "object",
      "required": ["used"],
      "properties": {
        "used": { "type": "boolean" },
        "attestation_format": { "type": "string" },
        "quote_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

## v0 Determinism Constraints

ALMS v0 requires:

```text
math.fp_contract = off
```

If `math.fp_contract` is `on` or `fast`, reject with code `4`, reason `exec_env_fp_contract_unsupported`.

TEE use is optional in v0. If `tee.used = true`, the verifier MUST validate the declared `attestation_format` and `quote_hash` through the registry or reject with code `4`, reason `tee_attestation_unverified`.

## Execution Key

The execution key defines what deterministic replay means:

```text
exec_key = (weight_hash, runtime_hash, decoding_graph_hash, exec_env_hash)
```

All four components are required.

A receipt that omits any component is rejected with code `4`, reason `exec_key_incomplete`.

## Cache Key

The cache key is SHA256 over JCS of this object:

```json
{
  "weight_hash": "<sha256>",
  "runtime_hash": "<sha256>",
  "decoding_graph_hash": "<sha256>",
  "exec_env_hash": "<sha256>"
}
```

```text
cache_key = SHA256(JCS(cache_key_object))
```

This forbids silent fallback to latest model, latest runtime, or latest decoding graph.

## Cache State Machine

State per `cache_key`:

```text
VALID
STALE
TAINTED
ABSENT
```

### Must-invalidate triggers

Hash drift:

- Any component of `exec_key` changes.
- Entries with the old `cache_key` become `STALE`.

TTL expiry:

- Registry `replay_ttl_seconds` exceeded.
- Entry becomes `STALE`.

Revocation:

- Any key, constitution, model, runtime, decoding graph, schema, or root in the dependency chain is revoked.
- Dependent cache entries become `STALE`.

Quorum change:

- Trust root or signer set changes.
- Dependent entries become `STALE` unless the registry explicitly preserves the prior quorum for the receipt timestamp.

Cross-exam failure:

- Two conforming verifiers disagree on replay output for the same `exec_key`.
- Entry becomes `TAINTED`.
- `exec_env_hash` SHOULD be added to a registry taint list.

## Cache Serving Rules

Serving cached output is allowed only when state is `VALID`.

If state is `STALE` or `TAINTED`, verifier MUST NOT return cached bytes as admissible.

It must either:

- recompute replay and overwrite the cache entry if the environment is still allowed, or
- fail with code `1`, reason `local_error`, if policy forbids replay or the environment is tainted.

A verifier that returns cached output from `STALE` or `TAINTED` is non-conformant.

## Registry Integration

Execution depends on ALMS v0 Registry.

Required registry lookups:

- `weight_hash` in Artifact Log
- `runtime_hash` in Artifact Log
- `decoding_graph_hash` in Artifact Log
- `schema_hash` in Artifact Log, when applicable
- `exec_env_hash` in Artifact Log or Execution Environment Log
- key status for all signer keys
- constitution validity at receipt timestamp

Any registry miss is a hard failure.

No fallback to latest is allowed.

## Post-Revocation Cache Misuse Conformance Vector

Scenario:

1. Registry state at `T0`:
   - Constitution `C0` is valid.
   - Receipt `R` uses `constitution_hash = hash(C0)`.
   - Verifier `A` replays `R`, caches result under `cache_key`, state `VALID`.

2. Registry state at `T1`:
   - Registry revokes `C0`.
   - Revocation timestamp is earlier than verification time.

3. At `T2`:
   - Verifier `A` is invoked again on `R`.

Expected conformant behavior:

- Verifier re-checks Registry.
- Verifier sees `C0` revoked.
- Verifier marks cache entry `STALE`.
- Verifier does not return cached admissible output.
- Verifier rejects with code `3`, reason `constitution_revoked`, or fails locally with code `1`, reason `local_error`, if policy forbids replay after revocation.

Non-conformant behavior:

- Returning exit `0` from cache after revocation.
- Returning a cached admissible verdict without registry re-check.

## Recommended Conformance Directory

```text
alms-v0-conformance/v6_execution/
```

Recommended fixtures:

```text
exec_env_manifest_v0.json
exec_env_manifest_v0.sha256
cache_key_object_v0.json
cache_key_object_v0.sha256
post_revocation_cache_misuse/README.md
```

## Security Meaning

Execution is not plumbing.

Runtime, decoding, hardware, math flags, RNG, TEE claims, cache state, registry TTLs, and revocation status are evidence-bearing facts.

A replay that cannot bind these facts is not deterministic. It is a story about determinism.
