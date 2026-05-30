# Witness Lattice v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/witness_lattice_v0_1.md`  
**Status:** Draft / Replay Support Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Witness Lattice v0.1 defines how surviving witness reports may support reconstruction after Archive Fire without becoming proof by themselves.

Witnesses may guide reconstruction.

Witnesses do not create replay.

---

## Rule Object

```json
{
  "rule": "WITNESS_LATTICE_V0_1",
  "purpose": "support_reconstruction_without_converting_claims_into_proof",
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Evidence Node States

```json
{
  "states": [
    "UNVERIFIED_CLAIM",
    "WITNESS_REPORT",
    "CORROBORATED_REPORT",
    "SUPPORTED_FRAGMENT",
    "REPLAY_CANDIDATE",
    "REPLAY_CONFIRMED",
    "TAINTED_REPORT"
  ]
}
```

---

## First Evidence Node

```json
{
  "node_id": "WL-001",
  "node_type": "WITNESS_REPORT",
  "source": "OPERATOR_REPORTED",
  "claim": "A recoverable lineage may exist after Archive Fire if at least one surviving anchor or fragment can be matched to a known hash.",
  "status": "UNVERIFIED_CLAIM",
  "replay_effect": "GUIDES_SEARCH_ONLY",
  "authority": false
}
```

---

## State Delta

```json
{
  "delta_id": "WL-DELTA-001",
  "from": "CLAIM",
  "to": "WITNESS_REPORT",
  "allowed": true,
  "reason": "operator_report_recorded_without_proof_upgrade",
  "authority": false
}
```

---

## Forbidden Promotions

The lattice must not silently promote:

- claim into receipt
- witness report into proof
- corroboration into replay
- memory into lineage
- consensus into authority

---

## Replay Gate

A witness node may become `REPLAY_CANDIDATE` only when paired with at least one replay-relevant artifact:

- surviving anchor
- file hash
- chunk hash
- manifest
- signed receipt
- reproducible output

A witness node becomes `REPLAY_CONFIRMED` only after reconstruction passes replay.

---

## Completion Rule

Witness support is not completion.

Completion requires a replayable result.

```json
{
  "completion_requires": [
    "artifact",
    "hash_or_manifest",
    "replay_test"
  ]
}
```

---

## Status

```json
{
  "artifact": "WITNESS_LATTICE_V0_1",
  "first_node": "WL-001",
  "authority": false,
  "membrane": "HOLDS",
  "status": "DRAFT_CREATED"
}
```
