# ALMS v0 Registry

## Purpose

ALMS Registry defines jurisdiction for receipt verification.

A receipt is not admissible merely because it is well-formed, signed, or locally deterministic. It is admissible only if every referenced trust root, constitution, artifact, key, schema, and parent receipt resolves through a current registry state under ALMS v0 rules.

Provenance decides lineage. Registry decides jurisdiction.

## Design Choice

ALMS v0 uses three independent append-only logs with separate quorum signatures:

1. Trust Root Manifest Log
2. Constitution Log
3. Artifact Log

A global registry snapshot MAY later aggregate these logs into a Merkle root, but v0 preserves fine-grained revocation semantics.

## Core Objects

### Trust Root Manifest

No root, no admission.

Verifiers pin a `root_id` out of band. Everything else is resolved from that root.

Required fields:

```json
{
  "object": "ALMS_TRUST_ROOT_MANIFEST_V0",
  "root_id": "<string>",
  "root_hash": "<sha256>",
  "signers": [
    {
      "key_id": "<string>",
      "public_key_hash": "<sha256>",
      "status": "ACTIVE"
    }
  ],
  "quorum": {
    "threshold": 2,
    "total": 3
  },
  "valid_from": "<iso8601>",
  "valid_until": "<iso8601|null>",
  "supersedes": "<root_hash|null>",
  "signatures": ["<signature>"]
}
```

Verifier rules:

- `root_id` must be pinned by verifier configuration.
- Root signatures must meet quorum.
- Expired or revoked roots are inadmissible.
- Missing root yields code `2`, reason `root_missing`.
- Quorum failure yields code `2`, reason `root_quorum_not_met`.

### Constitution Log

The constitution hash is a pointer into a signed append-only log.

Required fields:

```json
{
  "object": "ALMS_CONSTITUTION_ENTRY_V0",
  "constitution_hash": "<sha256>",
  "constitution_jcs_sha256": "<sha256>",
  "constitution_location": "<uri>",
  "governance_metadata": {
    "proposed_by": "<key_id>",
    "ratified_at": "<iso8601>",
    "supersedes": "<constitution_hash|null>",
    "revoked_at": null
  },
  "root_id": "<string>",
  "root_quorum_signatures": ["<signature>"]
}
```

Verifier rules:

- `policy.constitution_hash` must resolve to a Constitution Log entry.
- Constitution bytes must hash to `constitution_hash`.
- Root quorum signatures must validate under the pinned trust root.
- `revoked_at == null` means currently active.
- If `revoked_at` is non-null and `revoked_at <= receipt.timestamp`, reject with code `3`, reason `constitution_revoked`.
- If the hash is missing, reject with code `3`, reason `constitution_missing`.
- If bytes mismatch, reject with code `3`, reason `constitution_mismatch`.
- If quorum fails, reject with code `3`, reason `constitution_quorum_not_met`.

### Artifact Log

Artifacts include weights, runtimes, decoding graphs, and schemas.

Required fields:

```json
{
  "object": "ALMS_ARTIFACT_ENTRY_V0",
  "artifact_type": "weight|runtime|decoding_graph|schema",
  "artifact_hash": "<sha256>",
  "artifact_location": "<uri>",
  "publisher": "<key_id>",
  "publisher_signature": "<signature>",
  "root_id": "<string>",
  "root_quorum_signatures": ["<signature>"],
  "valid_from": "<iso8601>",
  "valid_until": "<iso8601|null>",
  "replay_ttl_seconds": 86400
}
```

Verifier rules:

- Publishers are not trust roots. Root quorum endorsements are authoritative.
- Every referenced artifact hash must resolve in the Artifact Log.
- Artifact bytes must hash to `artifact_hash`.
- If missing, reject with code `4`, reason `artifact_missing`.
- If hash mismatch, reject with code `4`, reason `artifact_mismatch`.
- If root quorum fails, reject with code `4`, reason `artifact_quorum_not_met`.
- If expired at receipt timestamp, reject with code `4`, reason `artifact_expired`.

## Key Status and Revocation

Receipts MAY include:

```json
{
  "key_status_url": "<uri>",
  "valid_until": "<iso8601>"
}
```

`key_status_url` MUST return a signed status object:

```json
{
  "object": "ALMS_KEY_STATUS_V0",
  "key_id": "<string>",
  "status": "GOOD|REVOKED|UNKNOWN",
  "this_update": "<iso8601>",
  "next_update": "<iso8601>",
  "reason": "<string|null>",
  "root_id": "<string>",
  "root_quorum_signatures": ["<signature>"]
}
```

Verifier rules:

- Cache key status only until `next_update - this_update`, maximum one hour.
- If status fetch fails, reject with code `2`, reason `key_status_unreachable`.
- If status signature is invalid, reject with code `2`, reason `key_status_signature_invalid`.
- If status is `REVOKED`, reject with code `2`, reason `key_revoked`.
- If status is stale, reject with code `2`, reason `key_status_stale`.
- If `valid_until < now`, reject with code `2`, reason `receipt_expired`.

## Replay Windows

Registry entries MAY include:

```json
{
  "replay_ttl_seconds": 86400
}
```

Verifier rules:

- After TTL, remote fetch replay may be refused unless the verifier has a local, bit-identical copy of the artifact.
- Remote fetch after TTL must not silently fall back to latest artifact.
- A cache entry is valid only when keyed by the full hash tuple.

Required cache key for model execution:

```text
(weight_hash, runtime_hash, decoding_graph_hash)
```

Any cache miss is a registry miss, not a license to use latest.

## Admissibility vs Persuasiveness

Registry decides admissibility.

Admissible means:

- receipt chain resolves,
- all parent receipts are admissible,
- all constitutions are active at receipt timestamp,
- all keys are good at receipt timestamp,
- all artifact hashes resolve,
- all signatures meet root quorum.

Persuasive means a human or automated court evaluates the content and legitimacy of the governing constitution or trust root.

The verifier proves the chain is intact. It does not decide whether the root is morally or politically persuasive.

## Exit Code Taxonomy

Registry-related failures use these codes:

```text
2 = identity, key, or trust-root failure
3 = policy or constitution failure
4 = artifact, runtime, schema, or execution dependency failure
5 = provenance parent failure
```

Precise reasons include:

```text
root_missing
root_quorum_not_met
key_status_unreachable
key_status_signature_invalid
key_status_stale
key_revoked
receipt_expired
constitution_missing
constitution_mismatch
constitution_revoked
constitution_quorum_not_met
artifact_missing
artifact_mismatch
artifact_quorum_not_met
artifact_expired
```

## Security Meaning

Revocation must bite.

A compromised key, revoked constitution, expired artifact, or invalid root must invalidate all downstream receipts without manually chasing each child.

Registry is how ALMS turns revocation from a narrative announcement into a machine-checkable state transition.
