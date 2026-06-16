# FIXTURE_EVIDENCE_CHECKLIST_V0_1

## STATUS: REUSABLE_CHECKLIST
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

Use this checklist at the top of new fixtures, receipts, runbooks, replay notes, and claim documents.

## Required Header

```text
TEMPLATE_COMPLIANT: TRUE|FALSE
TEMPLATE_REFERENCE: docs/templates/CLAIM_EVIDENCE_BOUNDARY_TEMPLATE_V0_1.md
AUTHORITY: FALSE
NO_FAKE_GREEN: TRUE
```

## Minimum Checklist

```text
[ ] The file states what is claimed.
[ ] The file states the claim source.
[ ] The file separates reported claims from verified facts.
[ ] The file names the exact evidence that would verify the claim.
[ ] The file states current evidence status.
[ ] The file includes hard category boundaries.
[ ] The file names one allowed next action.
[ ] The file forbids upgrades without evidence.
[ ] The file does not imply revenue, authority, validation, or verification without output.
[ ] The file uses accurate language: recorded, candidate, pending, observed, or verified_by_output.
```

## Replacement Rule

```text
locked -> recorded, unless real command output or commit readback exists
validated -> pending validation, unless validator output is attached
classifier -> script or manual review, unless a real classifier exists
node query -> RPC command, only when an actual RPC command/output exists
anchor -> candidate anchor, unless source bytes and verification output exist
operator-reported -> self-reported, when the same person supplied the claim
```

## Ruling

```text
CHECKLIST_READY = TRUE
NEW_FIXTURE_ENFORCEMENT = LIGHTWEIGHT
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
