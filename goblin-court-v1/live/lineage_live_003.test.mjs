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

const { createApp, getLiveConfig, ROUTE } = await import("./server.mjs");

assert.ok(createApp);
assert.equal(typeof createApp, "function");
assert.equal(ROUTE, "/api/mn-stearns-003/prompt-pack");

const env = {
  PORT: "4021",
  GC_X402_NETWORK: "eip155:84532",
  GC_X402_FACILITATOR_URL: "https://x402.org/facilitator",
  GC_X402_PAY_TO: "0x0000000000000000000000000000000000000001",
  GC_X402_PRICE: "$2.00",
  GC_BUILDER_CODE: "bc_j1200j64",
  GC_DOCKET_ID: "MN-STEARNS-003",
  GC_RECEIPT_ID: "r_mn_stearns_003_v1",
  GC_NUTRITION_SCORE: "78",
  GC_REPLAY_URL: "https://goblin.court/replay/mn-stearns-003"
};

const config = getLiveConfig(env);
assert.equal(config.network, "eip155:84532");
assert.equal(config.builder_code, "bc_j1200j64");
assert.equal(config.pay_to, "0x0000000000000000000000000000000000000001");

const created = createApp(env);
assert.ok(created.app);
assert.equal(created.config.docket_id, "MN-STEARNS-003");
assert.equal(created.config.receipt_id, "r_mn_stearns_003_v1");
assert.equal(created.config.nutrition_score, 78);
assert.equal(created.config.replay_url, "https://goblin.court/replay/mn-stearns-003");

console.log("PASS live lineage fixture test");
