# MEDIA_MESH_V1 ML Boundary Doctrine

## Core Rule

```txt
ML MAY ASSIST INTAKE.
ML MUST NEVER DEFINE PROOF.
```

This document defines where machine learning may operate around MEDIA_MESH_V1 and where it is permanently forbidden.

MEDIA_MESH_V1 is a verification system, not an AI fact-checker. Its proof layer must remain deterministic, byte-stable, replayable, and independently auditable.

## Safe Zone: ML-Assisted Intake

Machine learning may assist before an artifact enters the proof chain.

Allowed uses:

- discovery of candidate sources
- routing and triage
- language detection
- duplicate candidate detection
- source prioritization
- summarization for human review
- extraction assistance before canonicalization
- topic grouping outside the receipt core

In this zone, ML output is only a hint. It is not evidence. It is not a verdict. It must pass through deterministic canonicalization before becoming part of any receipt.

## Forbidden Zone: Proof Layer

Machine learning must never control or define:

- canonical JSON formatting
- leaf hash generation
- Merkle tree construction
- proof generation
- proof verification
- bundle validation
- anchor verification
- MATCH / MISMATCH verdicts
- BREAK / NO_BREAK verdicts
- final inclusion or replay results

The proof layer must be fully reproducible using only scripts, artifacts, and deterministic hash rules.

## Why This Boundary Exists

Machine learning can be useful for reducing noise and finding candidates, but it is not a cryptographic primitive.

ML outputs may vary by:

- model version
- hardware
- quantization
- sampling settings
- prompt structure
- runtime environment
- hidden provider changes

Those properties are unacceptable inside the proof layer.

## BitNet Placement

BitNet-style models may be useful for efficient local intake support:

- local triage
- local summarization
- local routing
- low-cost extraction assistance
- edge-device discovery

BitNet does not improve cryptographic verification. It does not replace hashing, canonicalization, Merkle proofs, anchors, or replay verification.

BitNet belongs at the edge, not in the core.

## Architecture Boundary

```txt
ML / BitNet Layer:
  suggest
  route
  summarize
  prioritize
  detect candidates

MEDIA_MESH Core:
  canonicalize
  hash
  prove
  verify
  fail explicitly
```

## Non-Negotiable Rule

If a result cannot be reproduced without a model, it cannot be part of the proof layer.

## Minimal Doctrine Statement

```txt
Models can point.
Receipts must prove.
```

## Final Position

MEDIA_MESH_V1 may use ML around the system.

MEDIA_MESH_V1 must never require ML to verify the system.
