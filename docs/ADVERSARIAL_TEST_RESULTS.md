# ALMS / Goblin Court Adversarial Test Results

## Status

VERIFIED

## Canonical Public State

- Merkle Root: `79e8494155d1e7c8e8f0c7e91c4e7a4e8f721f12a3a9424daade934790086a58`
- Leaf Count: `4`
- Leaves: `leaf008` through `leaf011`
- Public Index: `site/merkle/index.json`
- Browser Verifier: `site/verify/index.html`
- CLI Verifier: `scripts/verifiers/verify_merkle_proof.py`

## Invariant Under Test

Only canonical UPHELD court verdict files may feed the Merkle tree.

Allowed source:

```text
_truth/courts/leaf*/verdict_*.canonical.json
```
