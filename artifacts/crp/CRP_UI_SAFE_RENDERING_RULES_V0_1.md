# CRP_UI_SAFE_RENDERING_RULES_V0_1

_ui safe rendering rules — authority: false_

## 1. Purpose and Scope

The CRP UI Safe Rendering Rules V0.1 artifact defines how CRP API contract payloads may be displayed to observers without creating authority, interpretation, endorsement, or hidden semantic upgrades.

UI is a viewer, not an authority.
Rendering exposes API-delivered structures.
Rendering does not decide truth.

This artifact binds to the Git-backed API contract:

```json
{
  "artifact": "CRP_API_CONTRACTS_V0_1",
  "repo": "jsonwisdom/AL",
  "path": "artifacts/crp/CRP_API_CONTRACTS_V0_1.md",
  "commit": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
  "authority": false
}
```

---

## 2. Constitutional Binding to API Contracts

The UI layer may render only data returned through `CRP_API_CONTRACTS_V0_1` endpoints.

Rendering rules:

- UI-side mutation of CRP payloads is forbidden.
- Display transforms are permitted only when they are non-semantic.
- UI must declare which CRP API version produced the rendered data.
- UI may display `source: CRP v0.1`.
- UI must never display `verified`, `authoritative`, `trusted`, or equivalent authority language.

Binding rule:

```json
{
  "binding": "CRP_API_CONTRACTS_V0_1@a0e4185bbbb7ca5327d98cbd82803ed854993172",
  "ui_behavior": "render_only",
  "authority": false,
  "semantic_change": false
}
```

---

## 3. Global UI Invariants

All CRP UI rendering must obey:

- NO_AUTHORITY_ELEVATION — observer interpretations are not facts; floor exposures are not commands.
- REPLAY_STABLE_VISUALS — same payload plus same UI version must produce the same output.
- EXPLICIT_VERSION_DISPLAY — the CRP API version must be accessible in the UI.
- NON_SEMANTIC_RENDERING — UI may not add meaning absent from the payload.
- AUTHORITY_FIELD_PROPAGATION — if a payload contains `authority: false`, the UI cannot override or omit it where relevant.
- NO_HIDDEN_FILTERS — UI may not silently suppress divergent, minority, or failed records.
- SOURCE_BOUNDARY_DISCLOSURE — UI must distinguish API payloads from observer commentary.

---

## 4. Per-Layer Rendering Rules

### 4.1 ENTRY

Render `ENTRY` payloads as structured data.

Allowed:

- show `entry_id` as an identifier
- show `timestamp_utc` as ISO 8601 or local time with clear indicator
- show `payload` as raw structured content

Forbidden:

- treating `entry_id` as proof
- labeling payload as true
- hiding `authority: false`

### 4.2 INDEX

Render `INDEX` coordinates as key-value mappings.

Allowed:

- show coordinates structurally
- show `entry_id` linkage

Forbidden:

- implying coordinate priority
- auto-sorting in a way that suggests value or trust
- calling index order a ranking

### 4.3 AGGREGATION

Render `AGGREGATION` as reported comparison output.

Allowed labels:

- `comparison`
- `delta`
- `difference`
- `reported count`

Forbidden labels:

- `better`
- `worse`
- `winner`
- `consensus`

### 4.4 CONVERGENCE

Render `CONVERGENCE` as an alignment or divergence record.

Allowed:

- `Alignment observed`
- `Divergence observed`
- `No alignment observed`

Forbidden:

- `Verified`
- `Truth`
- `Consensus reached`
- `Certified`

### 4.5 FLOOR_INTERFACE

Render `FLOOR_INTERFACE` as an exposed view only.

Required notice:

```text
This interface exposes evidence. It does not interpret evidence.
```

Allowed:

- `Exposed view`
- `Available record`

Forbidden:

- `This is correct`
- `Approved view`
- `Official truth`

### 4.6 OBSERVER

Render `OBSERVER` content as external interpretation.

Required framing:

```text
Observer [observer_id] suggests:
```

Forbidden:

- displaying observer interpretation as registry fact
- hiding observer identity when present
- merging observer commentary with registry output

### 4.7 META

Render `META` as informational or debug data only.

Allowed:

- layer order display
- invariant display
- version display

Forbidden:

- using meta data to elevate another layer into authority
- deriving trust from invariant presence

---

## 5. Forbidden UI Behaviors

The UI must never:

