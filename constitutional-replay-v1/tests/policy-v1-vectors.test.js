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

const vectorFile = JSON.parse(fs.readFileSync(vectorsPath, "utf8"));
const policy = loadPolicy(vectorFile.policy);

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
    console.log(JSON.stringify(report));
  });
}
