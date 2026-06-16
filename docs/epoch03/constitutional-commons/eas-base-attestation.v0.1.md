# Epoch03 EAS/Base Attestation Payload v0.1

## Purpose

This document specifies the logical attestation payload for anchoring Epoch03 lineage on Base through EAS.

The attestation anchors lineage, not UI content.
The chain record is a publication receipt, not the source of truth.

## Logical Schema

```json
{
  "project": "string",
  "epoch": "string",
  "lineage_root": "string",
  "doctrine_root": "string",
  "fsm_root": "string",
  "validator_version": "string",
  "engine_contract_version": "string",
  "receipt_root": "string",
  "taxonomy_version": "string",
  "fixtures_survived": "uint256",
  "classes_covered": "uint256",
  "authors": "uint256",
  "harness_hash": "string",
  "repo_ref": "string",
  "commit": "string",
  "timestamp": "uint64"
}
```

## Canonical Hashing

All JSON objects are hashed using Epoch03 canonical JSON:

```text
hash(x) = sha256:hex(SHA-256(canonical_json(x)))
```

Canonical JSON requirements:

- UTF-8
- sorted object keys
- no insignificant whitespace
- arrays preserve order
- strings are JSON escaped by the runtime encoder

## Receipt Root Layout

The receipt root binds the current epoch surfaces.

### Leaves

```text
L0 = doctrine_root
L1 = fsm_root
L2 = validator_version_hash
L3 = taxonomy_version_hash
L4 = harness_hash
```

Where:

```text
validator_version_hash = hash("validator_version:" + validator_version)
taxonomy_version_hash = hash("taxonomy_version:" + taxonomy_version)
```

### Pair Hashing

```text
P01 = hash("receipt_root:v0.1:left=" + L0 + ";right=" + L1)
P23 = hash("receipt_root:v0.1:left=" + L2 + ";right=" + L3)
P44 = hash("receipt_root:v0.1:left=" + L4 + ";right=" + L4)
P0123 = hash("receipt_root:v0.1:left=" + P01 + ";right=" + P23)
receipt_root = hash("receipt_root:v0.1:left=" + P0123 + ";right=" + P44)
```

## Lineage Root Layout

The lineage root binds the receipt chain back to genesis.

Each epoch receipt hash is:

```text
receipt_epochN_hash = hash(canonical_receipt_epochN_json)
```

For Epoch03 with prior epochs:

```text
lineage_root = hash("lineage_root:v0.1:" + receipt_genesis_hash + ":" + receipt_epoch01_hash + ":" + receipt_epoch02_hash + ":" + receipt_epoch03_hash)
```

If no prior epoch exists yet:

```text
lineage_root = hash("lineage_root:v0.1:" + receipt_epoch03_hash)
```

No epoch may be omitted.
No receipt may be reordered.
No receipt may be replaced without changing the lineage root.

## Harness Hash Layout

Harness hash binds refusal machinery, not UI.

```text
harness_hash = hash({
  "files": [
    {
      "path": "docs/epoch03/adversarial/harness.js",
      "hash": hash(file_bytes_utf8)
    },
    {
      "path": "docs/epoch03/adversarial/lineage-harness.js",
      "hash": hash(file_bytes_utf8)
    },
    {
      "path": "docs/epoch03/constitutional-commons/receipt-lineage.invariants.md",
      "hash": hash(file_bytes_utf8)
    }
  ]
})
```

File order is lexicographic by path.

## Example Logical Payload

```json
{
  "project": "jsonwisdom/AL",
  "epoch": "epoch03",
  "lineage_root": "sha256:LINEAGE_ROOT_HEX",
  "doctrine_root": "sha256:DOCTRINE_ROOT_HEX",
  "fsm_root": "sha256:FSM_ROOT_HEX",
  "validator_version": "epoch03-validator-rust@0.1.0",
  "engine_contract_version": "engine@1",
  "receipt_root": "sha256:RECEIPT_ROOT_HEX",
  "taxonomy_version": "adversarial.taxonomy@1",
  "fixtures_survived": 10,
  "classes_covered": 10,
  "authors": 7,
  "harness_hash": "sha256:HARNESS_HASH_HEX",
  "repo_ref": "https://github.com/jsonwisdom/AL/tree/epoch03-site",
  "commit": "GIT_COMMIT_SHA",
  "timestamp": 1715380000
}
```

## Verification Rule

A verifier must be able to:

1. clone `jsonwisdom/AL` at `commit`
2. recompute doctrine_root
3. recompute fsm_root
4. recompute harness_hash
5. recompute receipt_root
6. recompute lineage_root
7. run validator, adversarial harness, and lineage harness
8. confirm all values match the EAS/Base attestation payload

If any recomputation differs:

```text
TAINTED_ATTESTATION
```

## Constitutional Boundary

The on-chain record is not the authority.

The authority remains in:

- doctrine
- FSM
- validator
- harness
- receipts
- replayable lineage

The chain only records that a specific lineage state was published at a specific time by a specific attester.
