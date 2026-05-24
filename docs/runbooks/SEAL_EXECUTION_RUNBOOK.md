# 3-Green Seal Execution Runbook

## Status
| Item | Value |
|------|-------|
| Seal model | `HUMAN_GATED_REPLAYABLE_CEREMONY` |
| Repository | `jsonwisdom/AL` |
| Branch | `master` |
| Environment gate | `three-green-seal` |
| Current state | `READY_PENDING_ENVIRONMENT_CONFIGURATION` |

---

## Required Before Execution

### 1. Configure GitHub Environment

- **Go to:** `https://github.com/jsonwisdom/AL/settings/environments`
- **Create or open:** `three-green-seal`
- **Enable:** Required reviewers
- **Add:** At least 2 trusted reviewers
- **Optional:** 5-minute wait timer

### 2. Run Preflight Verification

```bash
cd AL
./scripts/preflight_3_green_seal.sh
```

Expected result:

```text
🟢 PRE-FLIGHT PASSED — All checks successful
```

If preflight fails → DO NOT PROCEED

---

## Execution

| Step | Action |
|------|--------|
| 1 | Trigger upstream Verifier Heartbeat workflow on branch `master` |
| 2 | Wait for Heartbeat Transition workflow to start automatically |
| 3 | Confirm it pauses at environment gate: `three-green-seal` |
| 4 | Required reviewers approve in GitHub Actions UI |
| 5 | Workflow resumes → commits/pushes milestone root |

---

## Post-Seal Verification

After workflow completes:

```bash
cd AL
git pull
./scripts/post_seal_verify_3_green.sh
```

Expected result:

```text
🟢 POST-SEAL VERIFICATION PASSED
3_GREEN_MILESTONE root is present, formatted, and root remains clean.
```

---

## Stop Conditions

Do NOT approve the environment gate if:

- ❌ Preflight failed
- ❌ `three-green-seal` has no required reviewers configured
- ❌ `_truth/governance/CEREMONY_COURT_RULES_V1.json` reappears
- ❌ Workflow does not pause for approval
- ❌ Branch is not `master`
- ❌ Unexpected files are staged or committed

---

## Receipt Chain

| Receipt ID | Artifact |
|------------|----------|
| `HEARTBEAT_TRANSITION_APPROVAL_GATE_001` | Workflow approval gate |
| `PREFLIGHT_SCRIPT_001_COMMIT` | Preflight script |
| `POST_SEAL_VERIFICATION_001_COMMIT` | Post-seal script |

---

## Final Rule

No seal without preflight.  
No push without human gate.  
No milestone without post-seal verification.

---

## Current Status

```json
{
  "seal_state": "READY_FOR_HUMAN_GATED_EXECUTION",
  "remaining_step": "configure three-green-seal environment"
}
```
