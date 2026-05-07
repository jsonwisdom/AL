# ALMS-v1-BOUNDARY

Status: DRAFT_V1_BOUNDARY

Parent constitutional epoch: ALMS_v0_KERNEL

```yaml
ALMS_v0_KERNEL:
  CLOSURE_COMMIT: 045e90ee51feb76af0830554a30045fa43f58cd5
  CONSTANTS_COMMIT: 8f9a5dbbdb9e0f2eaff32d35ab9242a8b21a9d47
  STACK_PRECLOSURE_BLOB_SHA: 1c16a77dde5d9beb0262d23d929f89a4be0397c9
  NO_SELF_REFERENTIAL_PARADOX: true
  GLOBAL_STATE: NO_DRIFT
```

## 1. Scope of v1

### Extension only

v1 MAY extend ALMS_v0.

v1 MUST NOT mutate, delete, or reinterpret any ALMS_v0 text, constant, or invariant.

### Binding inheritance

All ALMS_v0 invariants remain fully binding on v1, including but not limited to:

- `NO_SELF_REFERENTIAL_PARADOX`
- frozen coordinate model
- explicit external attestation boundary
- `GLOBAL_STATE` semantics, with `NO_DRIFT` as target state

## 2. Citation Requirement

Every v1 surface, document, schema, protocol, or court MUST explicitly cite:

```text
ALMS_v0_CLOSURE_COMMIT = 045e90ee51feb76af0830554a30045fa43f58cd5
```

This citation:

- anchors v1 to the seated v0 constitutional order, and
- affirms that v1 operates under the ALMS_v0 closure, not beside or above it.

## 3. Coexistence Model

### Non-overwrite rule

v1 amendments MUST coexist beside v0.

They MUST NOT overwrite, redact, or silently supersede v0 surfaces.

### Layering semantics

Where v1 introduces new rules, they are interpreted as:

- extensions when v0 is silent, and
- refinements that MUST remain consistent with v0 when v0 speaks.

### Conflict handling

In any direct conflict between v0 and v1, v0 prevails unless a future, explicitly defined constitutional amendment process is seated in a later epoch.

## 4. New Surfaces Allowed in v1

v1 MAY introduce new:

- courts or court layers,
- treaties or treaty registries,
- registry layers or namespaces,
- execution evidence formats or channels,
- memory layers, such as historical logs, meta-ledgers, and replay indices.

All such surfaces MUST preserve the following invariants.

### Replay supremacy

Any v1 mechanism MUST be replayable from `ALMS_v0_CLOSURE_COMMIT` forward.

No v1 surface may require non-replayable, opaque, or unverifiable side channels.

### Lineage integrity

Provenance chains MUST remain continuous and non-forking with respect to v0.

Any v1 lineage extension MUST be traceable back to `ALMS_v0_CLOSURE_COMMIT`.

### Registry jurisdiction

Registries introduced or extended in v1 MUST clearly define their jurisdiction and MUST NOT silently annex v0 registries.

Cross-registry references MUST be explicit and replayable.

### Execution evidence

New execution layers or evidence formats MUST preserve the ability to:

- reconstruct decisions,
- verify inputs and outputs, and
- bind to v0 provenance and registry records.

### Deterministic refusal

v1 MUST preserve the ability of the system to refuse:

- ambiguous inputs,
- unverifiable claims,
- non-replayable state, and
- attempts to bypass v0 invariants.

## 5. Non-Reopening Guarantee

v1 MUST NOT:

- reopen ALMS_v0 closure,
- retroactively alter ALMS_v0_KERNEL, or
- introduce any mechanism that effectively rewrites v0 under a different name.

Any future epoch that seeks to alter v0 itself MUST:

- declare itself as a constitutional amendment epoch, and
- define a higher-order process that is itself replayable and non-paradoxical.

## 6. Boundary Statement

ALMS-v1-BOUNDARY establishes:

- a legal doorway from ALMS_v0 to ALMS_v1,
- without reopening, mutating, or weakening ALMS_v0, and
- with explicit, replayable obligations on all v1 surfaces.

All v1 documents MUST treat this boundary as binding constitutional law and MUST cite:

```text
ALMS-v1-BOUNDARY.md
ALMS_v0_CLOSURE_COMMIT = 045e90ee51feb76af0830554a30045fa43f58cd5
```
