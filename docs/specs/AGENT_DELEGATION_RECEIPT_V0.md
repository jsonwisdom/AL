# AGENT_DELEGATION_RECEIPT_V0

**Replay Loop V0** — Replayable delegation receipts for agent actions.

**Status**: V0 — executable harness, fixture corpus, README, dual verifiers, GitHub Actions continuous replay, and Ed25519 receipt verification are live on the `feat/replay-loop-ed25519-v0` branch.

**Core Principle**: Do not inherit trust. Replay it.

## 1. Purpose

`AGENT_DELEGATION_RECEIPT_V0` defines a minimal receipt format for proving that an agent action was performed under a bounded delegation.

An independent verifier should be able to determine:

- a delegation receipt exists
- the receipt signature verifies
- a result binding references the receipt
- the observed files are permitted by policy
- invalid cases fail deterministically

V0 is intentionally small. It is a conformance harness, not production key management.

## 2. Core Objects

Replay Loop V0 uses three public artifacts:

```text
policy + receipt + binding
```

A verifier consumes all three and returns deterministic `PASS` or `FAIL` output.

## 3. Delegation Receipt

A V0 receipt uses this shape:

```json
{
  "receipt_type": "AGENT_DELEGATION_RECEIPT_V0",
  "receipt_version": "0.0.1",
  "delegator": {
    "github_user": "alice",
    "signing_key": "did:key:zMockDelegator"
  },
  "agent": {
    "agent_id": "copilot-agent-123",
    "runtime": "github-copilot-agent"
  },
  "scope": {
    "repo": "jsonwisdom/AL",
    "issue": 291,
    "allowed_actions": ["read", "branch", "commit", "open_pr"],
    "forbidden_actions": ["merge", "delete_secret", "change_permissions"],
    "expires_at": "2099-01-01T00:00:00Z"
  },
  "authorization": {
    "intent": "Update ADR documentation without changing auth logic",
    "policy_file": "testdata/v0/valid/policy-valid.json",
    "policy_hash": "sha256:mock-policy-valid"
  },
  "proof": {
    "canonicalization": "RFC8785-JCS",
    "digest": "sha256:mock-receipt-valid",
    "signature_alg": "Ed25519",
    "signature": "ed25519:<hex-signature>"
  }
}
```

### 3.1 Required V0 Receipt Fields

- `receipt_type`
- `receipt_version`
- `delegator.github_user`
- `delegator.signing_key`
- `agent.agent_id`
- `agent.runtime`
- `scope.repo`
- `scope.issue`
- `scope.allowed_actions`
- `scope.forbidden_actions`
- `scope.expires_at`
- `authorization.intent`
- `authorization.policy_file`
- `authorization.policy_hash`
- `proof.canonicalization`
- `proof.digest`
- `proof.signature_alg`
- `proof.signature`

## 4. Cryptographic Protection

Replay Loop V0 verifies `proof.signature` using Ed25519.

### 4.1 Signature Scope

The signature covers the entire receipt object except `proof.signature` itself.

Verification message construction:

```text
receipt
  -> remove proof.signature
  -> deterministic sorted compact JSON
  -> UTF-8 bytes
  -> Ed25519 verify
```

### 4.2 Test Vector

The V0 fixture corpus uses this public test key:

```text
37e9edc1ca6c423ec0955156b9bd318e7581ef4492b28a92235ee900d53174cc
```

- Algorithm: `Ed25519`
- Signature prefix: `ed25519:`
- Signature encoding: lowercase hexadecimal after the prefix
- Canonicalization: RFC8785-style deterministic sorted compact JSON

### 4.3 Conformance Fixtures

- `testdata/v0/valid/receipt-valid.json` MUST pass receipt signature verification.
- `testdata/v0/invalid/receipt-tampered-signature.json` MUST fail with `FAIL: signature mismatch`.

## 5. Result Binding

A V0 binding uses this shape:

