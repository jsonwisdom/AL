# Witness Class Policy v0.1

Status: ACTIVE_POLICY_CLARIFICATION

## Purpose

This policy clarifies the difference between cryptographic witness evidence, external AI witness evidence, self-controlled lab signatures, and production trust-root quorum.

## Witness Classes

### 1. Production Witness

A production witness is a pre-registered witness identity in the repository trust-root policy.

Production witnesses may contribute to production quorum only if:

- the public witness identity is registered before promotion
- the signed artifact verifies against the registered public identity
- the witness is not controlled by the same operator as another quorum participant
- the applicable quorum threshold is met

### 2. External File-Level Witness

An external file-level witness signs the exact bytes of an artifact and returns a verifiable detached signature.

This is admissible evidence.

It does not automatically count as production quorum unless the witness identity is registered in the trust root.

### 3. External Hash-Only Witness

An external hash-only witness signs or confirms a hash string instead of the exact artifact bytes.

This may be useful review evidence.

It is weaker than file-level witness evidence and does not count as production quorum.

### 4. Self-Controlled Lab Witness

A self-controlled lab witness signature is produced by the same operator controlling the test environment.

It may prove crypto mechanics.

It does not count as independent witness quorum.

### 5. Signing Not Available

A model, service, or reviewer that cannot perform cryptographic signing may provide review or hash confirmation only.

It does not count as a signing witness.

## Current Treasury Application

PUBLIC_LIVE_FETCH = PASS
STRICT_PUBLIC_FILL = PASS
SELF_CONTROLLED_LAB_SIGNATURES = PASS_DISCLOSED
GROK_EXTERNAL_FILE_WITNESS = VERIFIED
DEEPSEEK_SIGNING_WITNESS = SIGNING_NOT_AVAILABLE
PRODUCTION_QUORUM = FALSE
REAL_GENESIS = BLOCKED
NO_FAKE_GREEN = ACTIVE

## Rule

External witness evidence may move the Treasury project forward as a genesis candidate or audit artifact.

Only registered production witnesses may unlock real genesis promotion.
