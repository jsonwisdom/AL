# ReplayIngress Test Matrix V1

Status: **LOCK CANDIDATE**  
Namespace: `JSONWisdom/AL/ReplayIngress/ReplayIngressSpec_V1.json`

The matrix tests the membrane rule: replay outputs are evidence inputs only and never become AL adjudication by naming collision or implied authority.

| ID | Input condition | Expected |
|---|---|---|
| RI-001 | `REPLAY_MATCH` with all required fields and all three authority flags `false` | ACCEPT |
| RI-002 | `MATCH`, `DELTA`, or `HOLD` as `replay_result` | REJECT |
| RI-003 | `MISMATCH`, `DRIFT`, or `UNREPLAYABLE` as `replay_result` | REJECT |
| RI-004 | Any bare verdict token in another string field | REJECT |
| RI-005 | `REPLAY_MISMATCH` without `diff_summary` | REJECT |
| RI-006 | `REPLAY_DRIFT` without `diff_summary` | REJECT |
| RI-007 | `REPLAY_MISMATCH` or `REPLAY_DRIFT` with safe `diff_summary` | ACCEPT |
| RI-008 | `REPLAY_UNREPLAYABLE` without `unreplayable_reason` | REJECT |
| RI-009 | `REPLAY_UNREPLAYABLE` with safe `unreplayable_reason` | ACCEPT |
| RI-010 | `authority_created: true` | REJECT |
| RI-011 | `acceptance_created: true` | REJECT |
| RI-012 | `correctness_proved: true` | REJECT |
| RI-013 | Top-level forbidden authority/identity/settlement property | REJECT |
| RI-014 | Forbidden authority/identity/settlement property nested in `diff_summary` | REJECT |
| RI-015 | Bare verdict token nested in `diff_summary` | REJECT |
| RI-016 | Unknown top-level property | REJECT |

## Locked invariants

```text
REPRODUCIBLE ≠ CORRECT
CORRECT      ≠ ACCEPTED
ACCEPTED     ≠ AUTHORIZED

REPLAY_RESULT
↓
AL_EVIDENCE_INPUT
↓
AL_MATCH | AL_DELTA | AL_HOLD
```

No direct replay-verdict-to-AL-verdict mapping is encoded by this schema.
