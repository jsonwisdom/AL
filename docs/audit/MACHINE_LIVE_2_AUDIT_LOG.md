# Machine LIVE 2.0 — Public Audit Log

Running public log of replay attempts, confirmations, breaks, and fixes for Machine LIVE 2.0.

## Active Claim

Machine LIVE 2.0 is GitHub Direct replay proof.

It recomputes ALMS state fixtures into a national root while preserving honest `INDETERMINATE` states.

Current verdicts:

```text
MN=PASS
AL=PASS
TX=INDETERMINATE
National=INDETERMINATE
```

Boundary:

```text
GitHub CI recompute only. Not Base/EAS anchored. National PASS requires every state PASS.
```

## Receipt Surface

- Repo: `jsonwisdom/AL`
- Script: `scripts/compute_national_root_ci.py`
- Receipt: `alms/anchors/runtime/github_direct_anchor_state.json`
- Replay guide: `docs/audit/MACHINE_LIVE_2_ADVERSARIAL_REPLAY.md`

## Audit Entries

| Date | Reviewer | Commit | Result | Notes |
|---|---|---|---|---|
| 2026-05-03 | jsonwisdom | `18af5459899b12ed609b9098aed1b6ec43ebfc13` | `BASELINE` | Initial launch receipt. GitHub Direct only. MN `PASS`; AL/TX/National `INDETERMINATE`. No Base/EAS, ENS, on-chain, or national `PASS` claim. |
| 2026-05-03 | jsonwisdom | `970fa505` | `CONFIRMED` | AL official Act 2025-251 PDF frozen and replayed. MN `PASS`; AL `PASS`; TX `INDETERMINATE`; National `INDETERMINATE`. |

## Entry Standard

To contribute an audit entry:

1. Run the adversarial replay guide.
2. Record the commit tested.
3. Record the root and verdicts observed.
4. Open a PR adding one row to this table.

Valid results:

- `CONFIRMED`
- `BREAK_REPORTED`
- `BREAK_REJECTED`
- `FIXED`
- `BASELINE`

**Receipts > vibes.**
