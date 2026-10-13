# ALMS Contract Creation Manual — GitHub → Base → Zora

**Status:** Draft manual for disciplined contract creation.

This manual exists to prevent ghost anchors.

A transaction hash is not enough. A contract is only treated as created when the deployment transaction is successful and the deployed contract address is verified from chain data.

## Operator identities

- Root identity: `jaywisdom.eth`
- Base identity: `jaywisdom.base`
- Settlement layer: Base mainnet, chain ID `8453`
- Public/publishing layer: Zora, only after contract verification

## Rule 0 — No ghost anchors

Never claim any of the following without the required receipt:

| Claim | Required receipt |
|---|---|
| Contract deployed | deployment tx hash + deployed contract address |
| Contract verified | source verification URL or explorer verification success |
| ENS/Base identity linked | visible text record / profile link / verified pointer |
| Zora object published | Zora URL + contract/token address + tx hash |

## Stage 1 — GitHub proof first

Before touching a wallet, commit the source:

```bash
git status --short
forge build
```

Required repo artifacts:

- `contracts/<domain>/<ContractName>.sol`
- deployment script under `scripts/deploy/`
- docs/manual or README explaining the purpose
- no private keys, no `.env`, no RPC secrets

Minimum state:

```json
{
  "state": "SOURCE_READY",
  "repo": "jsonwisdom/AL",
  "secret_policy": "NO_PRIVATE_KEYS_IN_REPO"
}
```

## Stage 2 — Base deployment

Set secrets only in the local shell:

```bash
export BASE_RPC_URL="YOUR_BASE_MAINNET_RPC"
export PRIVATE_KEY="0xYOUR_DEPLOYER_PRIVATE_KEY"
```

Run dry build:

```bash
forge build
```

Deploy:

```bash
forge script scripts/deploy/<DeployScript>.s.sol:<DeployContract> \
  --rpc-url "$BASE_RPC_URL" \
  --broadcast \
  --chain-id 8453 \
  -vvvv | tee _truth/<domain>/mainnet/deploy.log
```

## Stage 3 — Extract receipts

Required fields:

```json
{
  "chain_id": 8453,
  "network": "base",
  "deployment_tx_hash": "0x...",
  "contract_address": "0x...",
  "deployer": "0x...",
  "operator_identity": ["jaywisdom.base", "jaywisdom.eth"]
}
```

Commands:

```bash
grep -E "transactionHash|contractAddress|Deployed|NODEB_UPTIME_CONTRACT" _truth/<domain>/mainnet/deploy.log
sha256sum _truth/<domain>/mainnet/deploy.log > _truth/<domain>/mainnet/deploy.log.sha256
```

If the deployed contract address is missing, do not promote. Use BaseScan or `cast receipt` to extract it.

```bash
cast receipt 0xTX_HASH --rpc-url "$BASE_RPC_URL"
```

## Stage 4 — Verify the contract

Use explorer verification only after the address is confirmed.

```bash
forge verify-contract \
  --chain-id 8453 \
  --watch \
  0xCONTRACT_ADDRESS \
  contracts/<domain>/<ContractName>.sol:<ContractName> \
  --etherscan-api-key "$BASESCAN_API_KEY"
```

Required receipt:

```json
{
  "contract_address": "0x...",
  "source_verified": true,
  "explorer": "BaseScan",
  "verification_url": "https://basescan.org/address/0x...#code"
}
```

## Stage 5 — ENS / Basename pointer

ENS and Basename are pointer layers, not the trust boundary.

Acceptable pointers:

- contract address
- GitHub commit URL
- deployment receipt JSON URL
- BaseScan address URL

Do not claim ENS complete unless the text/profile record is visibly set.

## Stage 6 — Zora publishing layer

Zora is used only after Base contract creation is verified.

Required Zora receipts:

```json
{
  "zora_url": "https://zora.co/...",
  "zora_contract_or_token": "0x...",
  "mint_or_publish_tx": "0x...",
  "source_contract": "0x...",
  "source_network": "base"
}
```

Zora rule:

- receipt ≠ deed
- tx hash ≠ contract unless the explorer confirms contract creation
- public caption must not overclaim

## Promotion gates

| Gate | Status required |
|---|---|
| Source committed | PASS |
| Build passes | PASS |
| Deployment tx exists | PASS |
| Contract address confirmed | PASS |
| Receipt stored | PASS |
| Optional explorer verification | PASS or DEFERRED |
| Optional Zora publish | PASS or DEFERRED |

Final ALMS state format:

```json
{
  "artifact": "CONTRACT_CREATED",
  "chain_id": 8453,
  "network": "base",
  "contract_address": "0x...",
  "deployment_tx_hash": "0x...",
  "github_commit": "...",
  "operator_identity": ["jaywisdom.base", "jaywisdom.eth"],
  "status": "VERIFIED_CONTRACT_ADDRESS"
}
```

## Hard stop conditions

Stop immediately if:

- contract address is unknown
- transaction failed
- source file differs from deployed source
- private key appears in repo
- Zora publish happens before Base contract address confirmation

## Node B current state

```json
{
  "artifact": "NODEB_UPTIME",
  "deployment_tx_hash": "0xefcbcb81699322ce64c958d7556d4eaf38b21a2276851693f53f790397529e45",
  "contract_address": null,
  "status": "TX_HASH_RECEIVED__AWAITING_CONTRACT_ADDRESS_CONFIRMATION"
}
```

Next required Node B receipt: deployed contract address from Base transaction receipt.
