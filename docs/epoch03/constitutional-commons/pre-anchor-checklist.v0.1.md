# Epoch03 Pre-Anchor Checklist v0.1

## Purpose

This checklist MUST be completed before any EAS/Base attestation is minted for Epoch03.

The attestation anchors lineage state, not UI content.
No on-chain action is valid until the roots below are reproducible from a fresh clone.

## Required Freeze

Freeze these files before computing `harness_hash`:

```text
docs/epoch03/adversarial/harness.js
docs/epoch03/adversarial/lineage-harness.js
docs/epoch03/constitutional-commons/receipt-lineage.invariants.md
```

`harness_hash` MUST be computed using:

```text
docs/epoch03/constitutional-commons/canonical-concat.v0.1.md
```

## Required Parity Pass

For the attested commit:

```text
JS engine verdicts   = PASS
WASM engine verdicts = PASS
CLI/Rust verdicts    = PASS
```

The verdict JSONs MUST be bit-identical after canonicalization.

If any verdict differs:

```text
REFUSED_PARITY_DIVERGENCE
```

## Required Roots

Using frozen code and canonical surfaces, compute:

```text
doctrine_root
fsm_root
receipt_root
lineage_root
harness_hash
```

Each root MUST be reproducible from a fresh clone at the attested commit.

## Attestation Payload Boundary

The EAS/Base payload MUST include only constitutional roots and commit identity:

```json
{
  "project": "jsonwisdom/AL",
  "epoch": "epoch03",
  "lineage_root": "sha256:<hex>",
  "doctrine_root": "sha256:<hex>",
  "fsm_root": "sha256:<hex>",
  "validator_version": "epoch03-validator-rust@0.1.0",
  "engine_contract_version": "engine@1",
  "receipt_root": "sha256:<hex>",
  "taxonomy_version": "adversarial.taxonomy@1",
  "fixtures_survived": 10,
  "classes_covered": 10,
  "authors": 7,
  "harness_hash": "sha256:<hex>",
  "repo_ref": "https://github.com/jsonwisdom/AL/tree/<commit>",
  "commit": "<git-sha>",
  "timestamp": 0
}
```

No UI hashes.
No screenshots.
No decorative metadata.
No unverifiable claims.

## Verification Rule

Anyone must be able to:

1. clone `jsonwisdom/AL` at `<git-sha>`
2. recompute the five roots
3. rerun validator, adversarial harness, and lineage harness
4. compare to the EAS/Base payload

If all values match, the chain record is a dated receipt of a replayable constitutional state.

If any value differs:

```text
TAINTED_PRE_ANCHOR_STATE
```

## Current Status

```text
EAS_BASE_ATTESTATION = NOT_MINTED
ANCHOR_STATUS = PRE_ANCHOR_CHECKLIST_ONLY
```
