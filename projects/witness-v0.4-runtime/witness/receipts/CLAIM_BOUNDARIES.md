# Witness Claim Boundaries

This document defines the exact semantic claims that the Witness runtime legitimacy system is permitted to make.

It is the constitutional reference for every layer: emission, validation, observability, tests, and future enforcement.

Any new code or endpoint must stay within these boundaries.

## 1. CI Runtime Receipts

File:

```text
ci-runtime-receipt.json
```

### What they prove

- Ephemeral convergence of the CI runtime at the exact moment the receipt was emitted.
- The build/test environment reached a known-good state for that CI run.
- The runtime booted under CI and answered the required endpoints.
- The receipt passed loader validation and required convergence checks.

### What they do not prove

- Persistent continuity after the CI job finishes.
- Live hosted availability of the deployed service.
- Long-term integrity of any running instance.
- Any guarantee about the production runtime environment.
- That the code currently serving traffic is the same code that converged in CI.

### Explicit claim language

```text
proves ephemeral CI runtime convergence only; does not prove persistent continuity or live hosted availability
```

## 2. Render Layer

Render is an optional hosting layer.

### What Render can prove if implemented correctly

- A live URL reached a Witness runtime.
- The runtime responded to endpoint probes.
- The deployment surface was reachable at probe time.

### What Render does not prove

- Persistent continuity.
- That the runtime has a valid CI receipt unless `/legitimacy` says so.
- That the runtime state survived restarts.
- That the hosted service is a canonical authority surface.

## 3. Permanent Anchoring

Permanent anchoring is a future phase.

### What permanent anchoring may prove when added

- A receipt or artifact was published to a durable public surface.
- The artifact can be independently retrieved and checked.
- A public identity such as `jaywisdom.base` can point to a receipt rather than a runtime.

### What it still would not prove

- That a live service is currently reachable.
- That production state is persistent.
- That application-level outputs are correct.

## Enforcement Rule

No code path may return `runtime_converged: true` unless a valid CI receipt is physically present and passes full loader validation.

No code path may imply stronger guarantees than the boundaries above.

This document must be referenced in:

- New tests that touch runtime evidence.
- The `/legitimacy` endpoint docstring or route notes.
- Future guards or middleware.
- Pull requests that touch the Witness receipt subsystem.

## Last Updated

2026-05-16 — post #216 membrane lock.
