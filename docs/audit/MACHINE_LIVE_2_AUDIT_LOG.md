# Machine LIVE 2.0 — Public Audit Log

Running public log of replay attempts, confirmations, breaks, and fixes for Machine LIVE 2.0.

## Active Claim

Machine LIVE 2.0 is GitHub Direct replay proof.

It recomputes ALMS state fixtures into a national root while preserving honest `INDETERMINATE` states.

Root:

```text
sha256:272bd90e5b2682c75ab07a49c4491929f39280a2d391ab6742a421e844852105
```

Verdicts:

```text
MN=PASS
AL=INDETERMINATE
TX=INDETERMINATE
National=INDETERMINATE
```

## Receipt Surface

- Repo: `jsonwisdom/AL`
- Commit: `18af5459899b12ed609b9098aed1b6ec43ebfc13`
- Script: `scripts/compute_national_root_ci.py`
- Receipt: `alms/anchors/runtime/github_direct_anchor_state.json`
- Replay guide: `docs/audit/MACHINE_LIVE_2_ADVERSARIAL_REPLAY.md`

## Audit Entries

| Date | Reviewer | Commit | Result | Notes |
|---|---|---|---|---|
| 2026-05-03 | jsonwisdom | `18af5459899b12ed609b9098aed1b6ec43ebfc13` | `BASELINE` | Initial launch receipt. GitHub Direct only. No Base/EAS, ENS, on-chain, or national `PASS` claim. |

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
