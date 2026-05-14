# constitutional-runtime

Minimal deterministic replay + divergence engine for constitutional membrane verification.

## Verified Controls

- **Positive control** — `fixtures/receipt.valid.json` (genesis MATCH, empty replay path)
- **Negative control** — `fixtures/receipt.divergent.json` (D3 divergence, deterministic mismatch)
- **Lineage control** — `fixtures/lineage.valid.json`
- **Schema surface** — `schema/*.schema.json` (strict, no additionalProperties)

## CLI Contract

```bash
node dist/cli.js <receipt.json> <lineage.json>
```

## Exit Codes

- `0` → MATCH
- `2` → DIVERGENCE
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
- Fails hard on any drift

## Design Principles

- Replay is authoritative — receipts are only claims
- Schemas precede semantics
- Declared topology does not equal verified topology until commits land
- Divergence classification is intentionally conservative (D0 vs D3)

## Status

Branch: `constitutional-runtime-v0-1`

Membrane: structurally self-describing + externally reproducible
