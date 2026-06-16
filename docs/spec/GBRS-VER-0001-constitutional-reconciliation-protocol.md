# GBRS-VER-0001: Constitutional Reconciliation Protocol

**Status:** Draft  
**Version:** 0.1  
**Category:** Verifier / Constitutional Engine  
**Applies to:** All GBRS-governed routing and capability surfaces, including ENS, MCP, DNS, DID, API gateways, agent registries, and future projection surfaces.

---

## 1. Purpose

This specification defines the verifier as the constitutional engine of Governance-Bound Routing Surfaces (GBRS).

The verifier does not merely observe. It reconstructs and enforces `ROUTING_DOWNSTREAM_OF_TRUTH` by reconciling live projections against the canonical truth surface.

The verifier is the protocol's Constitutional Court.

It exists to answer one question:

> Does the live routing or capability surface still derive from canonical replay state?

If the answer is no, the verifier MUST fail closed and reconcile the surface back to canonical truth.

---

## 2. Verifier Function

The verifier is defined as:

```text
V : (TS_c, RS_live) -> RS_corrected
```

Where:

- `TS_c` is the canonical truth surface, including the canonical receipt index.
- `RS_live` is the live routing or capability state currently exposed by one or more projection surfaces.
- `RS_corrected` is the constitutionally valid state after reconciliation.

The verifier MUST treat `TS_c` as authoritative over any operator action, UI state, wallet mutation, local server state, resolver state, manifest, or dashboard projection.

Routing surfaces are outputs. They are not sources of truth.

---

## 3. Lifecycle

### 3.1 Reconstruction

The verifier MUST reconstruct expected state for each governed surface from the canonical truth surface.

Examples:

```text
ENS_expected = Pi_ENS(TS_c, canonical_index)
MCP_expected = Pi_MCP(TS_c, canonical_index)
```

Additional GBRS-compliant surfaces MAY define their own deterministic projection functions, but they MUST derive exclusively from canonical receipts.

### 3.2 Divergence Detection

The verifier MUST compare live state against reconstructed state.

```text
D = RS_live minus RS_expected
```

Any live entry that is missing from, mismatched against, or not lineage-valid under `RS_expected` is non-canonical.

Divergence includes, but is not limited to:

- resolver values that do not match the canonical projected route;
- MCP tools not present in the reconstructed manifest;
- stale records referencing superseded receipts;
- capability entries whose receipt hash does not match canonical lineage;
- routing entries created by operator/UI action without replay binding.

### 3.3 Constitutional Purge

For each non-canonical element in `D`, the verifier MUST purge or mark the element non-authoritative.

Surface-specific examples:

- **ENS:** rogue records MUST be cleared, ignored, or superseded by a canonical projection.
- **MCP:** unauthorized tools MUST be removed from the manifest and MUST NOT be invocable.
- **DNS/API/DID/Agent registries:** non-canonical entries MUST fail closed according to their surface profile.

Rule:

```text
Non-canonical projections MUST be purged.
```

No receipt. No lineage. No projection. No route.

### 3.4 Rollback Visibility

Before applying correction, the verifier MUST emit or require a `ROLLBACK_VISIBLE` receipt describing:

- the divergence;
- the affected surfaces;
- the canonical source receipt or successor receipt;
- the corrected state;
- the purge action or projection replacement.

This prevents silent operator capture.

A rollback that cannot be replayed is not a constitutional rollback.

### 3.5 Re-Projection

After rollback visibility is established, the verifier MUST deploy:

```text
RS_corrected = RS_expected
```

The system then returns to constitutional innocence: all live projections are downstream of canonical truth.

---

## 4. Fail-Closed Semantics

The verifier MUST fail closed under uncertainty.

### 4.1 Missing Index

If the canonical index is missing, unreadable, malformed, or not replay-verifiable:

```text
No index -> no truth -> no route.
```

All governed projections MUST be treated as non-canonical until the canonical index is restored and verified.

### 4.2 Broken Lineage

If lineage is broken, the verifier MUST reject the affected successor and purge any projection depending on it.

### 4.3 Out-of-Band Operator Action

If an operator, wallet, dashboard, resolver, server, or UI mutates a routing surface outside the canonical receipt flow, the verifier MUST override that live state on the next reconciliation cycle.

Operator action is not authority unless it is replay-bound.

---

## 5. Compliance

A system is GBRS-VER-0001 compliant if and only if it satisfies all of the following:

1. It implements:

```text
V(TS_c, RS_live) -> RS_corrected
```

2. It treats `RS_corrected` as authoritative over any live routing or operator state.
3. It logs all purges, divergences, rollbacks, and re-projections as receipts in the truth surface.
4. It fails closed when canonical truth is unavailable.
5. It prevents non-canonical projections from remaining silently active.

Compliance is not achieved by merely detecting drift.

Compliance requires reconciliation.

---

## 6. Role in the GBRS Family

GBRS-VER-0001 is the enforcement layer of the GBRS protocol family.

- `GBRS-INV-0001` defines the invariant: what must always be true.
- `GBRS-RSP-0001` defines surface behavior: how routing surfaces project.
- `GBRS-MCP-0001` defines capability governance: how tools become legal.
- `GBRS-VER-0001` defines reconciliation: how the constitution is enforced.

Together, these documents turn GBRS from a registry pattern into a self-healing constitutional runtime.

---

## 7. Non-Goals

This specification does not define a specific blockchain, resolver, registry, gateway, MCP implementation, or wallet interface.

It defines the constitutional reconciliation rule that all compliant implementations MUST satisfy.

Implementation details belong in surface profiles and executable verifier scripts.

---

## 8. Core Axiom

```text
Routing is downstream of truth, not upstream of it.
```

The verifier is the mechanism that makes this axiom executable.
