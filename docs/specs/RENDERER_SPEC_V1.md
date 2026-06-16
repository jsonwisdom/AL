# Renderer Spec v1

**Standard:** `RENDERER_SPEC_V1`  
**Parent:** `INHERITANCE_MODEL_V1`  
**Identity:** `jaywisdom.base.eth`  
**Applies To:** Auditable Tree Component, Family Node navigation, War Board dashboard  
**Status:** PUBLIC REPO CANON — EXECUTABLE RENDERER LAW

## Purpose

The renderer is not the constitution.

The renderer is a translator of the constitution.

This specification defines the executable rules that an Auditable Tree Component must obey before drawing parent, family, and child surfaces.

## 1. Inputs

`truth.json` is the sole authority for live rendering.

The renderer MUST fetch `truth.json` at runtime.

The renderer MUST NOT treat file existence, commit naming, or path naming as proof of attestation.

Optional `lineage.json` may be used for nested tree structure, but every node ID rendered from lineage data MUST also exist in `truth.json` or the renderer must fail closed.

## 2. Cache Rule

A renderer MUST NOT use a cached `truth.json` older than 60 seconds when network access is available.

If fresh `truth.json` cannot be fetched, the renderer MAY show local preview data only if visibly labeled:

```text
LOCAL PREVIEW — NOT LIVE TRUTH
```

## 3. Pre-Render Validation

Before drawing any pixels, the renderer must:

1. Parse `truth.json`.
2. Confirm `truth_boundary` exists.
3. Confirm `lineage_tree` exists if a tree is requested.
4. For each node:
   - If dedicated onchain status is true, require `eas_uid` or `schema_uid`.
   - If required fields are missing, mark `BREACH: Ghost Claim`.
   - If a green edge is requested without a verified UID, mark `BREACH: Edge Integrity`.
5. If any breach exists, halt normal render and display a high-visibility breach banner.

## 4. Rendering Rules

### PARENT_REFERENCED / INHERITS

Edge style:

```css
stroke: #666;
stroke-dasharray: 4 4;
opacity: 0.7;
```

Node badge:

```text
INHERITS
```

No glow. No gradient. No animation implying verification.

### ATTESTATION_CHAINED / ATTESTS

Edge style:

```css
stroke: #22c55e;
stroke-width: 2;
```

Node badge:

```text
ATTESTS
```

Must display truncated UID linking to EASScan or equivalent explorer.

### BREACH

Edge style:

```css
stroke: #ef4444;
stroke-width: 3;
```

Overlay text:

```text
BOUNDARY VIOLATION
```

## 5. Prohibited Behaviors

The renderer MUST NOT:

- infer status from file existence
- infer status from commit history
- infer status from naming conventions
- interpolate visually between gray and green
- default to green on error
- allow client-side override of `truth.json`
- hide non-claims
- show a UID as verified unless Observer A or equivalent verification status is present

## 6. Audit Surface

The renderer MUST expose:

- validation summary in console
- load timestamp
- `truth.json` hash
- source `truth.json` URL
- breach count
- rendered node count

The page footer MUST display:

```text
truth.json hash=<hash> loaded_at=<timestamp>
```

## 7. Failure Mode

Fail closed.

If truth cannot be parsed, lineage cannot be validated, or a ghost claim is detected, the renderer must show the breach state instead of a normal tree.

## Constitutional Rule

No pixel may imply a receipt that does not exist.

The map is a servant of the law.

The joke can fly. The receipt must land.
