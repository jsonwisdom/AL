# ALMS Base 2026-04 v2 Verifier Playbook

Status: SAFE_VERIFICATION_ONLY  
Network: Base / chain_id 8453  
Signing: Browser-wallet only  
Terminal role: verify only

## Boundary

Browser signs. Terminal verifies. GitHub shows receipts. ENS anchors identity.

This playbook describes how to verify ALMS Base 2026-04 v2 witness artifacts without private keys, terminal signing, broadcast commands, or RPC writes.

## Artifacts

- Preview file: `_truth/attest/base_alms_attest_2026_04_v2_preview_*.txt`
- Witness file: `_truth/attest/witness/base_alms_root_2026_04_v2_witness.json`
- Patched witness file: `_truth/attest/witness/base_alms_root_2026_04_v2_witness.with_tx.json`
- Extractor: `scripts/extract_base_alms_root_witness_2026_04_v2.sh`
- TX patcher: `scripts/patch_witness_tx.sh`
- Static verifier: `scripts/verify_base_alms_root_witness_2026_04_v2.sh`

## Required preview lines

The preview file must contain all seven required lines:

```text
schema_uid=
merkle_root=
func_sig=
request=
data=
NO_SIGNER_USED
NO_TX_SENT
```

If any line is absent, the witness is not valid for this verifier profile.

## Build witness from preview

```bash
cd AL
bash scripts/extract_base_alms_root_witness_2026_04_v2.sh \
  _truth/attest/base_alms_attest_2026_04_v2_preview_*.txt
```

Expected result:

```text
WITNESS_OK file=... hash=... status=NOT_SUBMITTED
```

## Patch submitted TX hash, if browser transaction exists

This is JSON-only mutation. It does not contact chain.

```bash
cd AL
bash scripts/patch_witness_tx.sh \
  _truth/attest/witness/base_alms_root_2026_04_v2_witness.json \
  0xYOUR_TX_HASH
```

Expected result:

```text
WITNESS_TX_PATCHED input=... output=... tx_hash=... hash=... status=SUBMITTED
```

## Verify preview and witness consistency

```bash
cd AL
bash scripts/verify_base_alms_root_witness_2026_04_v2.sh \
  _truth/attest/base_alms_attest_2026_04_v2_preview_*.txt \
  _truth/attest/witness/base_alms_root_2026_04_v2_witness.json
```

Expected result:

```text
VERIFIER_OK witness=... hash=... status=NOT_SUBMITTED
```

For a patched witness:

```bash
bash scripts/verify_base_alms_root_witness_2026_04_v2.sh \
  _truth/attest/base_alms_attest_2026_04_v2_preview_*.txt \
  _truth/attest/witness/base_alms_root_2026_04_v2_witness.with_tx.json
```

Expected result:

```text
VERIFIER_OK witness=... hash=... status=SUBMITTED
```

## Prove tx-only mutation

```bash
jq -cS 'del(.tx)' _truth/attest/witness/base_alms_root_2026_04_v2_witness.json | sha256sum
jq -cS 'del(.tx)' _truth/attest/witness/base_alms_root_2026_04_v2_witness.with_tx.json | sha256sum
```

The two hashes must match exactly.

## External Basescan checklist for CONFIRMED

This repository does not declare CONFIRMED without external observation.

An auditor may manually inspect Basescan and check:

1. Transaction status is Success.
2. Network is Base.
3. Transaction hash equals `tx.tx_hash`.
4. Contract target matches expected EAS contract.
5. Calldata / method corresponds to witness `attestation.func_sig` and `attestation.request`.
6. Block number and timestamp are visible.
7. No private key or terminal signing evidence exists in the repo path.

Only after external observation should a separate confirmation artifact be created. Do not mutate the original intent fields.

## Failure codes

| Code | Meaning |
|---|---|
| `FAIL missing_required_line=*` | Preview file lacks a required line. |
| `FAIL witness_missing_*` | Witness lacks a required JSON field. |
| `FAIL schema_uid_mismatch` | Preview schema UID differs from witness. |
| `FAIL merkle_root_mismatch` | Preview Merkle root differs from witness. |
| `FAIL func_sig_mismatch` | Preview function signature differs from witness. |
| `FAIL request_mismatch` | Preview request differs from witness. |
| `FAIL data_mismatch` | Preview data differs from witness. |
| `FAIL unsupported_chain_id=*` | Witness is not Base chain_id 8453. |
| `FAIL unsupported_tx_status=*` | TX status is outside allowed verifier states. |
| `FAIL invalid_tx_hash_format=*` | Patched TX hash is malformed. |
| `FAIL non_tx_fields_mutated` | Patched witness changed non-tx content. |

## Non-claims

This verifier does not prove transaction success, finality, signer identity, or contract state. It proves only that the witness content matches the preview intent and that any patched TX reference is structurally valid and isolated to `tx.*`.
