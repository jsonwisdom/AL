# ALMS Social-Layer Doctrine

## Classification

```txt
CLASSIFICATION: PUBLIC_SIGNAL_LAYER_OK
NOT_CLASSIFICATION: RECEIPT
BOUNDARY: SOCIAL_ANNOUNCEMENT_ONLY
MAPPING: NARRATIVE → PROOF_POINTER
```

## Invariant

Narrative may gesture; only artifacts prove.

## Core Rule

Public seals, tweets, images, screenshots, graphics, posts, and announcements are proof pointers only.

They are not receipts.  
They are not verifier inputs.  
They are not admissible machine proof.

## Layer Separation

```txt
public_seal  → signal
live_intel   → mirror
github_repo  → record
merkle_root  → commitment
receipt      → proof_object
```

## Canonical Definitions

**signal:** A human-facing object that points toward proof but does not prove.

**mirror:** A dashboard or public display derived from machine state.

**record:** Repository state, commits, paths, manifests, and audit logs.

**commitment:** A deterministic root hash binding a set of receipt leaves.

**proof_object:** A deterministic, hash-bound artifact produced by the verifier, replayable from repository state.

## Non-Admissible Examples

The following objects are never admissible as proof:

- Tweets, posts, threads, or replies
- Images, graphics, badges, seals, or logos
- Screenshots of dashboards or terminals
- Copilot summaries or natural-language descriptions
- Any narrative claim without a backing artifact

## Required Backing

A social object may point to proof only when backed by machine artifacts such as:

- repo commit
- batch root
- manifest hash
- leaf count
- preflight log
- worktree status
- receipt path

## Why This Doctrine Exists

The social layer is inherently narrative.

ALMS is inherently non-narrative.

This doctrine prevents narrative objects from entering the verifier boundary, ensuring that all claims remain reproducible, hash-bound, and adversarially verifiable.
