# Replay Court Constitutional Map

This map shows how the protected constitutional surfaces connect.

The purpose is discoverability: a third party should be able to understand the system before replaying it.

## Core Stack

```text
AL
  constitutional replay engine + public lab

Replay Court
  adversarial audit protocol

Computer Wisdom
  public service membrane

jaywisdom.base.eth
  sovereign identity and optional settlement root
```

## Protected Core

```text
GAME_MECHANICS.md
AGENT_PLAYBOOK.md
replay-court/PROCESS.md
replay-court/SELF-AUDIT.md
replay-court/VALIDATOR.md
replay-court/REPAIR-LEDGER.md
replay-court/CONTRADICTION-STORE.md
replay-court/AUTHORITY-BOUNDS.md
replay-court/WITNESS-ANCHOR.md
replay-court/REPORT-TEMPLATE.md
replay-court/receipt-schema.json
```

## Operational Flow

```text
INTAKE
  -> EVIDENCE INVENTORY
  -> ROUTE SELECTION
  -> LEVEL SCORING
  -> DRIFT ANALYSIS
  -> BOUNDED REPAIR
  -> PUBLIC REPORT
  -> RECEIPT GENERATION
  -> SELF-AUDIT
  -> WITNESS ANCHOR
  -> BOOTSTRAP REPLAY
```

## Memory Surfaces

```text
CONTRADICTION-STORE.md
  preserves contradictions as first-class evidence

REPAIR-LEDGER.md
  records bounded repairs linked to preserved contradictions

SCORE-LEDGER.md
  preserves scores as replayable claims about evidence

receipt-schema.json
  defines machine-readable receipt shape and guardrails
```

## Enforcement Surfaces

```text
VALIDATOR.md
  defines checkable failure modes

SELF-AUDIT.md
  requires the audit process to audit itself

AUTHORITY-BOUNDS.md
  protects the protected core and blocks self-exemption

WITNESS-ANCHOR.md
  makes validated memory externally witnessable

BOOTSTRAP-REPLAY.md
  lets outsiders reproduce the chain from public evidence
```

## Dependency Graph

```text
Contradiction Store
        ↓
Repair Ledger
        ↓
Score Ledger
        ↓
Report Template
        ↓
Validator
        ↓
Self-Audit
        ↓
Authority Bounds
        ↓
Witness Anchor
        ↓
Bootstrap Replay
```

## Doctrine Flow

```text
Truth -> Readiness -> Closure
```

Truth layer:

```text
receipts
artifacts
contradictions
repairs
scores
validator outputs
```

Readiness layer:

```text
self-audit
authority bounds
witness anchors
bootstrap replay
```

Closure layer:

```text
public report
optional tip
optional future x402 settlement
```

Closure does not flow upstream.
Payment does not create truth.
Settlement does not erase contradiction.

## Issue #228 Precedent

```text
contradiction:
  RECEIPT_CONFIRMED + status: failure

repair:
  separate verifier_verdict from recorded_outcome_status

post-repair:
  RECEIPT_CONFIRMED
  verifier_verdict: confirmed
  recorded_outcome_status: failure

result:
  historical failure preserved
  verifier contract clarified
  public replay restored score to 100
```

## Invariants

```text
No witness, no claim.
No receipt, no ratification.
No replay, no legitimacy.
No preserved contradiction, no legitimate repair.
No score without evidence.
No self-exemption.
If the rules cannot be checked, authority cannot be claimed.
If constitutional memory cannot be externally witnessed, authority remains local and limited.
```

## Purpose

Replay Court exists to test whether machine and institutional reasoning can survive adversarial replay without corrupting the record.
