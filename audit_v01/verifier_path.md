# Replayable Resilience Audit v0.1 — Verifier Path

## Purpose
This file defines how an outside verifier checks the first JSONWisdom membrane enforcement event without trusting conversation memory, private reasoning, or operator narrative.

## Current freeze candidate

The candidate constitutional freeze is the latest GitHub commit that includes:

- `membrane.json`
- `system_manifest.json`
- `audit_v01/assumption_map.md`
- `audit_v01/failure_mode_graph.json`
- `audit_v01/kill_order_report.md`
- `audit_v01/audit_receipt.json`
- `audit_v01/verifier_path.md`

## Verification layers

| Layer | Role | Authority limit |
|---|---|---|
| GitHub commit | Artifact state | Shows repository content at a commit |
| ENS/Basename | Human-readable pointer | Routes to a commit; does not prove correctness alone |
| Base tx | Public timestamped witness | Shows a commitment existed onchain |
| EAS UID | Structured attestation | Optional structured witness |
| Verifier replay | Truth promotion check | Recomputes and compares artifacts |

## Step-by-step replay

1. Resolve `jaywisdom.base.eth` text record `constitution.v0`.
2. Treat the resolved value as a GitHub commit SHA candidate.
3. Fetch `jsonwisdom/AL` at that exact commit.
4. Confirm all required files exist.
5. Read `membrane.json` and confirm the core rule:

   `Cognition may change internal state. Only receipts may promote truth state.`

6. Read `system_manifest.json` and confirm the claimed Merkle root remains marked `UNVERIFIED_IDENTIFIER` unless later receipts prove otherwise.
7. Read `audit_v01/assumption_map.md` and confirm the original anchor claim was downgraded to `NEEDS_RECEIPTS`.
8. Read `audit_v01/failure_mode_graph.json` and confirm failure modes F1-F5 were captured.
9. Read `audit_v01/kill_order_report.md` and confirm promotion was frozen before commercial escalation.
10. Read `audit_v01/audit_receipt.json` and confirm no Base/EAS/ENS witness is fabricated.
11. Recompute any declared content hashes once a final hash manifest is present.
12. Only promote to `VERIFIED` if recomputation and public witness match.

## Failure conditions

A verifier must reject promotion if any of the following occur:

- ENS points to a commit that does not contain the required files.
- `audit_receipt.json` claims Base/EAS witnesses that do not resolve.
- The Merkle root is treated as verified without a leaf list and canonicalization rule.
- Conversation text is used as proof instead of committed artifacts.
- The verifier cannot reproduce the declared content hash.

## Current allowed verdict

Until ENS, Base, or EAS witness exists, the strongest honest verdict is:

`GITHUB_ANCHORED_NEEDS_CHAIN_WITNESS`

## Core principle

The verifier does not ask whether the story is convincing.

The verifier asks whether the committed artifacts replay.
