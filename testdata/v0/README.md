# REPLAY LOOP V0 Stranger Replay

This directory contains the minimal V0 conformance corpus for replayable delegation receipts.

The goal is simple:

```text
A stranger should be able to clone the repo, run the verifier, and independently reach the same PASS/FAIL result.
```

## Happy Path

```bash
python3 tools/verify_fixture.py \
  testdata/v0/valid/receipt-valid.json \
  testdata/v0/valid/binding-valid.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
PASS
```

Node.js parity:

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

## Ed25519 Cryptographic Verification (V0)

The `tools/verify_fixture.py` and `tools/verify_fixture.js` verifiers now perform real Ed25519 signature verification on `AGENT_DELEGATION_RECEIPT_V0` receipts.

### Test Vector

- **Public Key**: `37e9edc1ca6c423ec0955156b9bd318e7581ef4492b28a92235ee900d53174cc`
- **Signature Algorithm**: `Ed25519`
- **Canonicalization**: RFC8785-style deterministic sorted compact JSON, excluding `proof.signature`
- **Python dependency**: `cryptography>=42.0.0`

## Enforcement Examples

### Receipt Digest Mismatch

```bash
python3 tools/verify_fixture.py \
  testdata/v0/valid/receipt-valid.json \
  testdata/v0/invalid/binding-wrong-receipt-digest.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
FAIL: receipt digest mismatch
```

### Expired Receipt

```bash
python3 tools/verify_fixture.py \
  testdata/v0/invalid/receipt-expired.json \
  testdata/v0/valid/binding-valid.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
FAIL: receipt expired
```

### Tampered Signature

Python:

```bash
python3 tools/verify_fixture.py \
  testdata/v0/invalid/receipt-tampered-signature.json \
  testdata/v0/valid/binding-valid.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
FAIL: signature mismatch
```

Node.js:

```bash
node tools/verify_fixture.js \
  testdata/v0/invalid/receipt-tampered-signature.json \
  testdata/v0/valid/binding-valid.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
FAIL: signature mismatch
```

### Forbidden File

```bash
python3 tools/verify_fixture.py \
  testdata/v0/valid/receipt-valid.json \
  testdata/v0/invalid/binding-forbidden-file.json \
  testdata/v0/valid/policy-valid.json
```

Expected output:

```text
FAIL: forbidden file touched: auth.py
```

## Continuous Replay

The Replay Loop V0 workflow is intended to run these checks on changes to this corpus or the verifier tools.

## V0 Boundary

This V0 harness now closes the mock-signature gap for receipt verification while preserving compatibility with #291 and #292.

Current boundaries:

- verifies receipt signatures using Ed25519
- uses deterministic sorted compact JSON rather than full RFC8785 coverage
- verifies signatures on receipts only
- checks `binding.receipt_digest == receipt.proof.digest`
- applies simple file-scope policy using `allowed_paths` and `forbidden_paths`
- does not implement production key management
- does not implement revocation
- does not verify real GitHub PR diffs yet

## Canonical Principle

Agent identity answers who acted.  
Delegation receipts answer who had authority.
