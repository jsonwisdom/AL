# Repo Test Topology Discovery V0.1

## Purpose
Prevent synthetic test path reconstruction before binding ArchiveCenter drift receipts into golden tests.

## Status
BLOCKED_ON_TEST_TOPOLOGY

## Core Rule
NO_SYNTHETIC_TEST_PATH_RECONSTRUCTION

## Reason
A drift receipt fixture exists, but the active verifier test source path is not yet byte-proven on this branch.

## Required Evidence Before Test Binding
One of the following must be proven from repository bytes before adding a golden test:

1. Confirmed current verifier test source path.
2. Existing package or verifier test root.
3. Existing schema loader path.
4. Existing FSM loader path.
5. Existing test file that imports or reads fixtures.

## Forbidden Actions
- Do not create `tests/test_verifier.py` from memory.
- Do not create `tools/al-verifier/tests/golden.rs` from stale search memory.
- Do not invent a Cargo, pytest, or verifier topology.
- Do not bind drift receipts into runtime without a proven test root.

## Required Behavior
FAIL_CLOSED

## Next Valid Transition
Only after a byte-proven test root is identified may the repo add a golden test binding for:

- `tests/fixtures/archivecenter_drift_receipt_v0_1.json`

## Authority
false