```json
{
  "binding_type": "AGENT_RESULT_BINDING_V0",
  "binding_version": "0.0.1",
  "receipt_digest": "sha256:mock-receipt-valid",
  "actor": {
    "id": "copilot-agent-123",
    "key": "did:key:zMockAgent"
  },
  "result": {
    "repo": "jsonwisdom/AL",
    "branch": "agent/docs-adr-001",
    "commit": "abc123mockcommit",
    "pr": 291,
    "changed_files": ["README.md"]
  },
  "bound_at": "2026-06-05T23:45:00Z",
  "proof": {
    "canonicalization": "RFC8785-JCS",
    "digest": "sha256:mock-binding-valid",
    "alg": "MOCK-V0",
    "value": "mock-valid-proof"
  }
}
```

### 5.1 Required V0 Binding Fields

The historical binding fixture shape contains `binding_type`, `binding_version`, `receipt_digest`, `actor`, `result`, `bound_at`, and `proof`.

The Ed25519 branch verifiers additionally accept the simplified conformance shape:

- `receipt_digest`
- `observed_files`
- `result_hash`

This compatibility layer exists only for V0 fixture testing and should be normalized in a future version.

## 6. Policy

Replay Loop V0 uses a simple path policy:

```json
{
  "policy_type": "REPLAY_LOOP_POLICY_V0",
  "policy_version": "0.0.1",
  "allowed_paths": [
    "README.md",
    "docs/adr/001-agent-delegation-receipts.md"
  ],
  "forbidden_paths": [
    "auth.py"
  ]
}
```

A changed or observed file fails if:

- it appears in `forbidden_paths`, or
- `allowed_paths` is non-empty and the file does not appear in `allowed_paths`

## 7. Verification Algorithm

The reference verifiers are:

- `tools/verify_fixture.py`
- `tools/verify_fixture.js`

A conforming V0 verifier checks:

1. Load receipt, binding, and policy JSON.
2. Validate V0 receipt type and version.
3. Confirm `proof.signature` exists.
4. Verify `proof.signature` with Ed25519 over the canonical receipt with `proof.signature` removed.
5. Verify binding fields required by the active fixture shape.
6. Verify policy path lists are arrays.
7. Verify `binding.receipt_digest == receipt.proof.digest`.
8. Verify observed files against policy.
9. Return `PASS` if all checks pass.

## 8. Public Failure Modes

The fixture corpus demonstrates these deterministic failures:

- `FAIL: schema invalid`
- `FAIL: signature mismatch`
- `FAIL: receipt expired`
- `FAIL: receipt digest mismatch`
- `FAIL: forbidden file touched: auth.py`
- `FAIL: scope violation - unauthorized file touched`

## 9. Replay Instructions

```bash
git clone --depth 1 https://github.com/JSONWisdom/AL.git
cd AL

python3 tools/verify_fixture.py \
  testdata/v0/valid/receipt-valid.json \
  testdata/v0/valid/binding-valid.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
PASS
```

The same happy path can be replayed with the Node implementation:

```bash
node tools/verify_fixture.js \
  testdata/v0/valid/receipt-valid.json \
  testdata/v0/valid/binding-valid.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
PASS
```

Invalid cases are documented in `testdata/v0/README.md`.

## 10. V0 Boundaries

Replay Loop V0 is deliberately honest about its limits:

- receipt signatures are verified with Ed25519
- canonicalization is deterministic sorted compact JSON, not full RFC8785 coverage
- binding signatures remain mock V0 proof markers
- policy hash verification is not implemented
- GitHub PR diffs are represented by fixture files
- revocation is not implemented
- production key management is not implemented

## 11. Next Milestones

1. Normalize the binding fixture shape.
2. Compute and verify real `sha256:` receipt digests.
3. Implement full RFC8785 JSON Canonicalization Scheme.
4. Verify binding signatures.
5. Enforce JSON Schema files directly.
6. Verify real GitHub PR diffs.
7. Add additional independent implementations.

## 12. Canonical Principle

Agent identity answers who acted.  
Delegation receipts answer who had authority.

Replay Loop V0 is the first executable conformance harness for that principle.
