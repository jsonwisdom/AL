# Deterministic Civic Memory — Minimal Records, Replayable Proofs, and the ALMS Core Variant Detector

## Status

`DETERMINISTIC_CIVIC_MEMORY_V1_OPENED`

---

## Core Thesis

American civic publishing does not require a new platform first.

It requires a replayable public record layer.

ALMS proposes a minimal civic verification architecture where public records, media, agent actions, and institutional outputs are converted into canonical byte artifacts, receipt hashes, manifests, and replayable proofs.

The system does not require government adoption, platform permission, or full onchain storage.

GitHub, CSV, JSON, IPFS/Pinata, and public verifiers form the primary proof surface.

ENS, Base, and EAS function as optional discovery and witness layers.

---

## Minimal Records Doctrine

```text
CSV / JSON / media / PDF
-> canonical bytes
-> receipt hash
-> Merkle / manifest
-> public verifier
-> optional Base/EAS/ENS witness
-> voice/schema searchable civic memory
```

The architecture minimizes trust surface area while maximizing replayability.

Truth derives from deterministic recomputation.

Not from platform authority.

---

## Minnesota — State Fixture #001

Minnesota became the first ALMS civic replay fixture because its public records infrastructure was stable enough to support:

- canonical transforms
- receipt emission
- provenance continuity
- independent verification
- replayable civic proofs

The innovation is not "government onchain."

The innovation is deterministic civic replay.

---

## Deterministic Civic Memory

Transparency means the public can view the record.

Deterministic civic memory means the public can independently recompute the same truth state from the same canonical evidence.

A civic artifact becomes replay-admissible only when:

1. the source is identifiable,
2. the transform policy is deterministic,
3. the canonical byte representation is reproducible,
4. the receipt lineage is continuous,
5. and independent operators recompute the same verification state.

Transparency alone is insufficient.

Replay equivalence is required.

---

## ALMS Core Variant Detector (CVD)

The ALMS Core Variant Detector is a deterministic replay subsystem that detects divergence between canonical verification state and observed replay state.

The CVD does not determine:

- political legitimacy
- institutional authority
- narrative preference
- semantic intent

The CVD determines:

- replay equivalence
- transform stability
- provenance continuity
- identity consistency
- structured divergence classification

### Variant Classes

#### V1 — BYTE_VARIANT

Invariant violated:
`Canonical Byte Determinism`

Detection:
- sha256 mismatch
- keccak mismatch
- canonicalization drift
- non-idempotent transforms

Verdict:
`FAIL`

---

#### V2 — TRANSFORM_VARIANT

Invariant violated:
`Deterministic Transform Policy`

Detection:
- transform policy hash mismatch
- parser divergence
- OCR nondeterminism
- layout heuristic mismatch

Verdict:
`TAINTED` or `INDETERMINATE`

---

#### V3 — PROVENANCE_VARIANT

Invariant violated:
`Provenance Continuity`

Detection:
- broken Merkle continuity
- missing attestations
- inconsistent ancestry
- orphan receipts

Verdict:
`FAIL`

---

#### V4 — IDENTITY_VARIANT

Invariant violated:
`Identity / Proof Separation`

Detection:
- ENS reassignment
- signer rotation
- conflicting attesters
- identity drift

Verdict:
`REVIEW_REQUIRED`

---

#### V5 — SEMANTIC_VARIANT

Invariant violated:
`Semantic Stability`

Detection:
- legal language mutation
- policy inversion
- numerical drift
- adversarial rewording
- selective omission

Verdict:
`HIGH_RISK_VARIANT`

---

## Governance Model

Jay's Pincer Movement describes a dual-sided verification architecture:

Side A:
Institutions publish records, budgets, policies, laws, and operational artifacts.

Side B:
Independent operators and agents replay canonical evidence through deterministic verification pipelines.

The objective is not narrative alignment.

The objective is replay equivalence across independent observers.

---

## Final Rule

Identity resolves discovery.

Replay resolves truth.

Verify > narrative.
