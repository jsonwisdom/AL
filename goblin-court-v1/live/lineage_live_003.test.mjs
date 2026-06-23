import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { mayServePromptPack } = require("../payment/gate_003.js");
const promptPack = require("../fixtures/mn-stearns-003/prompt_pack_unit.json");

const validPaymentContext = {
  payment_valid: true,
  builder_code: "bc_j1200j64",
  docket_id: "MN-STEARNS-003",
  receipt_id: "r_mn_stearns_003_v1",
  nutrition_score: 78,
  replay_url: "https://goblin.court/replay/mn-stearns-003"
};

const result = mayServePromptPack(validPaymentContext, promptPack);
assert.deepEqual(result, {
  ok: true,
  payment_errors: [],
  prompt_pack_errors: []
});

const wrongBuilderCode = {
  ...validPaymentContext,
  builder_code: "wrong_builder_code"
};

const denied = mayServePromptPack(wrongBuilderCode, promptPack);
assert.equal(denied.ok, false);
assert.ok(denied.payment_errors.includes("builder_code_mismatch"));

console.log("PASS live lineage fixture test");