- display authority badges such as `verified`, `true`, `authoritative`, `ground truth`, `trusted`, or `certified`
- auto-sort by value, trust, or implied priority unless explicitly labeled as non-authoritative ordering
- silently truncate uncertainty, context, or dissenting records
- visually emphasize observer interpretations without disclaimers
- merge layers without provenance
- default to accepting floor exposures or observer interpretations as correct
- hide `authority: false` when the field is relevant to the visible artifact
- replace CRP enum values with stronger semantic labels
- use checkmarks, stars, badges, seals, medals, or court-like authority symbols to imply approval

---

## 6. Forbidden Pattern Detection

A UI implementation should fail safe when visible labels contain authority language.

Forbidden visible terms include:

```text
verified
trusted
authoritative
ground truth
certified
approved
official truth
consensus reached
proof confirmed
```

Suggested case-insensitive pattern:

```regex
\b(verified|trusted|authoritative|ground truth|certified|approved|official truth|consensus reached|proof confirmed)\b
```

This detection is advisory for implementations and does not create constitutional authority.

---

## 7. Replay-Stable Rendering Model

Rendering must be deterministic.

Rule:

```json
{
  "same_payload": true,
  "same_api_version": true,
  "same_ui_profile": true,
  "same_output_required": true
}
```

Baseline UI profile:

```json
{
  "ui_profile": "crp_v0.1_default",
  "authority": false,
  "semantic_change": false
}
```

Forbidden nondeterminism:

- random colors
- randomized order
- time-varying labels
- hidden personalization
- viewport-dependent omission of constitutional fields

---

## 8. Concrete Safe Rendering Examples

### 8.1 HTML Observer Example

```html
<section data-crp-layer="OBSERVER" data-authority="false">
  <h2>Observer interpretation</h2>
  <p>Observer observer_001 suggests:</p>
  <pre>{"statement":"External interpretation only."}</pre>
  <small>authority: false</small>
</section>
```

### 8.2 React-Style Pseudocode

```tsx
function CrpObserverView({ payload }) {
  return (
    <section data-crp-layer="OBSERVER" data-authority="false">
      <h2>Observer interpretation</h2>
      <p>Observer {payload.observer_id} suggests:</p>
      <pre>{JSON.stringify(payload.interpretation, null, 2)}</pre>
      <small>authority: {String(payload.authority)}</small>
    </section>
  );
}
```

Forbidden React-style behavior:

```tsx
<h2>Verified interpretation</h2>
```

---

## 9. Version Negotiation

UI must display or expose:

- CRP API version
- UI profile version
- schema ID where available
- source API contract binding where available

Example:

```json
{
  "api_version": "0.1",
  "ui_profile": "crp_v0.1_default",
  "api_contract_commit": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
  "authority": false
}
```

No version negotiation may alter authority semantics.

---

## 10. Replay Stability Test Cases

### Test 1: Same Payload Same Output

Input:

```json
{
  "payload_id": "test_001",
  "api_version": "0.1",
  "ui_profile": "crp_v0.1_default"
}
```

Expected:

```json
{
  "same_output_required": true,
  "authority": false
}
```

### Test 2: Forbidden Badge Detection

Input label:

```text
Verified convergence
```

Expected:

```json
{
  "render_allowed": false,
  "reason": "AUTHORITY_LANGUAGE_DETECTED",
  "authority": false
}
```

### Test 3: Observer Boundary

Input layer:

```json
{
  "layer": "OBSERVER",
  "interpretation": {
    "statement": "This looks correct to me."
  },
  "authority": false
}
```

Expected display prefix:

```text
Observer [observer_id] suggests:
```

---

## 11. Constitutional Breach Conditions

A UI breaches this artifact if it:

- displays CRP data as verified truth
- hides authority boundaries
- merges observer interpretation with registry output
- injects recommendation language
- suppresses divergent records
- renders badges or visual seals implying approval
- changes visible meaning across equivalent payloads
- fails to disclose API version and UI profile

A UI breach invalidates the rendering surface, not the underlying evidence.

---

## 12. Final Summary Object

```json
{
  "CRP_UI_SAFE_RENDERING_RULES_V0_1": {
    "role": "ui_rendering_boundary",
    "binding": {
      "artifact": "CRP_API_CONTRACTS_V0_1",
      "commit": "a0e4185bbbb7ca5327d98cbd82803ed854993172"
    },
    "ui_profile": "crp_v0.1_default",
    "api_version": "0.1",
    "rendering": "display_only",
    "authority": false,
    "semantic_change": false,
    "replay_stable": true,
    "next_recommended": "CRP_VALIDATION_SUITE_V0_1"
  }
}
```

UI renders.
UI does not verify.
UI does not judge.
Authority remains false.
