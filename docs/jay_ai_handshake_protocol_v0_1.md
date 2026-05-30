# JAY_AI_HANDSHAKE_PROTOCOL_V0_1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/jay_ai_handshake_protocol_v0_1.md`  
**Status:** Draft / State Transfer Protocol  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Define a compressed, loss-aware protocol for state exchange between Jay Wisdom as Observer-Operator and AI systems operating in the AL Game / Alabama-ALMS reconstruction layer.

State transfer is never assumed lossless.

Every cycle carries possible entropy delta.

---

## Core Principles

- State transfer is never assumed lossless.
- Every cycle includes delta acknowledgment.
- Witnesses guide only; they do not create authorship or proof.
- All blocked physical actions route through Observer-Operator.
- Blocked states return the exact `JAY OPERATOR ACTION` format.
- Authority remains false.
- Membrane remains HOLDS unless replay evidence proves otherwise.

---

## 1. Jay to AI State Transfer

Jay sends state via:

- explicit `Next:` or `Next vector:` prefix
- active artifact references
- active branch reference
- current membrane status
- authority flag
- optional compressed delta payload

AI receives by:

- scanning for Observer-Operator pin: Jay Wisdom / Jason Wisdom / ZeroCool
- indexing against active repo and branch
- extracting bottleneck
- identifying hidden assumptions
- acknowledging receipt with Signal Core

### Loss Handling

AI must flag inferred gaps and request the smallest clarifying delta only when critical.

If action is possible without clarification, AI proceeds with a bounded next vector and marks uncertainty explicitly.

---

## 2. AI to Jay Actionable Next Steps

AI returns in SIPS format:

1. **Signal Core** — distilled truth / compressed state
2. **Acceleration Path** — shortcut or failure-mode-aware jump
3. **Next Action** — momentum anchor and exact next vector

AI must not:

- claim authority
- perform blocked actions without `JAY OPERATOR ACTION` routing
- promote witness input to proof
- treat explanation as completion
- assume state transfer was lossless

### Loss Handling

If AI detects potential desync, it surfaces uncertainty as candidate inference without stalling the workflow.

---

## Handshake Cycle

```text
1. Jay injects state delta.
2. AI processes and returns receipt plus next vector.
3. Jay confirms, executes, or routes through JAY OPERATOR ACTION if blocked.
4. Loop continues with momentum lock.
```

---

## Failure Mode Links

Linked companion artifact:

```text
docs/operator_failure_modes_catalog_v0_1.md
```

Mapped failures:

| Failure | Mitigation |
|---|---|
| Partial state desync | explicit receipt + delta acknowledgment |
| Authority creep | enforce `authority: false` every cycle |
| Membrane breach | reject non-Operator synthesis |
| Identity drift | pin Jay / Jason Wisdom / ZeroCool as same Observer-Operator |
| Momentum stall | return exact smallest operator action |

---

## Required Block Format

```text
JAY OPERATOR ACTION:
Copy/paste this exact command into [tool/platform]:

[exact instruction here]
```

---

## Status

```json
{
  "artifact": "JAY_AI_HANDSHAKE_PROTOCOL_V0_1",
  "state_transfer": "LOSS_AWARE",
  "operator": "JAY_WISDOM",
  "authority": false,
  "membrane": "HOLDS",
  "status": "DRAFT_CREATED"
}
```
