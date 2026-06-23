# PAYMENT_PASS_003 — Live Gate Scaffold

**Status:** PAYMENT PASS STARTED  
**Branch:** `gc-v1-pass-003`  
**Canonical Demo:** `MN-STEARNS-003`  
**Builder Code:** `bc_j1200j64`

---

## Purpose

This pass wires the signed payment boundary into a small, reviewable enforcement scaffold for the canonical demo case.

Target flow:

```text
Receipt -> Replay -> Score 78 -> Payment Required -> Prompt Pack Unit
```

---

## Boundary

This pass does not add:

- DDL
- migrations
- subscriptions
- marketplace behavior
- generated images
- agent workflows
- additional seed cases

---

## Enforcement Rule

Before serving the paid Prompt Pack Unit, the service must validate:

```text
docket_id = MN-STEARNS-003
receipt_id = r_mn_stearns_003_v1
nutrition_score = 78
replay_url = https://goblin.court/replay/mn-stearns-003
builder_code = bc_j1200j64
artifact_count = 7
```

The paid artifact must not be served if any lineage field mismatches the signed fixture.

---

## Files

```text
goblin-court-v1/payment/
  README_PAYMENT_PASS_003.md
  payment_boundary_003.json
  gate_003.js
  route_example_003.js
```

---

## Live Middleware Note

`route_example_003.js` is a framework-neutral example route. It marks where a production x402 verifier/facilitator integration must be attached.

The fixture gate is deliberately separated from network settlement so the lineage rules can be reviewed without touching database or deployment state.
