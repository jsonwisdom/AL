# Replay Node v0.1 — Operator Brief

Status: PR #260-bounded operator explanation
Authority: false
Merge permission: false

## 1. What Replay Node v0.1 Does

Replay Node v0.1 replays one official public civic PDF source through a deterministic extraction pipeline.

It:

- fetches one official public PDF URL
- computes PDF SHA256
- verifies identity using expected date plus proceedings/minutes text
- extracts text with `pdftotext -layout`
- computes extracted text SHA256
- emits deterministic rows
- computes output CSV SHA256
- compares output CSV SHA256 against the claimed CSV SHA256
- emits receipt JSON only on MATCH
- fails closed on dependency, identity, or hash mismatch

## 2. What Replay Node v0.1 Does Not Do

Replay Node v0.1 does not:

- ingest CSV source inputs
- crawl websites
- perform daily ingestion
- assign merge authority
- certify institutions
- summarize civic content
- continue after hash mismatch
- continue after identity mismatch
- expose debug or mutation flags

## 3. Authority Posture

Replay Node v0.1 is verification infrastructure.

It preserves:

```json
{
  "authority": false,
  "merge_permission": false
}
```

The node may emit receipts.

A reviewer decides whether to trust, reject, rerun, or merge based on those receipts.

## 4. Fail-Closed Behavior

Replay Node v0.1 fails closed under:

- missing dependency
- PDF fetch failure
- identity mismatch
- output CSV SHA256 mismatch

The runtime would rather emit uncertainty than produce unverifiable output.

## 5. Membrane Rule

NO_NARRATIVE_MUTATION_OF_RUNTIME.

Every statement in this brief maps back to a runtime step, runtime scope item, fail-closed condition, or receipt field in `runtime_spec.md`.
