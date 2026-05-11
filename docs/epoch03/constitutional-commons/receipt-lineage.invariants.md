# Epoch03 Receipt Lineage Invariants

## Purpose

Receipt lineage invariants prevent constitutional ancestry from being silently forked, rewritten, or forgotten across future epochs.

A receipt is evidence, not authority.
A receipt is legitimate only when its ancestry matches recomputed doctrine, FSM, validator, and receipt-root surfaces.

## Core Invariant

```text
cryptographic correctness != constitutional legitimacy
```

A receipt may be structurally valid and hash-consistent while still being constitutionally illegitimate.

## Required Lineage Fields

Every epoch receipt lineage object MUST include:

```json
{
  "lineage_id": "epoch03-lineage",
  "epoch": "epoch03",
  "parent_epoch": null,
  "doctrine_hash": "sha256:<hex>",
  "fsm_hash": "sha256:<hex>",
  "validator_hash": "sha256:<hex>",
  "receipt_root": "sha256:<hex>",
  "adversarial_ledger_root": "sha256:<hex>",
  "created_at_utc": "ISO-8601",
  "status": "ACTIVE"
}
```

## Invariants

### L-0: Recomputed Surface Match

A lineage receipt is lawful only if:

- `doctrine_hash` equals the browser/CLI recomputed doctrine hash
- `fsm_hash` equals the browser/CLI recomputed FSM hash
- `validator_hash` equals the recomputed validator hash
- `receipt_root` reconstructs from declared receipt leaves

Failure state:

```text
TAINTED_LINEAGE_SURFACE_MISMATCH
```

### L-1: No Silent Doctrine Fork

A future epoch MAY change doctrine only by explicit versioned successor receipt.

A doctrine hash change without an explicit successor link is a fork.

Failure state:

```text
REFUSED_LINEAGE_FORK
```

### L-2: No Silent FSM Fork

A future epoch MAY change FSM topology only by explicit versioned successor receipt.

An FSM hash change without an explicit successor link is a fork.

Failure state:

```text
REFUSED_TOPOLOGY_FORK
```

### L-3: No Validator Drift

A validator implementation change MUST preserve bit-identical verdicts for unchanged doctrine, FSM, and transcript inputs.

If verdict parity fails, the lineage is tainted.

Failure state:

```text
TAINTED_VALIDATOR_DRIFT
```

### L-4: No Fixture Deletion

Adversarial fixtures MAY NOT be deleted from lineage history.

They may only be superseded by explicit successor fixtures that preserve the original fixture hash.

Failure state:

```text
REFUSED_ADVERSARIAL_FORGETTING
```

### L-5: Cross-Epoch Refusal Preservation

A fixture REJECTED in epoch N MUST remain REJECTED in epoch N+1 unless the doctrine clause it probes is explicitly deprecated by successor receipt.

Failure state:

```text
REFUSED_CROSS_EPOCH_AMNESIA
```

### L-6: No Counterfeit Authority

A receipt with internally valid hashes but externally mismatched lineage roots is not legitimate.

Failure state:

```text
REFUSED_COUNTERFEIT_AUTHORITY
```

### L-7: Browser Is Witness Only

The browser MAY recompute, compare, and refuse.

The browser MUST NOT author doctrine, FSM, lineage, validator identity, or receipt ancestry.

Failure state:

```text
REFUSED_BROWSER_AUTHORITY_ESCALATION
```

## Replay Rule

A lineage replay is lawful iff:

1. all lineage hashes recompute locally
2. all successor links are explicit
3. all historical hostile fixtures remain present or superseded
4. unchanged hostile fixtures retain bit-identical refusal outcomes
5. no receipt root is accepted without ancestry match

Otherwise:

```text
TAINTED
```

No partial legitimacy.
No interpretive override.
No silent fork acceptance.

## Canonical Compression

```text
Authority cannot be forged.
Lineage cannot be forked silently.
History cannot be forgotten.
The browser witnesses; it does not notarize.
```
