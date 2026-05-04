# Meme Court Charge System

Status: DESIGN SPEC — INTERNAL GOBLIN QUEST AUDIT

## Purpose

Meme Court turns ALMS verification failures into playable civic audit lessons.

The joke is never the Constitution. The joke is fake certainty, skipped proof, ghost roots, smart quote drift, and unverifiable claims.

## Core Rule

```text
No receipt, no mercy.
```

## Operator Layer

Operator: Jay Wisdom

Display identity:

```text
jaywisdom.base → jaywisdom.eth
```

Jay Wisdom routes attention to proof. ALMS decides the verdict.

## ALMS Machine Speed Stages

Stages are monotonic. A case cannot skip forward.

```text
CAPTURE → HASH → COMMIT → FETCH → REPLAY → PUBLISH → CHAIN_CONFIRM
```

A stage is admissible only if the prior stage has a receipt.

## Verdict Colors

| Color | Meaning |
|---|---|
| GREEN | proof passes |
| YELLOW | degraded / pending / incomplete evidence |
| RED | mismatch or invalid claim |
| GRAY | unavailable / indeterminate |

## Charges

### GHOST_PROMOTION

Claiming a higher state than the receipts prove.

Examples:

- calling a root LOCKED before remote fetch
- calling a manifest verified before replay
- calling a Base event confirmed before chain evidence

Sentence:

```text
Return to last verified stage.
```

### NORMALIZATION_TREASON

Mutating canonical bytes for readability or convenience.

Examples:

- good Behaviour → good Behavior
- supreme Court → Supreme Court
- Affirmation:--" → Affirmation: — “

Sentence:

```text
Quarantine mutated span and replay canonical bytes.
```

### IDENTITY_DRIFT

Using a display identity without binding it to the canonical ENS root.

Examples:

- displaying jaywisdom.base without resolving to jaywisdom.eth in receipts
- treating a social name as proof of authority

Sentence:

```text
Bind display identity to jaywisdom.eth or mark identity UNVERIFIED.
```

### FAKE_CHAIN_CONFIRM

Claiming Base/Zora chain confirmation without a valid tx, UID, or explorer-backed receipt.

Examples:

- tx hash used as contract address
- Zora post treated as proof
- Base attestation UID declared verified before fetch

Sentence:

```text
Downgrade to PENDING_CHAIN_CONFIRMATION.
```

### HASH_THEATER

Using hashes that were not generated from the stated bytes.

Examples:

- zero-padded SHA-256 values
- reused roots from memory
- placeholder JSONL labeled OK

Sentence:

```text
Purge audit, recompute from repo bytes, and fetch remote proof.
```

### SKIPPED_REPLAY

Publishing or aggregating before replay confirmation.

Examples:

- manifest exists but status is still PENDING_REPLAY
- aggregate root built from stale manifest state

Sentence:

```text
Run replay and update status only after match.
```

## Case File Format

```json
{
  "artifact": "MEME_COURT_CASE",
  "case_id": "MC-0001",
  "operator": "Jay Wisdom",
  "identity": "jaywisdom.base -> jaywisdom.eth",
  "charge": "NORMALIZATION_TREASON",
  "machine_speed_stage": "FETCH",
  "claim": "good Behavior is acceptable spelling",
  "evidence_path": "_truth/us/constitution/a3_s1_c1_span.txt",
  "expected": "good Behaviour",
  "observed": "good Behavior",
  "verdict": "GUILTY",
  "root_status": "GREEN_AFTER_REPLAY"
}
```

## Badge System

| Badge | Unlock Condition |
|---|---|
| Goblin Bonker I | convict first drift case |
| Root Keeper | verify federal root |
| Receipt Clerk | build first receipt from bytes |
| No Ghost Promotion | correctly block premature status upgrade |
| Chain Clean | complete CAPTURE through REPLAY without miss |
| Constitutional Operator | complete Article III Drift Lab |

## Zora Caption Template

```text
Meme Court Case: <CASE_ID>

Charge: <CHARGE>
Verdict: <VERDICT>
Stage: <MACHINE_SPEED_STAGE>
Operator: Jay Wisdom
Identity: jaywisdom.base → jaywisdom.eth
Root: <short_root>
Receipt: <receipt_path>
Verify: <url>

No Receipt. No Mercy. 🧌⚖️🧾
```

## Final Rule

Meme Court is a teaching layer, not a trust boundary.

ALMS receipts decide truth.

Proof > narrative.
