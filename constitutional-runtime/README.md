# constitutional-runtime

Minimal deterministic replay + divergence engine for constitutional membrane verification.

## Verified Controls

- **Positive control** — `fixtures/receipt.valid.json` (genesis MATCH, empty replay path)
- **Negative control** — `fixtures/receipt.divergent.json` (D3 divergence, deterministic mismatch)
- **Contradiction control** — `fixtures/contradiction.valid.json` (multi-observer CONSTITUTIONAL_CONTRADICTION)
- **Revoked observer control** — `fixtures/contradiction.revoked-observer.json` (claim rejected after observer activity filtering)
- **Lineage control** — `fixtures/lineage.valid.json`
- **Schema surface** — `schema/*.schema.json` (strict, no additionalProperties)

## Verified Constitutional Controls

| Control | Fixture | Claimed Verdict | Evaluated Verdict | Active Observers | Divergence | Mutation Surface | Exit Code |
|---------|---------|-----------------|-------------------|------------------|------------|------------------|-----------|
| Genesis Positive | `receipt.valid.json` | `MATCH` | `MATCH` | — | `D0` | Mutable/Frozen | 0 |
| Replay Divergence | `receipt.divergent.json` | `DIVERGENCE` | `DIVERGENCE` | — | `D3` | Frozen | 2 |
| Observer Contradiction | `contradiction.valid.json` | `CONSTITUTIONAL_CONTRADICTION` | `CONSTITUTIONAL_CONTRADICTION` | >=2 | `D3` | Frozen | 2 |
| Revoked Observer Negative | `contradiction.revoked-observer.json` | `CONSTITUTIONAL_CONTRADICTION` | `INSUFFICIENT_EVIDENCE` | 1 | `D0` | Frozen | 4 |

## CLI Contract

```bash
node dist/cli.js <receipt.json> <lineage.json>
```

## Exit Codes

- `0` → MATCH
- `2` → DIVERGENCE / CONSTITUTIONAL_CONTRADICTION
- `4` → UNKNOWN / INSUFFICIENT_EVIDENCE

## Reproduction

```bash
chmod +x reproduce.sh
./reproduce.sh
```

This script:

- Builds from source
- Validates positive control (exit 0)
- Validates divergent control (exit 2)
- Validates contradiction control with lineage binding (exit 2)
- Validates revoked-observer negative control (exit 4)
- Fails hard on any drift

## Contradiction Control (with lineage binding)

Observer disagreement is now bound to specific replay context:

- `lineage_tip` (required) — anchors contradiction to a concrete tip/root
- `replay_path` (optional) — preserves genesis/empty-path compatibility
- Enforced structurally: **No contradiction without lineage context**

A contradiction receipt records multiple observer reports for the same event where observers report conflicting state roots. In v0.1, any exact root conflict from enough active observers is treated as D3 and freezes the mutation surface.

## Observer Activity Rules

Observer activity is enforced at evaluation time:

- Only `ACTIVE` observers whose `lineage_tip` matches the receipt contribute evidence
- `REVOKED` observers are filtered out and treated as non-evidence
- Contradiction requires at least 2 active observers with conflicting `observed_state_root` values
- Receipts describe claims; the validator determines legitimacy

Negative control: `contradiction.revoked-observer.json` claims `CONSTITUTIONAL_CONTRADICTION`, but contains only 1 active observer after filtering. The validator returns `INSUFFICIENT_EVIDENCE` with exit code 4.

This layer is intentionally narrow:

- No fuzzy consensus
- No weighted observers
- No settlement logic
- No quorum mutation
- Duplicate observer reports do not inflate agreement

## Design Principles

- Replay is authoritative — receipts are only claims
- Schemas precede semantics
- Declared topology does not equal verified topology until commits land
- Divergence classification is intentionally conservative (D0 vs D3)
- Contradiction is evidence, not adjudication

## Status

Branch: `constitutional-runtime-observer-attestation-lineage`

Membrane: structurally self-describing + externally reproducible
