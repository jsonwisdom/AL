# proof_blob Specification v0.1

Status: DESIGN_SPEC_NOT_OPERATIONAL

## Purpose

The proof_blob object defines the canonical replay-verifiable output format for AGW / ALMS procedural integrity measurements.

proof_blob objects are intended to:

- anchor replay outputs
- bind verdicts to evidence boundaries
- support GitHub-based replay verification
- support future proof systems
- separate public verification from restricted content

proof_blob objects are not verdicts about people, morality, guilt, or institutional legitimacy.

## Canonical Shape

```json
{
  "artifact": "PROOF_BLOB_V0_1",
  "receipt_id": "string",
  "track_id": "string",
  "circuit_id": "string",
  "target_url": "string",
  "canonical_hash": "sha256:...",
  "crawl_timestamp": "ISO8601",
  "verdict": "string",
  "public_inputs": {
    "url_hash": "sha256:...",
    "expected_manifest_hash": "sha256:..."
  },
  "proof_ref": "string",
  "merkle_root": "sha256:...",
  "restricted_layer_ref": "string|null",
  "state": "REPLAYABLE"
}
```

## Allowed Verdict Classes

```json
[
  "FOUND",
  "NOT_FOUND",
  "REPLAY_FAIL",
  "REFUSAL_CAPTURE_R1",
  "REFUSAL_CAPTURE_R2",
  "REFUSAL_CAPTURE_R3",
  "MANIFEST_MISMATCH",
  "DOCKET_GAP",
  "EVIDENCE_INACCESSIBLE"
]
```

## 404 Governance Minimal Circuit

The minimal 404 replay circuit may compare:

- expected hash
- observed hash
- manifest hash
- URL hash

Minimal logic:

```text
if observed_hash == expected_hash:
    verdict = FOUND
else:
    verdict = NOT_FOUND
```

## Public vs Restricted Boundary

proof_blob objects may publicly expose:

- hashes
- verdicts
- Merkle roots
- timestamps
- replay state
- public inputs

proof_blob objects must not expose restricted ciphertext plaintext.

## Canonical Replay Requirements

A replay verifier must be able to:

- recompute canonical hashes
- recompute Merkle roots
- verify verdict consistency
- verify fixture compatibility
- distinguish public vs restricted references

without network trust assumptions.

## GitHub Direct Invariant

proof_blob objects are designed for GitHub-first replay:

```json
{
  "inputs": "git + declared replay state",
  "outputs": "deterministic verdict surface",
  "network_required": false
}
```

## Non-Claims

proof_blob objects do not prove:

- guilt
- intent
- corruption
- authenticity of hidden content
- institutional morality
- legal finality

proof_blob objects prove only replay-visible procedural state.

## State

```json
{
  "proof_blob_v0_1": "DESIGN_SPEC_NOT_OPERATIONAL",
  "stark_layer": "NOT_IMPLEMENTED",
  "404_circuit": "SPECIFIED_ONLY",
  "no_ghost_anchor": true
}
```
