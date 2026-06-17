import "dotenv/config";
import { CdpClient } from "@coinbase/cdp-sdk";
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { createHash } from "crypto";

const RECEIPT_013 = "receipts/013/RECEIPT_013_SETTLEMENT_STAGED.json";
const RECEIPT_014 = "receipts/014/RECEIPT_014_SETTLEMENT_CONFIRMED.json";
const EXPECTED_013_SHA256 = "3b8c1bb6272707a68c39ef0454e5680474dd0a026b2411bbfaed10b8cf3250fc";
const SETTLEMENT_HASH = "d49a45a82729bdb1692fc9a62d156a87138c7ce9f1e7dba5b951a6ecb0c1acae";
const SELF = "0xA5a5491bCa93dD4C076e4906e79E7673F4A5A142";
const DATA = "0x" + SETTLEMENT_HASH;

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

for (const k of ["CDP_API_KEY_ID", "CDP_API_KEY_SECRET", "CDP_WALLET_SECRET"]) {
  if (!process.env[k]) throw new Error(`${k} missing`);
}

const actual013 = sha256(RECEIPT_013);
if (actual013 !== EXPECTED_013_SHA256) throw new Error(`Receipt 013 hash mismatch: ${actual013}`);

const staged = JSON.parse(readFileSync(RECEIPT_013, "utf8"));
if (staged.status !== "STAGED_NOT_BROADCAST") throw new Error("Receipt 013 not staged");
if (staged.settlement_hash !== SETTLEMENT_HASH) throw new Error("Settlement hash mismatch");
if (staged.anchor_encoding !== "RAW_BYTES32_CALLDATA") throw new Error("Wrong anchor encoding");
if (staged.anchor_plan?.data !== DATA) throw new Error("Calldata mismatch");
if (staged.anchor_plan?.to !== SELF) throw new Error("Self address mismatch");
if (String(staged.anchor_plan?.value) !== "0") throw new Error("Value must be 0");

const cdp = new CdpClient();

const sent = await cdp.evm.sendTransaction({
  network: "base",
  transaction: { to: SELF, value: "0", data: DATA }
});

const txHash = sent.transactionHash;
console.log("TX_SENT", txHash);

const receipt = await cdp.evm.waitForTransactionReceipt({
  network: "base",
  transactionHash: txHash
});

if (receipt.status !== "success" && receipt.status !== 1) {
  throw new Error("Base transaction failed");
}

const block = await cdp.evm.getBlock({
  network: "base",
  blockNumber: receipt.blockNumber
});

mkdirSync("receipts/014", { recursive: true });

const out = {
  proof: "RECEIPT_014_SETTLEMENT_CONFIRMED_V1",
  episode: "004",
  parent_receipt_013_sha256: EXPECTED_013_SHA256,
  settlement_hash: SETTLEMENT_HASH,
  anchor_encoding: "RAW_BYTES32_CALLDATA",
  chain: "base",
  chain_id: 8453,
  tx_hash: txHash,
  block_number: receipt.blockNumber.toString(),
  block_timestamp_utc: new Date(Number(block.timestamp) * 1000).toISOString(),
  to: SELF,
  value: "0",
  data: DATA,
  gas_used: receipt.gasUsed.toString(),
  status: "SETTLEMENT_CONFIRMED",
  funds_moved: "NO_VALUE_TRANSFER_GAS_ONLY",
  secrets_printed: "NO",
  no_fake_green: "ACTIVE"
};

const canonical = JSON.stringify(out, null, 2);
out.fileHash = createHash("sha256").update(canonical).digest("hex");

writeFileSync(RECEIPT_014, JSON.stringify(out, null, 2) + "\n");
console.log("RECEIPT_014_CREATED", RECEIPT_014);
console.log("FILE_HASH", out.fileHash);
