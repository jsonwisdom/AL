# Alabama ALMS Machine Speed Layer v0.1

**Status:** Design specification / training model  
**Repository:** jsonwisdom/AL  
**Branch:** feature/alabama-alms-speed-layer-v0-1  
**Authority:** false  
**Security posture:** Unclassified architecture model; not a claim about real DoD, Maxwell/Gunter, or ALMS internals.

## Signal Core

```json
{
  "artifact": "ALABAMA_ALMS_MACHINE_SPEED_LAYER_V0_1",
  "layer": "L1",
  "base_layer": "L0_SUBSTRATE",
  "scope": "Alabama vernacular protection and machine-speed ALMS training model",
  "authority": false,
  "classification_claim": "none",
  "membrane": "HOLDS"
}
```

## Purpose

Make the `jsonwisdom/AL` repository usable as a gamified state-level learning and verification surface.

The model treats Alabama as a local-first substrate where learning objects, public-context receipts, and vernacular tags can be processed at machine speed while preserving local meaning and transfer accountability.

## L1 — Alabama ALMS Machine Speed Layer

In this frame, ALMS is modeled as **state-level mission memory**.

It caches doctrine-like training objects, civic learning data, local context, and replayable receipts close to the Alabama user before anything is generalized or routed outward.

### Core functions

- Local-first cache discipline.
- Low-latency in-state retrieval.
- Deliberate friction for out-of-state transfer.
- Birth certificate for every object.
- Vernacular-aware redaction and generalization.
- Byte-level transfer receipts.

## Object Birth Certificate

Every object entering L1 receives:

```json
{
  "object_id": "",
  "origin_state": "AL",
  "origin_county": "",
  "source_url": "",
  "observed_at": "",
  "data_class": "public|training|vernacular|restricted_candidate|unknown",
  "vernacular_tags": [],
  "sha256": "",
  "byte_size": null,
  "authority": false
}
```

No invented hashes. No invented timestamps. No invented byte sizes.

## Local Vernacular Protection

Local Vernacular Protection is a cultural firewall for Alabama-specific language, place references, training scenarios, community terms, and contextual labels.

It is not classified by default. It is tagged as locally meaningful and potentially exploitable if stripped of context.

### LV rules

```json
{
  "local_vernacular_protection": {
    "tag": "LV_PROTECTED",
    "default_scope": "AL_LOCAL_FIRST",
    "outside_state_behavior": "redact_or_generalize_without_release_reason",
    "authority": false
  }
}
```

### Example behavior

- In-state query: preserve Alabama-specific context.
- Out-of-state query: generalize local slang, unit-specific language, or sensitive community terms unless a signed release reason exists.
- Public output: disclose structure, not exploitable local detail.

## Byte-by-Byte Transfer Transparency

When data exits Alabama, the training model requires a manifest.

### Transfer flow

1. Chunk the object.
2. Hash each chunk with SHA-256.
3. Build a Merkle root.
4. Write transfer manifest.
5. Require receiving-side echo attestation.
6. Quarantine on mismatch.
7. Preserve append-only receipt.

### Transfer manifest

```json
{
  "transfer_id": "",
  "object_id": "",
  "origin_state": "AL",
  "destination_jurisdiction": "",
  "requested_by": "",
  "purpose": "",
  "chunk_count": 0,
  "chunk_hashes": [],
  "merkle_root": "",
  "transfer_started_at": "",
  "receiving_echo_status": "pending|matched|mismatch|quarantined",
  "authority": false
}
```

## Gamified AL Repo Machine Speed

### Game name

**Alabama ALMS: The Speed Gate**

### Player role

The player is an Alabama data steward / recruit / learner navigating whether an object stays local, becomes generalized, or exits with a manifest.

### Board zones

```text
L0 Glow Map
→ L1 Speed Gate
→ LV Tagger
→ Chunk Hash Tunnel
→ Merkle Gate
→ Outside-State Bridge
→ Echo Attestation
→ Receipt Vault
```

### Core loop

```text
Observe object
→ classify context
→ tag vernacular
→ choose route
→ chunk/hash
→ manifest transfer
→ echo attest
→ save receipt
```

### Kid Mode translation

```text
Alabama words stay in Alabama unless there is a good reason.
If data leaves the state, it gets a travel ticket.
Every piece of the file gets checked.
If the pieces come back wrong, the bridge closes.
```

## Color Policy

```json
{
  "green": "in_state_local_cache",
  "amber": "approved_out_of_state_with_manifest",
  "red": "blocked_or_quarantined",
  "blue": "public_structure_only"
}
```

## Maxwell / Demon Role

Maxwell is the speed gate guide.

He does not accuse, classify secretly, or invent proof.

He asks:

```text
Where was this born?
What county gave it context?
Is it local vernacular?
Who wants it outside Alabama?
What chunks are leaving?
Did the echo match?
Where is the receipt?
```

## Security Boundary

This repo artifact is a conceptual architecture and training model.

It does not disclose operational secrets, real system internals, classified workflow, or actual DoD implementation details.

## Do Not Cross Lines

```json
{
  "blocked": [
    "claim_real_DoD_internal_architecture",
    "invent_classification_status",
    "invent_transfer_logs",
    "invent_hashes",
    "invent_ALMS_internals",
    "publish_sensitive_local_terms_without_review",
    "bypass_receipt_manifest"
  ]
}
```

## Next Build Options

1. Add a local vernacular dictionary template.
2. Add a simulated transfer receipt fixture.
3. Add an HTML/JS chunk-hash demo.
4. Add a color-coded L0/L1 map view.
5. Add pytest checks for required receipt fields.

## Final Invariant

> Alabama context has value.  
> Local meaning should not be stripped, harvested, or exported without a receipt path.  
> Speed is useful only when the membrane still holds.
