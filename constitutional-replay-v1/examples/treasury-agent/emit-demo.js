import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { loadPolicy } from "../../dist/src/policy.js";
import { interpretPolicy } from "../../dist/src/interpreter.js";
import { emitReceipt } from "../../dist/src/receipt.js";
import { replayReceipt } from "../../dist/src/replay.js";
import { emitBatch, summarizeReceipt } from "../../dist/src/batch.js";
import { canonicalHash } from "../../dist/src/hash.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const root = __dirname;
const policyPath = path.join(root, "policies", "treasury-basic-v1.json");
const receiptsDir = path.join(root, "receipts");
const summariesDir = path.join(root, "summaries");
const batchesDir = path.join(root, "batches");
const replayDir = path.join(root, "replay");

for (const dir of [receiptsDir, summariesDir, batchesDir, replayDir]) {
  fs.mkdirSync(dir, { recursive: true });
}

const policyRaw = JSON.parse(fs.readFileSync(policyPath, "utf8"));
const policy = loadPolicy(policyRaw);
const interpreter_hash = canonicalHash({ interpreter: "policy.v1", version: "replay.v1" });

const successInput = {
  action: "transfer_usdc",
  amount: "50",
  recipient: "0x1111111111111111111111111111111111111111"
};

const refusalInput = {
  action: "transfer_usdc",
  amount: "50000",
  recipient: "0x2222222222222222222222222222222222222222"
};

const successVerdict = interpretPolicy(policy, successInput);
const refusalVerdict = interpretPolicy(policy, refusalInput);

const successReceipt = emitReceipt({
  policy,
  interpreter_hash,
  input: successInput,
  action: successInput.action,
  verdict: successVerdict
});

const refusalReceipt = emitReceipt({
  policy,
  interpreter_hash,
  input: refusalInput,
  action: refusalInput.action,
  verdict: refusalVerdict
});

fs.writeFileSync(
  path.join(receiptsDir, "success-001.json"),
  JSON.stringify(successReceipt, null, 2) + "\n"
);

fs.writeFileSync(
  path.join(receiptsDir, "refusal-001.json"),
  JSON.stringify(refusalReceipt, null, 2) + "\n"
);

const batchId = "batch-001";
const summaries = [
  summarizeReceipt(successReceipt, batchId),
  summarizeReceipt(refusalReceipt, batchId)
];

fs.writeFileSync(
  path.join(summariesDir, "summaries.json"),
  JSON.stringify(summaries, null, 2) + "\n"
);

const batch = emitBatch(batchId, [successReceipt, refusalReceipt]);
fs.writeFileSync(
  path.join(batchesDir, "batch-001.json"),
  JSON.stringify(batch, null, 2) + "\n"
);

const replayResult = replayReceipt({
  receipt: refusalReceipt,
  policy: policyRaw,
  input: refusalInput,
  interpreter_hash
});

fs.writeFileSync(
  path.join(replayDir, "refusal-001.replay.json"),
  JSON.stringify(replayResult, null, 2) + "\n"
);

console.log("REPLAY RESULT:");
console.log(JSON.stringify(replayResult, null, 2));

if (replayResult.replay_status !== "REFUSAL_CONFIRMED") {
  process.exit(1);
}

console.log("SUCCESS_CONFIRMED receipt=examples/treasury-agent/receipts/success-001.json");
console.log("REFUSAL_CONFIRMED receipt=examples/treasury-agent/receipts/refusal-001.json");
console.log("REPLAY_RESULT=examples/treasury-agent/replay/refusal-001.replay.json");
console.log("BATCH=examples/treasury-agent/batches/batch-001.json");
console.log(`MERKLE_ROOT=${batch.merkle_root}`);
console.log(`INTERPRETER_HASH=${interpreter_hash}`);
console.log("WITNESS_STATUS=NOT_CHECKED");