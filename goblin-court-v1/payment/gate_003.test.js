/*
 * Minimal Node test for the MN-STEARNS-003 paid artifact gate.
 * Run from repo root after checkout:
 * node goblin-court-v1/payment/gate_003.test.js
 */

const assert = require("assert");
const path = require("path");
const { mayServePromptPack, validatePromptPackUnit } = require("./gate_003");

const promptPack = require(path.join("..", "fixtures", "mn-stearns-003", "prompt_pack_unit.json"));

const validPaymentContext = {
  payment_valid: true,
  builder_code: "bc_j1200j64",
  docket_id: "MN-STEARNS-003",
  receipt_id: "r_mn_stearns_003_v1",
  nutrition_score: 78,
  replay_url: "https://goblin.court/replay/mn-stearns-003"
};

const promptPackResult = validatePromptPackUnit(promptPack);
assert.deepStrictEqual(promptPackResult, { ok: true, errors: [] });

const serveResult = mayServePromptPack(validPaymentContext, promptPack);
assert.deepStrictEqual(serveResult, {
  ok: true,
  payment_errors: [],
  prompt_pack_errors: []
});

const badPaymentContext = {
  ...validPaymentContext,
  payment_valid: false
};

const deniedResult = mayServePromptPack(badPaymentContext, promptPack);
assert.strictEqual(deniedResult.ok, false);
assert.ok(deniedResult.payment_errors.includes("payment_not_valid"));

const badPack = {
  ...promptPack,
  receipt_id: "wrong_receipt"
};

const badPackResult = mayServePromptPack(validPaymentContext, badPack);
assert.strictEqual(badPackResult.ok, false);
assert.ok(badPackResult.prompt_pack_errors.includes("mismatch:receipt_id"));

const shortPack = {
  ...promptPack,
  artifacts: {
    ...promptPack.artifacts
  }
};

delete shortPack.artifacts.headline_pack;

const shortPackResult = mayServePromptPack(validPaymentContext, shortPack);
assert.strictEqual(shortPackResult.ok, false);
assert.ok(shortPackResult.prompt_pack_errors.includes("artifact_count:6"));

console.log("PASS gate_003 fixture tests");
