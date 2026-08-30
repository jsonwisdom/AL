# Chaos & Order of Vertical Scaling Magnitude v0.1-θ

**Parent systems:** `AMERICAN_HISTORY_3D_NAVIGATION_SCHEMA_v0.1`, `TRANSITION_CONTROL_MATRIX_v0.1-theta`, `GAMIFIED_STATE_WARFARE_v0.1-theta`  
**Classification:** Measurement & teaching layer for systemic tension  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Vessel status:** EMPTY_VESSEL  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Name and bound a vertical scale that measures how far a claim, session, or institution sits between **Chaos** and **Order** as depth and magnitude increase. This is a pedagogical instrument. It does not adjudicate history, assign legal status, or open Gate 1.

```text
CHAOS ↔ ORDER          = VERTICAL_SCALING_MAGNITUDE
MAGNITUDE              = DEPTH × COHERENCE × CUSTODY
SCALE_READING          ≠ AUTHORITY
SCALE_READING          ≠ HISTORICAL_TRUTH
SCALE_READING          ≠ GATE_1_OPEN
```

## 2. Axes

### Horizontal (inherited)

- **X — Time** (US3D)
- **Y — Geography / pathing** (US3D)

### Vertical (this layer)

- **Z — Authority depth** (Z0 SOURCE_BYTES → Z8 INTERPRETATION) — already defined
- **M — Scaling magnitude** — how much Chaos or Order is concentrated at that depth

```text
M = f(depth_layer, evidence_coherence, custody_integrity, fork_pressure, gap_pressure)
```

M is reported as a signed or labeled reading, not as a sovereign claim.

## 3. Chaos ↔ Order Continuum

| Pole | Simulation meaning |
|------|--------------------|
| **Chaos** | Missing bytes, broken custody, collapsed forks, unscoped authority jumps, narrative over procedure |
| **Order** | Byte integrity, preserved provenance, explicit jurisdiction, append-only receipts, fail-closed gates |

Neither pole is morally absolute inside the game. Extreme Order without SELF∩JUSTICE can become brittle; extreme Chaos without disclosure becomes noise.

## 4. Magnitude Bands (Informative)

```text
M0  TRACE        — single receipt, local coherence
M1  LOCAL        — session-scale, one claim chain
M2  DOCKET       — multi-claim, still sandbox
M3  INSTITUTION  — simulated institutional surface
M4  SYSTEM       — cross-route, multi-era campaign
M5  HORIZON      — full-spine campaign (pedagogical only)
```

Higher M only means larger *scope of simulation*. It never means higher real-world rank.

## 5. Coupling to Dual-Axis & Gates

- **SELF ≈ JUSTICE** remains mandatory for real-source *proposal* eligibility (Student Certification).
- Vertical magnitude does not replace WEAKEST_LINK disclosure.
- Advancement through STUDENT → … → STEWARD still follows the Transition Control Matrix; M is observational.
- Gate 1 stays BLOCKED until operator admission + epistemic_class + byte-capture pair.

## 6. Readings (Receipt Payload Sketch)

```json
{
  "chaos_order_reading": {
    "depth_layer": "Z2",
    "magnitude_band": "M1",
    "pole_lean": "ORDER",
    "coherence": 0.0,
    "custody_integrity": 0.0,
    "fork_pressure": 0.0,
    "gap_pressure": 0.0,
    "authority": false,
    "gate_1": "BLOCKED"
  }
}
```

Numeric fields are simulation scores (0–1). They create no public ranking.

## 7. Hard Boundaries

```text
MAGNITUDE_IS_NOT_RANK           = ENFORCED
CHAOS_LABEL_IS_NOT_GUILT        = ENFORCED
ORDER_LABEL_IS_NOT_LEGITIMACY   = ENFORCED
NO_GATE_1_VIA_MAGNITUDE         = ENFORCED
NO_MASS_VIA_MAGNITUDE           = ENFORCED
NO_ROLE_MERGE_VIA_SCALE         = ENFORCED
```

Separation of Duties remains FROZEN.

## 8. Use in Media Modes

- Cold cases: plot M as investigative difficulty / messiness
- Reenactments: show how procedure moves a scene toward Order without inventing bytes
- 80s RePlay / JSON streams: optional on-screen Chaos–Order meter (entertainment only)
- Teaching props: vertical slider or depth cards paired with magnitude bands

## 9. Current State

```text
ARTIFACT              = CHAOS_ORDER_VERTICAL_SCALING_v0.1-theta
SCALE                 = CHAOS ↔ ORDER × MAGNITUDE
GATE_1                = BLOCKED
VESSEL_STATUS         = EMPTY_VESSEL
AUTHORITY             = FALSE
CORE_DOCKET           = EMPTY
PROMOTION             = BLOCKED
```

## 10. Promotion Boundary

A scale for teaching tension is not a theory of the state and not a license for real conflict. Real-source work still requires Entrenched Admissions and an open Gate 1 after explicit operator action.
