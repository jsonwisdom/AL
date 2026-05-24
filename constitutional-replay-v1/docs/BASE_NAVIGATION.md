# BASE_NAVIGATION.md — constitutional-replay-v1

Receipt-first bridge. Local replay sovereign. Base as witness only.

```text
No witness, no claim.
No receipt, no ratification.
No replay, no settlement.
```

## Layer Separation

AL doctrine preserved:

- **Local Replay** → proves meaning: deterministic, no network, no clock, no entropy.
- **AL Receipt** → evidence: policy, interpreter, and replay binding.
- **Base transaction or root** → witness: immutable public record.
- **x402** → payment trigger and settlement surface.
- **Smart Wallet** → signer and executor.
- **Paymaster** → gas witness.
- **EAS / Attestation** → optional public witness.

Base never mutates replay semantics.

Base cannot override a local verdict.

## v0.1 Boundary: Local-First Only

v0.1 must preserve:

- No Base RPC calls.
- No on-chain dependencies.
- No live clock in replay.
- No network access in replay.
- No witness fields required.
- All verdicts come from local policy interpreter and replay engine.

Failure state:

- Any attempt to call Base before golden vectors pass.

## v0.2+ Witness Integration Paths

### `BASE_WITNESS_NONE`

v0.1 default.

Receipts carry no Base reference.

### `BASE_TX_HASH`

Optional field:

```json
{
  "base_witness": {
    "mode": "BASE_TX_HASH",
    "tx_hash": "0x...",
    "block_number": 1234567
  }
}
```

Verification:

- read-only RPC lookup of transaction existence
- optional event log lookup
- no semantic replay mutation

### `BASE_MERKLE_ROOT`

Batch commitment:

```json
{
  "base_witness": {
    "mode": "BASE_MERKLE_ROOT",
    "root": "0x...",
    "batch_index": 42
  }
}
```

Verification:

- confirm root exists on Base
- verify local receipt hash against local Merkle proof
- preserve full local replay requirement

### `BASE_EAS_ATTESTATION`

Optional public proof:

```json
{
  "base_witness": {
    "mode": "BASE_EAS_ATTESTATION",
    "attestation_uid": "0x..."
  }
}
```

Verification:

- confirm attestation exists
- confirm attester if required
- confirm payload hash matches local commitment
- do not treat attestation as replay authority

### `BASE_CONTRACT_EVENT`

Future mode.

Receipt summary emitted as contract event for indexing.

Rule:

- event supports discovery
- full receipt supports replay

All witness fields are additive only.

Local replay must still succeed without them.

## x402 Handoff

x402 is a payment trigger and settlement surface.

AL mapping:

- x402 request quote → `input_hash`
- signed authorization → `economic_authority_hash`
- settlement transaction hash → `execution_ref`
- AL receipt → full semantic replay object

Constraints:

- No sensitive payload in x402 metadata.
- No free-text refusal reasons.
- Use fixed refusal enum only.
- Hash context before settlement.
- Redaction middleware is recommended for public metadata.

## Smart Wallet Handoff

Wallet actions should eventually emit receipts automatically:

- action execution → `emitReceipt()`
- policy refusal → `emitRefusal()`
- capability delegation → `delegateCapability()`
- on-chain transaction → `execution_ref` witness

Wallet signs the receipt binding, not the raw sensitive payload.

## Paymaster Boundary

- Paymaster is a gas witness only.
- Paymaster does not interpret policy.
- Paymaster does not produce semantic meaning.
- Policy hash remains the authority boundary.
- Receipt remains the replay object.

## Risk Controls

Known risk surface:

- payment metadata can leak resource URLs, descriptions, reason strings, or operational context before settlement.

Mitigation:

- refusal enum only
- no free-text refusal reasons
- context hashed, not embedded
- full receipt revealed only during explicit replay or challenge
- no floats
- no random IDs
- no live clock anywhere in replay path

## Jay Navigation Rule

1. Build and prove local replay first: golden vectors plus `demo.sh`.
2. Add read-only Base witness verification.
3. Add x402 payment-trigger integration.
4. Add Smart Wallet and Paymaster automation hooks.
5. Add optional EAS public witness.

Never let Base become replay authority.

## Final Status

This document is the canonical navigation receipt for Base integration in `constitutional-replay-v1`.

All future Base-related changes must reference it.
