# Validator Verification Receipts

This directory is the receipt lane for the ComputerWisdom validator verification process.

## Purpose

The validator verification lane records evidence that validator outputs match the frozen fixture truth standard. It is a governance container, not an authority source.

## Scope

A validator verification receipt may record:

- the fixture name
- the canonical input hash
- the decision table version
- the expected state
- the evaluated state
- the verification result
- any failure class
- the authority boundary
- the membrane status
- the no-fake-green flag

## Membrane Rules

The following separations are mandatory:

```text
test_vectors != invariants
invariants != implementation
implementation != verification
verification != attestation
attestation != liquidity
```

A verification receipt does not create authority.
A matching fixture result does not create authority.
A passing test suite does not create authority.
A committed receipt does not create authority by itself.

Authority remains false unless separately established by an external attestation process.

## Failure Classes

```text
TYPE_1_LOGIC_DEVIATION
```

The validator output does not match the fixture expected_state.

```text
TYPE_2_INVARIANT_BREACH
```

The evaluated state violates the Replay Invariant Set.

```text
TYPE_3_NON_DETERMINISTIC
```

The same input and decision table produce different outputs across runs.

## Receipt Schema

A receipt should follow this shape:

```json
{
  "receipt_type": "VALIDATOR_VERIFICATION_RECEIPT",
  "version": "0.1",
  "fixture_name": "valid_pass",
  "input_hash": "sha256:<canonical_input_digest>",
  "decision_table_version": "DECISION_TABLE_V0_1",
  "expected_state": "PASS",
  "evaluated_state": "PASS",
  "verification_result": "MATCH",
  "failure_class": null,
  "authority": false,
  "membrane": "INTACT",
  "no_fake_green": true
}
```

## First Run Boundary

This README materializes the verification doctrine only.

It does not mean a verification run has occurred.
It does not mean receipts have been generated.
It does not mean authority has been created.

The first valid run state is:

```text
VALIDATOR_RUN_RECEIPT_001 = ELIGIBLE
AUTHORITY                 = FALSE
```

## No Fake Green

The verification lane must never mark the validator as green unless fixture execution produces matching results and those results are recorded as receipts.

Even then, the result is verification evidence only. It is not attestation and it is not authority.
