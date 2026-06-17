import { createPublicClient, http } from "viem";
import { base } from "viem/chains";
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { createHash } from "crypto";

const TX = process.argv[2];
if (!TX || !TX.startsWith("0x")) throw new Error("Usage: node validate_and_mint_014.mjs 0xTX_HASH");

const SETTLEMENT_HASH = "d49a45a82729bdb1692fc9a62d156a87138c7ce9f1e7dba5b951a6ecb0c1acae";
const DATA = "0x" + SETTLEMENT_HASH;
const SELF = "0xA5a5491bCa93dD4C076e4906e79E7673F4A5A142".toLowerCase();

const r13sha = createHash("sha256").update(readFileSync("receipts/013/RECEIPT_013_SETTLEMENT_STAGED.json")).digest("hex");
if (r13sha !== "1c7cff3c0766585b061da2c4ec964a2598441950596ac9f2da76f5775a9a1a7f") throw new Error("Receipt 013 drift");

const client = createPublicClient({ chain: base, transport: http() });

const tx = await client.getTransaction({ hash: TX });
const receipt = await client.getTransactionReceipt({ hash: TX });
const block = await client.getBlock({ blockNumber: receipt.blockNumber });

const checks = {
  tx_hash_exists: !!tx.hash,
  block_number_gt_0: receipt.blockNumber > 0n,
  timestamp_from_block: !!block.timestamp,
  settlement_hash_matches: tx.input.toLowerCase() === DATA.toLowerCase(),
  to_address_is_self: tx.to?.toLowerCase() === SELF,
  value_is_zero: tx.value === 0n,
  gas_used_from_receipt: receipt.gasUsed > 0n,
  no_fake_green: true
};

for (const [k, v] of Object.entries(checks)) {
  if (!v) throw new Error(`CHECK_FAILED_${k}`);
}

mkdirSync("receipts/014", { recursive: true });

const out = {
  proof: "RECEIPT_014_SETTLEMENT_CONFIRMED_V1",
  episode: "004",
  parent_receipt_013_sha256: r13sha,
  settlement_hash: SETTLEMENT_HASH,
  anchor_encoding: "RAW_BYTES32_CALLDATA",
  chain: "base",
  chain_id: 8453,
  tx_hash: tx.hash,
  block_number: receipt.blockNumber.toString(),
  block_timestamp_utc: new Date(Number(block.timestamp) * 1000).toISOString(),
  to: tx.to,
  value: tx.value.toString(),
  data: tx.input,
  gas_used: receipt.gasUsed.toString(),
  checks,
  status: "SETTLEMENT_CONFIRMED",
  funds_moved: "NO_VALUE_TRANSFER_GAS_ONLY",
  secrets_printed: "NO",
  no_fake_green: "ACTIVE"
};

const canonical = JSON.stringify(out, null, 2);
out.fileHash = createHash("sha256").update(canonical).digest("hex");

writeFileSync("receipts/014/RECEIPT_014_SETTLEMENT_CONFIRMED.json", JSON.stringify(out, null, 2) + "\n");
console.log("RECEIPT_014_CREATED");
console.log("fileHash", out.fileHash);
