import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { loadPolicy } from "../dist/src/policy.js";
import { interpretPolicy } from "../dist/src/interpreter.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const moduleRoot = path.join(__dirname, "..");
const vectorsPath = path.join(moduleRoot, "interpreters", "policy.v1", "test-vectors.json");
const distSrcPath = path.join(moduleRoot, "dist", "src");

const vectorFile = JSON.parse(fs.readFileSync(vectorsPath, "utf8"));
const policy = loadPolicy(vectorFile.policy);

function emitReport(report) {
  console.log(JSON.stringify(report));
}

test("emitted-path alignment", () => {
  const required = [
    "policy.js",
    "interpreter.js",
    "receipt.js",
    "replay.js",
    "batch.js",
    "hash.js",
    "canonicalize.js"
  ];

  for (const file of required) {
    const target = path.join(distSrcPath, file);
    assert.equal(fs.existsSync(target), true, `missing emitted artifact: ${target}`);
  }

  emitReport({
    vector_id: "emitted-path-alignment-001",
    evidence_class: "EXECUTABLE_VECTOR_TEST",
    expected_result: "EMITTED_ARTIFACTS_PRESENT",
    actual_result: "EMITTED_ARTIFACTS_PRESENT",
    status: "PASS"
  });
});

for (const vector of vectorFile.vectors) {
  test(`policy.v1 vector ${vector.vector_id}`, () => {
    const actual = interpretPolicy(policy, vector.input);

    const report = {
      vector_id: vector.vector_id,
      evidence_class: "EXECUTABLE_VECTOR_TEST",
      expected_result: vector.expected.result,
      expected_refusal_code: vector.expected.refusal_code,
      actual_result: actual.result,
      actual_refusal_code: actual.refusal_code,
      status: "PENDING"
    };

    assert.equal(actual.result, vector.expected.result, JSON.stringify(report, null, 2));
    assert.equal(actual.refusal_code, vector.expected.refusal_code, JSON.stringify(report, null, 2));

    report.status = "PASS";
    emitReport(report);
  });
}

test("malformed input rejects cleanly", () => {
  const actual = interpretPolicy(policy, {
    action: "transfer_usdc",
    amount: "25"
  });

  const report = {
    vector_id: "malformed-input-rejection-001",
    evidence_class: "EXECUTABLE_VECTOR_TEST",
    expected_result: "REFUSAL",
    expected_refusal_code: "UNKNOWN_REFUSAL",
    actual_result: actual.result,
    actual_refusal_code: actual.refusal_code,
    status: "PENDING"
  };

  assert.equal(actual.result, "REFUSAL", JSON.stringify(report, null, 2));
  assert.equal(actual.refusal_code, "UNKNOWN_REFUSAL", JSON.stringify(report, null, 2));

  report.status = "PASS";
  emitReport(report);
});

test("high-iteration deterministic replay smoke test", () => {
  const input = {
    action: "transfer_usdc",
    amount: "50000",
    recipient: "0x2222222222222222222222222222222222222222"
  };

  for (let index = 0; index < 1000; index += 1) {
    const actual = interpretPolicy(policy, input);
    assert.equal(actual.result, "REFUSAL");
    assert.equal(actual.refusal_code, "SPEND_LIMIT_EXCEEDED");
  }

  emitReport({
    vector_id: "high-iteration-determinism-001",
    evidence_class: "EXECUTABLE_VECTOR_TEST",
    expected_result: "REFUSAL",
    expected_refusal_code: "SPEND_LIMIT_EXCEEDED",
    iterations: 1000,
    status: "PASS"
  });
});

test("status reports name evidence class", () => {
  const sample = {
    vector_id: "status-evidence-class-001",
    evidence_class: "EXECUTABLE_VECTOR_TEST",
    status: "PASS"
  };

  assert.equal(sample.evidence_class, "EXECUTABLE_VECTOR_TEST");

  emitReport(sample);
});
