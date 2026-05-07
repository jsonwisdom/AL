# REPUTATION_SPEC_V1

Status: MAINNET
Artifact Class: GOVERNANCE_PRIMITIVE
Property: REPLAY-ADMISSIBLE
Operator: jaywisdom.base.eth
Hash Policy: Canonical UTF-8 LF -> SHA-256

## 0. Primitive

Reputation = Replay Survival.

A reputation claim is valid if and only if it survives replay under the constraints defined in this specification.

## 1. Definitions

### 1.1 Replay

A deterministic re-execution of a declared process using canonical inputs, canonical transforms, and canonical outputs, with no network access, no nondeterminism, and no undeclared state.

### 1.2 Canonical Bytes

The exact byte sequence representing inputs, transforms, outputs, receipts, and verdicts.

Canonical bytes MUST be UTF-8, LF-terminated, free of BOM, and free of environment-dependent serialization differences.

### 1.3 Survival

A process survives replay if the replayed output is byte-equivalent to the declared canonical output.

### 1.4 Failure

A process fails replay if the replayed output diverges from the canonical output.

### 1.5 Refusal

A process is refused if it violates admissibility conditions and therefore cannot be replayed.

### 1.6 Receipt

A machine-admissible record binding canonical inputs, canonical outputs, transforms, operator identity, environment invariants, git commit, attestation UIDs, and tx hashes.

### 1.7 Verdict

A machine-readable determination of PASS, FAIL, or REFUSE.

## 2. Invariants

### 2.1 No Replay -> No Proof

If a claim cannot be replayed, it cannot be considered valid.

### 2.2 No Canonical Bytes -> No Replay

If canonical bytes are missing, mutated, or ambiguous, replay is impossible.

### 2.3 No Undeclared Transforms

All transforms MUST be declared in the receipt. Any undeclared transform invalidates admissibility.

### 2.4 No Network Calls During Replay

Replay MUST NOT perform HTTP(S) requests, RPC calls, DNS lookups, or external filesystem reads.

### 2.5 No Synthetic Continuity

Replay MUST NOT infer missing state. If an ancestor is missing, the process is REFUSED.

### 2.6 Operator Bound by Same Rules

The operator MUST be replayable under the same constraints as the verified party.

### 2.7 Payment Cannot Influence Verdict

Payment grants access to the process, not influence over the outcome.

## 3. Replay Contract

### 3.1 Required Inputs

- canonical input bytes
- declared transform list
- declared environment invariants
- declared operator identity
- declared git commit
- declared receipt hash

### 3.2 Allowed Transforms

Transforms MUST be deterministic, pure, order-stable, and declared in advance.

### 3.3 Forbidden Transforms

- nondeterministic operations
- time-dependent operations
- environment-dependent operations
- network-dependent operations
- hidden state mutation

### 3.4 Equivalence

Replay output MUST be byte-equivalent to canonical output.

### 3.5 Divergence

Any byte-level difference constitutes FAIL.

## 4. Verdict Semantics

### 4.1 PASS

Replay output == canonical output.

### 4.2 FAIL

Replay output != canonical output.

### 4.3 REFUSE

Replay cannot proceed due to missing canonical bytes, undeclared transforms, environment violations, nondeterminism, forbidden operations, or missing ancestors.

## 5. Governance Boundary

### 5.1 Process Supremacy

The process outranks the operator. The operator cannot override replay.

### 5.2 Economic Membrane

Payment buys access to the process, the replay engine, and the adjudication pipeline.

Payment does NOT buy favorable outcomes, altered transforms, or relaxed invariants.

### 5.3 Third-Party Replay

Any third party MUST be able to obtain canonical bytes, execute replay, and verify verdicts.

### 5.4 Operator Replaceability

Any verifier implementing this spec is admissible. No verifier is privileged.

## 6. Replay Verdict Schema Stub

```json
{
  "verdict": "PASS | FAIL | REFUSE",
  "claim_id": "string",
  "canonical_input_sha256": "hex32",
  "canonical_output_sha256": "hex32",
  "replay_output_sha256": "hex32 | null",
  "receipt_sha256": "hex32",
  "operator_identity": "string",
  "git_commit": "hex20",
  "environment": {
    "os": "string",
    "arch": "string",
    "runtime": "string"
  },
  "timestamp_unix": "int64"
}
```

## 7. Compliance

A verifier is compliant if all invariants are enforced, all receipts are canonical, all verdicts are machine-admissible, all replays are deterministic, and all transforms are declared.

A verifier is non-compliant if any invariant is violated.

## 8. Constitutional Clause

This specification is the root of the reputation system. All other artifacts, including the service contract, court interface, landing page, and implementation guides, MUST derive from this spec and MUST NOT contradict it.
