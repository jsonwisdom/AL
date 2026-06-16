# Constitutional Replay Economy v0.1

Status: DRAFT
Operational status: ACTIVE_FOR_REVIEW
Scope: All economic interfaces to the constitutional machine
Enforcement: schema + CI + forbidden terms + runtime tests

## 1. Purpose

Define what revenue may and may not purchase.

This spec makes the business model a constitutional surface, not an external contract.

Core invariant:

```json
{
  "revenue_cannot_buy_authority": true
}
```

Money buys operations.

Money cannot buy meaning, attention, speech, interpretation, unlock authority, verdict semantics, or lifecycle power.

## 2. Constitutional Surfaces Affected

No economic interface may modify:

1. Speech: `AllowedSurface` from `proof_blob_v0.1.md`
2. Receipts: verdict schema or forbidden fields
3. Dashboard: payload guard or four-state rendering
4. Restricted access: RAP unlock logic or decryptor authority
5. Attention: `targets_governance_v0.1.md`
6. Agent identity: `agent_manifest_v0.1.md`
7. Agent lifecycle: proposal, amendment, deprecation, retirement
8. CI immunity: membrane tests, forbidden terms scan, schema validation
9. Economic membrane: this document

## 3. Forbidden Economic Transactions

Revenue must not purchase:

- new verdicts
- new semantics
- sentiment, political classification, or risk modeling
- dashboard mutation that adds fields, scores, colors, or interpretive layers
- target addition, removal, or prioritization outside targets governance
- receipt suppression
- RAP unlock authority
- custom decryptors
- agent privileges
- new agent kind
- schema exceptions
- customer-specific `additionalProperties` overrides
- private interpretation layers that add meaning to receipts

## 4. Permitted Economic Transactions

Revenue may purchase:

- crawl frequency
- SLA and uptime
- API throughput
- webhook concurrency
- signed feed delivery
- white-label rendering that preserves membrane constraints
- filters on tags, dates, and allowed verdicts
- support and integration work
- custom export formats
- on-prem runners
- expedited review queue position for governed target PRs
- attestation bundles of existing receipts
- agent bounties for bounded agents

Paid features must modify operational parameters only.

Paid features must not alter verdict enums, schemas, membrane logic, target governance, lifecycle governance, or unlock authority.

## 5. Participant Classes

### Observers

Participants:

- journalists
- researchers
- watchdogs
- civic groups

May pay for:

- webhooks
- API access
- historical replay
- exports
- uptime

May not buy:

- target control
- interpretive labels
- private verdicts

### Submitters

Participants:

- public-interest groups
- courts
- agencies
- archives

May pay for:

- target batch preparation
- governed target review support
- manifest support

May not buy:

- approval
- favorable verdicts
- bypass of targets governance

### Builders

Participants:

- developers
- civic technologists
- grant sponsors

May pay for:

- bounded agent bounties
- implementation sponsorship
- audits

May not buy:

- adjudicator agents
- risk scoring agents
- accusation semantics
- lifecycle shortcuts

### Integrators

Participants:

- legaltech firms
- compliance firms
- archival firms
- public-record platforms

May pay for:

- enterprise license
- support
- uptime
- deployment help

May not buy:

- official interpretive overlays
- custom forbidden fields
- verdict mutation

## 6. Economic Membrane Tests

CI should include:

- schema validation for billing config
- tests proving customer tiers render identical receipt JSON
- tests proving paid labels cannot auto-approve targets
- forbidden terms checks for economic authority leaks

Forbidden economic terms include:

```text
premium_verdict
risk_score
trust_score
sentiment
priority_verdict
customer_override
paid_unlock
private_interpretation
```

## 7. Amendment Process

Changing this spec requires:

1. PR tagged `constitutional-amendment`
2. Rationale explaining why the economic membrane must change
3. Review by maintainers
4. Full membrane test suite
5. Public diff

## 8. Customer Guarantee

Commercial contracts should reference this spec and include:

```text
Provider warrants that Customer payments cannot alter the constitutional surfaces defined in specs/. Provider breach of constitutional_replay_economy_v0.1.md constitutes material breach, and Customer may fork all constitutional artifacts under the applicable open license.
```

## 9. Non-Claims

This spec does not assert:

- customer legitimacy
- institutional guilt
- market dominance
- legal finality
- RAP activation
- mainnet activation

It defines only membrane-safe commercial access to a constitutionally bounded public-record replay machine.

## State

```json
{
  "constitutional_replay_economy_v0_1": "ACTIVE_FOR_REVIEW",
  "revenue_can_buy": ["scale", "speed", "uptime", "support", "exports", "integrations"],
  "revenue_cannot_buy": ["attention", "speech", "interpretation", "verdicts", "target_control", "unlock_authority", "lifecycle_power"],
  "RAP": "DORMANT",
  "mainnet_authority": "NOT_ACTIVE",
  "no_ghost_anchor": true
}
```
