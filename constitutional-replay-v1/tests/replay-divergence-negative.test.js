import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { canonicalHash } from "../dist/src/hash.js";
import { interpretPolicy } from "../dist/src/interpreter.js";
import { loadPolicy } from "../dist/src/policy.js";
import { emitReceipt } from "../dist/src/receipt.js";
import { replayReceipt } from "../dist/src/replay.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const moduleRoot = path.join(__dirname, "..");
const policyPath = path.join(moduleRoot, "examples", "treasury-agent", "policies", "treasury-basic-v1.json");

const policyRaw = JSON.parse(fs.readFileSync(policyPath, "utf8"));
const policy = loadPolicy(policyRaw);
const interpreter_hash = canonicalHash({ interpreter: "policy.v1", version: "replay.v1" });

const refusalInput = {
  action: "transfer_usdc",
  amount: "50000",
  recipient: "0x2222222222222222222222222222222222222222"
};

const refusalVerdict = interpretPolicy(policy, refusalInput);
const baseReceipt = emitReceipt({
  policy,
  interpreter_hash,
  input: refusalInput,
  action: refusalInput.action,
  verdict: refusalVerdict
});

function emitReport(report) {
  console.log(JSON.stringify(report));
}

function assertNegativeReplay({ vector_id, mutatedReceipt, input, expected_status, expected_failure_reason }) {
  const actual = replayReceipt({
    receipt: mutatedReceipt,
    policy: policyRaw,
    input,
    interpreter_hash
  });

  const report = {
    vector_id,
    evidence_class: "EXECUTABLE_NEGATIVE_VECTOR_TEST",
    expected_status,
    expected_failure_reason,
    actual_status: actual.replay_status,
    actual_failure_reason: actual.failure_reason,
    status: "PENDING"
  };

  assert.equal(actual.replay_status, expected_status, JSON.stringify(report, null, 2));
  assert.equal(actual.failure_reason, expected_failure_reason, JSON.stringify(report, null, 2));

  report.status = "PASS";
  emitReport(report);
}

test("policy-hash-mismatch-001", () => {
  assertNegativeReplay({
    vector_id: "policy-hash-mismatch-001",
    mutatedReceipt: {
      ...baseReceipt,
      policy_hash: baseReceipt.policy_hash.replace(/.$/, baseReceipt.policy_hash.endsWith("0") ? "1" : "0")
    },
    input: refusalInput,
    expected_status: "RECEIPT_REJECTED",
    expected_failure_reason: "POLICY_HASH_MISMATCH"
  });
});

test("input-hash-mismatch-001", () => {
  assertNegativeReplay({
    vector_id: "input-hash-mismatch-001",
    mutatedReceipt: baseReceipt,
    input: {
      ...refusalInput,
      amount: "50001"
    },
    expected_status: "RECEIPT_REJECTED",
    expected_failure_reason: "INPUT_HASH_MISMATCH"
  });
});

test("interpreter-hash-mismatch-001", () => {
  assertNegativeReplay({
    vector_id: "interpreter-hash-mismatch-001",
    mutatedReceipt: {
      ...baseReceipt,
      interpreter_hash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    },
    input: refusalInput,
    expected_status: "RECEIPT_REJECTED",
    expected_failure_reason: "INTERPRETER_HASH_MISMATCH"
  });
});

test("verdict-mismatch-001", () => {
  assertNegativeReplay({
    vector_id: "verdict-mismatch-001",
    mutatedReceipt: {
      ...baseReceipt,
      result: "SUCCESS",
      refusal_code: null
    },
    input: refusalInput,
    expected_status: "REPLAY_DIVERGENCE",
    expected_failure_reason: "VERDICT_MISMATCH"
  });
});

test("refusal-code-mismatch-001", () => {
  assertNegativeReplay({
    vector_id: "refusal-code-mismatch-001",
    mutatedReceipt: {
      ...baseReceipt,
      refusal_code: "ACTION_NOT_ALLOWED"
    },
    input: refusalInput,
    expected_status: "REPLAY_DIVERGENCE",
    expected_failure_reason: "VERDICT_MISMATCH"
  });
});
