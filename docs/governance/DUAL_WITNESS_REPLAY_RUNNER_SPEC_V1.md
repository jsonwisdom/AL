# DUAL_WITNESS_REPLAY_RUNNER_SPEC_V1

Status: FROZEN
Date: 2026-05-27
Scope: Dual-witness governance membrane replay runner
Authority: NONE

## Purpose

Provide a deterministic, scriptable CLI that exercises the dual-witness harness and reports success or failure via exit codes and artifacts.

The runner performs no interpretation. It loads inputs, invokes the invariant harness, records replay artifacts, and exits with a machine-readable result.

## Command Signature

```bash
replay_membrane \
  --red PR_256 \
  --green PR_257 \
  --red-payload <file> \
  --green-payload <file> \
  [--red-receipt <file>] \
  [--green-receipt <file>] \
  --output-dir <dir> \
  [--verbose]
```

## Flags

| Flag | Required | Description |
|---|---:|---|
| `--red` | yes | PR identifier for red path. Must be `PR_256`. |
| `--green` | yes | PR identifier for green path. Must be `PR_257`. |
| `--red-payload` | yes | Path to file containing raw payload for `PR_256`. |
| `--green-payload` | yes | Path to file containing raw payload for `PR_257`. |
| `--red-receipt` | no | Path to receipt file for `PR_256`. If omitted, receipt is treated as missing. |
| `--green-receipt` | no | Path to receipt file for `PR_257`. Must be valid for green-path success. |
| `--output-dir` | yes | Directory where logs, receipts, and comparison report are written. |
| `--verbose` | no | Print decision traces to stdout. |

## Input Formats

### Payload File

Payload files are arbitrary bytes. They may be JSON, binary, text, or any other byte sequence. The harness canonicalization path must be identical for both PRs.

### Receipt File

Receipt files are JSON documents with the following minimal shape:

```json
{
  "id": "receipt-123",
  "lineage_hash": "0xabcd...",
  "issued_at": "2026-05-27T10:00:00Z",
  "issuer_id": "membrane/preflight/v1",
  "signature": "base64encoded..."
}
```

## Exit Codes

| Code | Meaning |
|---:|---|
| `0` | Dual-witness success: red rejected, green admitted, same invariants. |
| `1` | Red path false positive: red accepted when it should reject. |
| `2` | Green path false negative: green rejected when it should admit. |
| `3` | Harness internal error: canonicalization failure, receipt parse failure, or I/O error. |
| `4` | Non-determinism detected: same inputs produced different outputs across replay runs. |

## Output Artifacts

```text
output-dir/
├── PR_256_receipt.log
├── PR_257_receipt.log
├── comparison_report.json
└── replay_manifest.json
```

### Artifact Semantics

| Artifact | Meaning |
|---|---|
| `PR_256_receipt.log` | Full decision trace for red path. |
| `PR_257_receipt.log` | Full decision trace for green path. |
| `comparison_report.json` | Opposite lawful outcomes under the same invariant set. |
| `replay_manifest.json` | Summary of run, input hashes, invariant-set hash, determinism, and exit reason. |

## `replay_manifest.json` Example

```json
{
  "run_id": "replay-20260527T100000Z",
  "cli": "replay_membrane",
  "exit_code": 0,
  "red": {
    "pr": "PR_256",
    "decision": "REJECT",
    "receipt_present": false,
    "payload_hash": "0x111..."
  },
  "green": {
    "pr": "PR_257",
    "decision": "ADMIT",
    "receipt_present": true,
    "payload_hash": "0x222..."
  },
  "invariant_set_hash": "0xinvariant-set-v1",
  "deterministic": true
}
```

## Usage Examples

### Basic Dual-Witness Test

Expected result: exit `0`.

```bash
replay_membrane \
  --red PR_256 --red-payload ./pr256.bin \
  --green PR_257 --green-payload ./pr257.bin \
  --green-receipt ./valid_receipt.json \
  --output-dir ./replay_out
```

### Missing Green Receipt Test

Expected result: exit `2` because the green path has no valid receipt.

```bash
replay_membrane \
  --red PR_256 --red-payload ./pr256.bin \
  --green PR_257 --green-payload ./pr257.bin \
  --output-dir ./replay_out
```

## Determinism Enforcement

The CLI must:

1. Reuse exactly the same canonicalization logic for both PRs.
2. Not branch on `--red` or `--green` values inside invariant evaluation.
3. Record input hashes in the manifest for external replay verification.
4. Optionally rerun with identical inputs and compare outputs.
5. Exit `4` if identical inputs produce divergent outputs.

## Relationship to Harness Pseudocode

| CLI Concern | Harness Function |
|---|---|
| Parse flags and load files | `PRInput` construction |
| Invoke validator | `validate_pr()` |
| Check expected outcomes | `run_dual_witness_harness()` success logic |
| Write logs | `write_receipt_log()` |
| Write comparison report | `write_comparison_report()` |
| Detect non-determinism | external wrapper comparing two harness runs |

## Implementation Order

1. Harness core: pseudocode to real code in target language.
2. CLI wrapper implementing this spec.
3. Integration test: `PR_256` plus `PR_257` must exit `0`.

## Constitutional Lock

```json
{
  "minimal_test_vector": ["PR_256", "PR_257"],
  "red_path": "FAIL_CLOSED_WITHOUT_RECEIPT",
  "green_path": "PASS_WITH_VALID_LINEAGE",
  "proof": "SAME_INVARIANT_SET_HANDLED_BOTH_PATHS",
  "status": "SELF_AUDITING_GOVERNANCE_MEMBRANE",
  "authority": false
}
```
