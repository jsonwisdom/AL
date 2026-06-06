# AGENT_DELEGATION_RECEIPT_V0

**Replay Loop V0** — Replayable delegation receipts for agent actions.

**Status**: V0 — executable harness, fixture corpus, README, dual verifiers, and GitHub Actions continuous replay are live.

**Core Principle**: Do not inherit trust. Replay it.

## 1. Purpose

`AGENT_DELEGATION_RECEIPT_V0` defines a minimal receipt format for proving that an agent action was performed under a bounded delegation.

An independent verifier should be able to determine:

- a delegation receipt exists
- the receipt has not expired
- a result binding references the receipt
- the observed files are permitted by policy
- invalid cases fail deterministically

V0 is intentionally small. It is a conformance harness, not production cryptography.

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
    "signature_alg": "Ed25519-MOCK-V0",
    "signature": "mock-valid-signature"
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

## 4. Result Binding

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

### 4.1 Required V0 Binding Fields

- `binding_type`
- `binding_version`
- `receipt_digest`
- `actor.id`
- `actor.key`
- `result.repo`
- `result.branch`
- `result.commit`
- `result.pr`
- `result.changed_files`
- `bound_at`
- `proof.canonicalization`
- `proof.digest`
- `proof.alg`
- `proof.value`

## 5. Policy

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

A changed file fails if:

- it appears in `forbidden_paths`, or
- `allowed_paths` is non-empty and the file does not appear in `allowed_paths`

## 6. Verification Algorithm

The reference verifiers are:

- `tools/verify_fixture.py`
- `tools/verify_fixture.js`

A conforming V0 verifier checks, in order:

1. Load receipt, binding, and policy JSON.
2. Validate required fields.
3. Verify receipt type is `AGENT_DELEGATION_RECEIPT_V0`.
4. Verify binding type is `AGENT_RESULT_BINDING_V0`.
5. Verify policy path lists are arrays.
6. Verify `scope.expires_at` is valid and not expired, allowing 300 seconds of clock skew.
7. Verify V0 proof marker on the receipt.
8. Verify `binding.receipt_digest == receipt.proof.digest`.
9. Verify V0 proof marker on the binding.
10. Verify `result.changed_files` against the policy.
11. Return `PASS` if all checks pass.

## 7. Public Failure Modes

The fixture corpus demonstrates these deterministic failures:

- `FAIL: schema invalid`
- `FAIL: signature mismatch`
- `FAIL: receipt expired`
- `FAIL: receipt digest mismatch`
- `FAIL: forbidden file touched: auth.py`
- `FAIL: file outside allowed paths: <path>`

## 8. Replay Instructions

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

## 9. V0 Boundaries

Replay Loop V0 is deliberately honest about its limits:

- mock proof values are used
- real Ed25519 verification is not implemented
- RFC8785 canonicalization is declared but not implemented
- policy hash verification is not implemented
- GitHub PR diffs are represented by fixture `changed_files`
- revocation is not implemented

## 10. Next Milestones

1. Replace mock proof checks with real Ed25519 signatures.
2. Implement RFC8785 JSON Canonicalization Scheme.
3. Compute and verify real `sha256:` digests.
4. Enforce JSON Schema files directly.
5. Verify real GitHub PR diffs.
6. Add additional independent implementations.

## 11. Canonical Principle

Agent identity answers who acted.  
Delegation receipts answer who had authority.

Replay Loop V0 is the first executable conformance harness for that principle.
