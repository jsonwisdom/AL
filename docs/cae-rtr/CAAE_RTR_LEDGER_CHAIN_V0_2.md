# CAAE-RTR Ledger Chain v0.2

Status: draft implementation baseline
Doctrine: Discovery creates debt. Replay-verified remediation closes debt. Everything else is narrative.

## Purpose

CAAE-RTR v0.1.1 gave deterministic close-out for a single finding. v0.2 adds tamper-evidence across time by chaining remediation receipts, committing each reporting window to a Merkle root, and separating remediation loss from ledger-integrity failure.

## Chain scope

The receipt chain is scoped per service boundary, not globally.

Field rule:

- `service` is mandatory domain separation.
- `prev_receipt_hash` means previous receipt hash for the same `service` chain.
- Receipt hash is computed over canonical JSON that includes `service`, `finding_hash`, `prev_receipt_hash`, `status`, `replay_verdict`, and all other material fields except derived signature fields.

This prevents transplanting a valid receipt from `service_a` into `service_b`.

## Window Merkle root

The window Merkle root is computed over full `receipt_hash` values, not `finding_hash` values.

Reason: `finding_hash` proves intake membership only. `receipt_hash` commits to outcomes, replay verdicts, authority scope, canary state, rollback state, and timestamps.

## Uniqueness guard

Finding uniqueness is scoped to `(service, finding_hash)`.

The same vulnerability may legitimately affect multiple services. A duplicate in the same service is a ledger issue unless it explicitly points to `first_seen_receipt_hash`.

## Temporal ordering

Use two clocks:

- `sequence`: monotonic logical integer, required for ordering.
- `timestamp_utc`: RFC3339 UTC timestamp, informational and auditable.

The validator fails closed on non-increasing `sequence`. Timestamp regressions are reported separately as clock-skew warnings unless strict timestamp mode is enabled.

## Integrity failure vs remediation loss

If the chain breaks, signature fails, duplicate guard fails, or Merkle root fails, the window result is not a normal low-RTR remediation window.

The validator reports:

- `governor_status: LEDGER_INTEGRITY_INCIDENT`
- `rtr: 0.0`
- `rtr_reason: LEDGER_INTEGRITY_FAILURE`

This keeps incident response separate from remediation backlog response.

## Required receipt fields

```json
{
  "schema": "CAAE_RTR_REMEDIATION_RECEIPT_V0_2",
  "service": "payments-api",
  "sequence": 42,
  "finding_hash": "sha256:...",
  "prev_receipt_hash": "sha256:...",
  "first_seen_receipt_hash": null,
  "severity": "critical",
  "capability_telemetry_cid": "ipfs://...",
  "exploit_harness_hash": "sha256:...",
  "pre_patch_replay": "PASS_EXPLOIT_CONFIRMED",
  "authority_token_id": "jit-...",
  "authority_scope_hash": "sha256:...",
  "patch_commit": "...",
  "canary_id": "canary-...",
  "canary_verdict": "PASS",
  "post_patch_replay": "PASS_EXPLOIT_BLOCKED",
  "replay_verdict": "PASS",
  "rollback_available": true,
  "rollback_receipt_hash": null,
  "transition_timestamps": [
    {"state": "CAPABILITY_VERIFIED", "timestamp_utc": "2026-06-21T18:00:00Z"},
    {"state": "ACCESS_SCOPED", "timestamp_utc": "2026-06-21T18:01:00Z"},
    {"state": "AUTHORITY_GRANTED", "timestamp_utc": "2026-06-21T18:02:00Z"},
    {"state": "CANARY_EXECUTED", "timestamp_utc": "2026-06-21T18:03:00Z"},
    {"state": "REPLAY_VERIFIED", "timestamp_utc": "2026-06-21T18:04:00Z"},
    {"state": "REMEDIATION_RECEIPTED", "timestamp_utc": "2026-06-21T18:05:00Z"}
  ],
  "status": "REMEDIATION_RECEIPTED",
  "receipt_hash": "sha256:..."
}
```

## Boss Lock

Incoming receipt status is not trusted.

A critical receipt is only counted as remediated when:

- `post_patch_replay == PASS_EXPLOIT_BLOCKED`
- `replay_verdict == PASS`
- `status == REMEDIATION_RECEIPTED`
- chain integrity passes
- service-scoped duplicate guard passes
- window Merkle root passes, when provided
- ledger signature passes, when provided

Otherwise it becomes `DEBT_ACCUMULATING` or a ledger-integrity incident.

## RTR

```text
RTR = verified_remediations / critical_findings
Debt(t) = critical_findings - verified_remediations
```

When ledger integrity fails:

```text
RTR = 0.0
rtr_reason = LEDGER_INTEGRITY_FAILURE
governor_status = LEDGER_INTEGRITY_INCIDENT
```

When no critical findings exist:

```text
0 findings / 0 remediations = STABLE_EMPTY_WINDOW, RTR = 1.0
remediations > findings = LEDGER_INTEGRITY_ERROR, RTR = 0.0
```

## v0.2 acceptance

A window is green only when:

- every receipt hash recomputes from canonical JSON,
- every `prev_receipt_hash` matches the previous receipt in the same service chain,
- every service sequence is strictly increasing,
- every `(service, finding_hash)` duplicate is explained by `first_seen_receipt_hash`,
- Merkle root over receipt hashes matches,
- Ed25519 signature over Merkle root verifies when a public key is provided,
- Boss Lock audited statuses produce `RTR >= 1.0` or `STABLE_EMPTY_WINDOW`.
