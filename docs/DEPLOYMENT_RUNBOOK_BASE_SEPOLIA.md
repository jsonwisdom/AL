# Deployment Runbook — Base Sepolia

Status: CORRECTED_DEPLOYMENT_RUNBOOK_V1
Branch: root-law-machine-audit-v1
Chain ID: 84532
Root identity: jaywisdom.base

## Critical Correction

EAS and Schema Registry addresses are Ethereum addresses, not bytes32 values.

Do not use 32-byte zero-padded addresses such as:

```text
0x42000000000000000000000000000000000000000000000000000000000000000
```

That is invalid for `address` fields and must not be used for deployment wiring.

## Verified Base Sepolia EAS Wiring

```env
CHAIN_ID=84532
RPC_URL=https://sepolia.base.org
EAS_ADDRESS=0x4200000000000000000000000000000000000021
SCHEMA_REGISTRY_ADDRESS=0x4200000000000000000000000000000000000020
EIP712_PROXY_ADDRESS=0xAd64A04c20dDBbA7cBb0EcAe4823095B4adA5c57
INDEXER_ADDRESS=0x2C7BCE69D5Ee84EF73CC9286416F68E60F9A61b3
EASSCAN=https://base-sepolia.easscan.org
```

## Important

EAS and Schema Registry do not share the same address on Base Sepolia.

```text
EAS              = 0x4200000000000000000000000000000000000021
Schema Registry  = 0x4200000000000000000000000000000000000020
```

## Deployment Gate

Do not deploy until these are true:

```text
MigrationGuard.sol present
MigrationRelayerReputationOracle.sol present
forge test --match-contract MigrationGuardTest -vv passes
private key is local only, never committed
.env is local only, never committed
Base Sepolia ETH available for gas
```

## Environment Setup

```bash
cd AL
cp .env.base-sepolia.example .env
```

Local `.env` values:

```env
RPC_URL=https://sepolia.base.org
CHAIN_ID=84532
EAS_ADDRESS=0x4200000000000000000000000000000000000021
SCHEMA_REGISTRY_ADDRESS=0x4200000000000000000000000000000000000020
EIP712_PROXY_ADDRESS=0xAd64A04c20dDBbA7cBb0EcAe4823095B4adA5c57
INDEXER_ADDRESS=0x2C7BCE69D5Ee84EF73CC9286416F68E60F9A61b3
PRIVATE_KEY=<local_only_deployer_key>
```

## Test First

```bash
forge test --match-contract MigrationGuardTest -vv
```

Expected:

```text
9 passing tests
```

## Register Schemas

```bash
source .env

forge script script/RegisterSchemas.s.sol \
  --rpc-url "$RPC_URL" \
  --broadcast \
  -vvv
```

Capture:

```text
CONSTITUTIONAL_ROOT_SCHEMA_UID=0x...
MIGRATION_RECEIPT_SCHEMA_UID=0x...
```

## Compute Constitutional Hashes

Use the committed document bytes. Do not hash an editor buffer.

```bash
cast keccak "$(cat docs/jays-instrument.md)"
```

For binary-safe hashing, prefer a script that reads bytes exactly and emits the keccak256 digest.

## Deploy Oracle and Guard

Deploy order:

```text
1. MigrationRelayerReputationOracle
2. MigrationGuard with constitutionalRootUID and oracle address
3. Constitutional root attestation
4. Update docs/WIRING.md only after receipts exist
```

## Update WIRING.md After Deployment

Replace placeholders only after real receipts exist:

```env
VITE_CONSTITUTIONAL_ROOT_UID=0x<actual_root_uid>
VITE_MIGRATION_GUARD_ADDRESS=0x<actual_guard_address>
VITE_REPUTATION_ORACLE_ADDRESS=0x<actual_oracle_address>
VITE_EAS_ADDRESS=0x4200000000000000000000000000000000000021
VITE_CHAIN_ID=84532
```

## Prohibited Actions

```text
No tokenization
No trust scores
No silent confidence upgrade
No autonomous settlement
No deployment from CDN bytes
No deployment with bytes32-padded address values
No deployment before 9-vector tests pass
```

## Audit Verdict

BASE_SEPOLIA_RUNBOOK_CORRECTED

Address wiring fixed.
Deployment remains blocked until tests pass and real receipts exist.
