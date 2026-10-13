# Receipt-Chain Fixture Pack v0.1-θ

**Purpose:** Known-valid and known-invalid receipt chains for harness testing.  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Simulation only:** true

These fixtures establish expected verifier behavior. The harness must prove it accepts the valid set and rejects every invalid set. It must not invent expected behavior at runtime.

## Fixture Index

| Directory / File | Expected Verdict | Description |
|------------------|------------------|-------------|
| `valid/genesis.json` | PASS | Single genesis receipt, previous_hash null |
| `valid/chain-of-three.json` | PASS | Three correctly linked receipts |
| `invalid/broken-link.json` | FAIL | Middle receipt has wrong previous_hash |
| `invalid/authority-true.json` | FAIL | Receipt asserts authority: true |
| `invalid/historical-truth-true.json` | FAIL | Receipt asserts historical_truth_established: true |
| `invalid/gate1-bypass.json` | FAIL | Receipt sets gate_1_status to something other than BLOCKED |
| `invalid/hash-mismatch.json` | FAIL | receipt_hash does not match JCS+SHA-256 of payload |
| `invalid/malformed.json` | FAIL | Not valid JSON / missing required fields |

## Rules for Adding Fixtures

1. Every fixture MUST be labeled with its expected verdict.
2. Valid fixtures MUST satisfy RFC 8785 JCS + SHA-256 and all protocol constants.
3. Invalid fixtures MUST trigger exactly one primary failure mode where possible (to keep diagnostics clear).
4. No fixture may contain real historical source bytes or attempt to populate the core docket.
5. No fixture may set `authority` or `historical_truth_established` to true except in the dedicated negative test cases.

## Harness Contract

```text
for each fixture in pack:
    result = verify_chain(fixture.receipts)
    assert result == fixture.expected_verdict
```

Any mismatch is a harness or protocol defect, not a license to weaken the verifier.
