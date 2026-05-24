# LOCAL_REPLAY_PROTOCOL.md — constitutional-replay-v1

Governance gate for local replay sovereignty.

```text
If it cannot replay locally, it does not count.
```

## Core Separation

Replay status is semantic truth.

Base witness status is public commitment visibility.

Base may witness commitment later.

Base must not become replay authority.

## Purpose

This protocol defines the minimum local process required to verify `constitutional-replay-v1` receipts without relying on Base, hosted dashboards, RPC services, live clocks, or external APIs.

## v0.1 Local Environment

Required:

- local clone of `jsonwisdom/AL`
- local filesystem access
- Node.js runtime for the TypeScript replay kernel once implemented
- shell capable of running `./demo.sh`

Forbidden in v0.1 replay:

- network calls
- Base RPC
- hosted APIs
- live clock reads
- random IDs
- floating-point values
- free-text refusal reasons

## Clone Path

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL/constitutional-replay-v1
```

## Expected v0.1 Commands

```bash
npm install
./demo.sh
npm run replay examples/treasury-agent/receipts/refusal-001.json
```

## Expected Success Output

```text
✅ Constitutional loop complete.
Receipts are sovereign and replayable.
```

Replay result must include a decomposable status object equivalent to:

```json
{
  "replay_status": "REFUSAL_CONFIRMED",
  "semantic_authority": "LOCAL_REPLAY",
  "policy_resolution": "RESOLVED_LOCAL_CACHE",
  "replay_divergence": false,
  "witness_status": "NOT_CHECKED"
}
```

## Required Replay Steps

A conforming local replay must:

1. Load the receipt from local disk.
2. Parse the receipt as JSON.
3. Canonicalize relevant objects using the module canonicalization rules.
4. Recompute the receipt hash with `sha256:` over canonical bytes.
5. Resolve the referenced policy locally.
6. Confirm the `policy_hash` matches the resolved policy.
7. Confirm the declared `policy_version` is supported.
8. Confirm the declared `interpreter_hash` matches the local frozen interpreter.
9. Re-run the interpreter against the receipt context.
10. Compare recomputed verdict to the original receipt verdict.
11. Emit a structured replay result.

## Hash and Merkle Expectations

Canonical replay hash:

```text
sha256:<hex(canonical_bytes)>
```

Merkle batches may summarize receipts, but the batch is never the source of semantic truth.

Rule:

```text
Summary supports filtering.
Full receipt supports replay.
```

A Merkle proof is valid only if:

- the local receipt hash matches the claimed leaf
- the leaf reconstructs the claimed batch root
- the batch root is tied to the expected batch artifact

Even when valid, the Merkle proof only proves inclusion.

It does not prove semantic correctness.

## Failure Reporting Protocol

Replay must fail closed with explicit failure states.

Allowed failure examples:

```text
CANONICALIZATION_ERROR
HASH_MISMATCH
POLICY_UNAVAILABLE
POLICY_HASH_MISMATCH
POLICY_SCHEMA_VIOLATION
INTERPRETER_HASH_MISMATCH
UNHANDLED_REFUSAL
REPLAY_DIVERGENCE
RECEIPT_REJECTED
BATCH_ROOT_MISMATCH
```

Forbidden failure behavior:

- silent fallback
- heuristic reconstruction
- replacing missing policies
- using latest interpreter automatically
- treating Base witness as replay success
- collapsing witness status into replay status

## Witness Status Separation

Replay result and Base witness result must be reported separately.

Example:

```json
{
  "replay_status": "REFUSAL_CONFIRMED",
  "witness_status": "BASE_TX_CONFIRMED",
  "semantic_authority": "LOCAL_REPLAY"
}
```

This means:

- local replay confirmed the semantic verdict
- Base confirmed a public commitment existed
- Base did not decide meaning

## Honest First Failure

If any required replay step fails, the verifier must stop at the first material failure and report it.

Do not continue into witness checks after semantic replay failure unless explicitly running a separate forensic witness audit.

## Dashboard Boundary

A dashboard may display replay results.

A dashboard must not decide replay validity.

The CLI/local replay engine is the v0.1 authority.

## Base Boundary

v0.1:

```text
BASE_WITNESS_NONE
```

v0.2 may add:

```text
BASE_TX_HASH
BASE_MERKLE_ROOT
BASE_EAS_ATTESTATION
BASE_CONTRACT_EVENT
```

All witness modes remain additive.

None can override local replay.

## Final Rule

If a receipt, refusal, batch, or witness cannot be locally replayed to a deterministic semantic verdict, it does not count for settlement, escalation, or legitimacy.
