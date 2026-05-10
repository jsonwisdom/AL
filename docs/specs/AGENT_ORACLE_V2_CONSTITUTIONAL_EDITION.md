# Agent Oracle v2 — Constitutional Edition

Status: SPEC_DRAFT_V2
Root identity: jaywisdom.base
Applies to: multi-agent dashboards, worker bee orchestration, learning lab assistants, witness streams, and receipt-bound AI outputs.

## Verdict

A classic AI swarm is not a constitutional machine.

A constitutional machine requires receipts, replay, challenge windows, provenance, and root law binding.

## Root Law Binding

```text
constitutional_root: jaywisdom.base
machine_law: Family before Economy; School before Market; Repair before Punishment; Replay before Authority
```

AI workers may prepare.
AI workers may not rule.

## Role Renaming

```text
Oracle -> Coordinator Bee
Researcher -> Scout Bee
Analyst -> Pattern Bee
Builder -> Builder Bee
Critic -> Auditor Bee
```

These are worker bees, not sovereign agents.

## Worker Bee Boundary

Worker bees may:

- observe
- draft
- compute
- compare
- route receipts
- flag uncertainty
- propose synthesis
- request replay

Worker bees may not:

- define final truth unilaterally
- silently rewrite outputs
- bypass human acceptance
- erase challenge windows
- create permanent user or worker scores
- hide model lineage
- promote confidence without evidence

## Receipt First Rule

Every worker bee message must emit a receipt.

A valid WorkerBeeMessageReceipt includes:

```json
{
  "type": "WorkerBeeMessageReceipt",
  "root_identity": "jaywisdom.base",
  "constitutional_root_uid": "bytes32_or_pending",
  "session_id": "string",
  "message_id": "string",
  "bee_role": "ScoutBee|PatternBee|BuilderBee|AuditorBee|CoordinatorBee",
  "model_lineage": {
    "provider": "string",
    "model": "string",
    "model_version": "string_or_unknown",
    "temperature": "number_or_null",
    "tooling": ["string"]
  },
  "input_hash": "bytes32",
  "output_hash": "bytes32",
  "previous_receipt_hash": "bytes32_or_zero",
  "confidence_bounds": {
    "state": "SPECULATIVE|EXTERNAL_PENDING|REPLAYED|CHALLENGED|SETTLED",
    "restraint_flags": ["UNVERIFIED_SOURCE", "MODEL_LIMITATION", "NEEDS_HUMAN_REVIEW"]
  },
  "created_at": "iso8601",
  "challenge_window_ends_at": "iso8601",
  "receipt_hash": "bytes32"
}
```

## Oracle Downgrade

The Oracle must not be a judge.

Coordinator Bee may:

- plan
- dispatch
- collect receipts
- link claims
- propose synthesis

Coordinator Bee may not:

- publish final truth
- override an Auditor Bee challenge
- mark a synthesis settled without human acceptance or replay

## Synthesis Proposal Receipt

The final answer is not final truth. It is a proposal.

```json
{
  "type": "SynthesisProposalReceipt",
  "root_identity": "jaywisdom.base",
  "source_receipt_hashes": ["bytes32", "bytes32"],
  "proposal_hash": "bytes32",
  "coordinator_bee": "CoordinatorBee",
  "status": "PENDING_HUMAN_DECISION",
  "allowed_actions": ["ACCEPT", "CHALLENGE", "REQUEST_REPLAY"],
  "challenge_window_ends_at": "iso8601",
  "receipt_hash": "bytes32"
}
```

## Required Dashboard Views

### 1. Witness Stream

Formerly: Chat.

Every message bubble must show:

- bee role
- model lineage
- restraint flags
- receipt hash
- verify button
- challenge button

### 2. Architecture

Add these required states:

```text
01 ROOT_LAW
02 DISPATCH
03 WORKER_BEE_RECEIPT
04 SYNTHESIS_PROPOSAL
05 HUMAN_DECISION
06 CHALLENGE_WINDOW
07 COMMUNITY_VERIFICATION
08 SETTLEMENT
09 EXPORT_FOR_ANCHOR
```

### 3. Immutable Receipt Log

Formerly: Log.

Must include:

- local receipt store
- hash chain
- export JSON
- replay status
- open challenges
- settled repairs

## Replay Before Authority

A Verify This Answer button must:

- recompute every receipt hash
- show green/red proof state
- list missing provenance
- show unresolved challenges
- allow single-bee replay request
- compare new output hash against original output hash

## No Performance Score

Forbidden:

- agent performance rating
- hidden leaderboard
- permanent trust score
- engagement score
- donor-weighted verdicts

Allowed:

- receipts produced today
- repairs honored
- challenges open
- role cooldowns
- settled receipt count

## Local-First Storage

The first prototype should use browser storage before chain anchoring.

Recommended:

```text
IndexedDB object stores:
- sessions
- receipts
- messages
- challenges
- replays
- exports
```

No chain write until receipt export passes local replay.

## Export for MigrationGuard

The dashboard may export receipt bundles for later anchoring/migration.

Export format:

```json
{
  "type": "AgentOracleV2ReceiptBundle",
  "root_identity": "jaywisdom.base",
  "constitutional_root_uid": "bytes32_or_pending",
  "session_id": "string",
  "receipt_count": 0,
  "bundle_hash": "bytes32",
  "receipts": []
}
```

## Invariants

```text
Family before Economy.
School before Market.
Repair before Punishment.
Replay before Authority.
Receipts before Synthesis.
Human acceptance before Settlement.
```

## Audit Verdict

AGENT_ORACLE_V2_CONSTITUTIONAL_SPEC_READY

The swarm becomes a constitutional machine only when every worker bee output is receipted, replayable, challengeable, and bound to root law.
