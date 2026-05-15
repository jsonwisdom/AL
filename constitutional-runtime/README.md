# constitutional-runtime

Minimal deterministic replay + divergence engine for constitutional membrane verification.

## Verified Controls

- **Positive control** — `fixtures/receipt.valid.json` (genesis MATCH, empty replay path)
- **Negative control** — `fixtures/receipt.divergent.json` (D3 divergence, deterministic mismatch)
- **Contradiction control** — `fixtures/contradiction.valid.json` (multi-observer CONSTITUTIONAL_CONTRADICTION)
- **Lineage control** — `fixtures/lineage.valid.json`
- **Schema surface** — `schema/*.schema.json` (strict, no additionalProperties)

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
- Validates contradiction control (exit 2)
- Fails hard on any drift

## Contradiction Receipts

Observer disagreement is constitutional state, not hidden operator context.

A contradiction receipt records multiple observer reports for the same event where observers report conflicting state roots. In v0.1, any exact root conflict is treated as D3 and freezes the mutation surface.

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

Branch: `constitutional-runtime-observer-reports`

Membrane: structurally self-describing + externally reproducible
