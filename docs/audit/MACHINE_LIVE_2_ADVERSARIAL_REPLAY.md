# Machine LIVE 2.0 — Adversarial Replay

Do not trust the post. Replay the machine.

## Claim

Machine LIVE 2.0 recomputes ALMS state fixtures into a national root and preserves honest `INDETERMINATE` verdicts instead of forcing false `PASS` results.

Expected root:

```text
sha256:272bd90e5b2682c75ab07a49c4491929f39280a2d391ab6742a421e844852105
```

Expected verdicts:

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
- Output: `alms/national/national_root_ci_latest.json`

## Replay

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
git checkout 18af5459899b12ed609b9098aed1b6ec43ebfc13
python3 scripts/compute_national_root_ci.py
```

## Pass Condition

Replay passes only if:

1. `national_root` equals the expected root.
2. Verdicts remain `MN=PASS`, `AL/TX/National=INDETERMINATE`.
3. No on-chain, Base/EAS, or ENS claim is introduced.

## Valid Breaks

A valid break is reproducible proof that:

1. Same commit + same fixtures produce a different root.
2. A verdict changes without script or fixture changes.
3. A `PASS` state has a source hash mismatch.
4. An `INDETERMINATE` state has a complete matching source chain.
5. The receipt overclaims Base/EAS, ENS, or on-chain status.
6. The committed receipt does not match generated output.

## Not Breaks

These do not break the replay claim:

- Disagreement with the fiscal or political meaning of a state budget.
- Treating `INDETERMINATE` as `FAIL`.
- Newer commits changing outputs after code or fixtures change.
- Expecting Base/EAS, ENS, or wallet anchoring from this receipt.

## Boundary

GitHub Direct replay proof only.

No Base/EAS claim.  
No ENS claim.  
No on-chain claim.  
No national `PASS` claimed.

Same script + same fixtures = same verdict.

**Receipts > vibes.**
