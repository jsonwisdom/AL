# Machine LIVE 2.0 — Adversarial Replay Guide

This guide exists so reviewers can test the Machine LIVE 2.0 claim without trusting the author.

The standard is simple:

> Do not trust the post. Replay the machine.

## Claim Under Test

Machine LIVE 2.0 recomputes state-level ALMS fixture claims into a national root hash while preserving honest `INDETERMINATE` verdicts instead of forcing false `PASS` results.

Expected national root:

```text
sha256:272bd90e5b2682c75ab07a49c4491929f39280a2d391ab6742a421e844852105
```

Expected verdicts:

- Minnesota: `PASS`
- Alabama: `INDETERMINATE`
- Texas: `INDETERMINATE`
- National: `INDETERMINATE`

## Receipt Surface

- Repo: `jsonwisdom/AL`
- Commit: `18af5459899b12ed609b9098aed1b6ec43ebfc13`
- Script: `scripts/compute_national_root_ci.py`
- Receipt: `alms/anchors/runtime/github_direct_anchor_state.json`
- National output: `alms/national/national_root_ci_latest.json`

## Replay Commands

Run from a clean shell:

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
git checkout 18af5459899b12ed609b9098aed1b6ec43ebfc13
python3 scripts/compute_national_root_ci.py
```

## Pass Condition

The replay passes if the emitted `national_root` equals:

```text
sha256:272bd90e5b2682c75ab07a49c4491929f39280a2d391ab6742a421e844852105
```

and the verdicts remain:

```text
MN=PASS
AL=INDETERMINATE
TX=INDETERMINATE
National=INDETERMINATE
```

## What Counts as a Valid Break

A valid break is any reproducible demonstration that one of the following is true:

1. The same commit and same fixtures produce a different national root.
2. A verdict changes without fixture or script changes.
3. A state marked `PASS` has a source hash mismatch.
4. A state marked `INDETERMINATE` has a complete matching source chain.
5. The receipt claims Base/EAS, ENS, or on-chain anchoring without a matching transaction receipt.
6. The committed receipt does not match the script output generated from the named commit.

## What Does Not Count as a Break

The following are not valid breaks by themselves:

- A disagreement with the political or fiscal meaning of a state budget.
- A claim that `INDETERMINATE` should mean `FAIL`.
- A newer commit producing a different result after fixtures or scripts changed.
- An on-chain anchor expectation. This receipt does not claim Base/EAS, ENS, or wallet anchoring.

## Boundary

This is GitHub Direct replay proof only.

No Base/EAS claim.  
No ENS claim.  
No on-chain claim.  
No national `PASS` claimed.

Same script + same fixtures = same verdict.

**Receipts > vibes.**
