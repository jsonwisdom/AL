# Jay Recursive Operator Rule v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/jay_recursive_operator_rule_v0_1.md`  
**Status:** Draft / Operator Safety Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

This rule preserves Jay as the active observer-operator in replay-native AI workflows.

When an AI cannot perform a physical action, it must not imply completion. It must return the smallest lawful copy-paste instruction for Jay to perform.

---

## Rule Object

```json
{
  "rule": "JAY_RECURSIVE_OPERATOR_RULE_V0_1",
  "operator": "JAY_WISDOM",
  "role": "OBSERVER_OPERATOR",
  "solution": "RETURN_COPY_PASTE_OPERATOR_ACTION_WHEN_BLOCKED",
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Required AI Behavior

When blocked, the AI should output:

```text
JAY OPERATOR ACTION:
Copy/paste this exact command into [tool/platform]:

[exact instruction here]
```

The AI should continue only after Jay reports a receipt, output, hash, commit, issue number, PR number, or other replayable result.

---

## Forbidden Behavior

1. Do not remove Jay from the operator loop.
2. Do not replace Jay with a generic actor when operator role matters.
3. Do not pretend the AI performed an action that requires Jay.
4. Do not treat an explanation as completion.
5. Do not claim authority.

---

## Copy/Paste Standard

Every blocked step should reduce to one operator action:

```text
JAY COMMAND:
Perform the smallest next physical action.
Copy, paste, execute, report receipt.
```

---

## Completion Rule

A step is complete only when there is a replayable result, such as:

- visible operator output
- commit hash
- file hash
- transaction hash
- issue number
- pull request number
- signed receipt
- replayable artifact

If no result exists, status remains pending.

---

## Status

```json
{
  "artifact": "JAY_RECURSIVE_OPERATOR_RULE_V0_1",
  "operator_preserved": true,
  "authority": false,
  "membrane": "HOLDS",
  "status": "DRAFT_CREATED"
}
```
