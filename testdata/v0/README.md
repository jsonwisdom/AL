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

## V0 Boundary

This V0 verifier uses mock proof values. It is a deterministic conformance harness, not production cryptography.

Production work must add:

- real Ed25519 verification
- RFC8785 JSON canonicalization
- schema validation
- policy hash verification
- real GitHub PR diff binding

## Canonical Principle

Agent identity answers who acted.  
Delegation receipts answer who had authority.
