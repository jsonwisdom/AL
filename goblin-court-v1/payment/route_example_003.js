/*
 * Goblin Court v1 — MN-STEARNS-003 route example
 *
 * This is a framework-neutral example showing where live x402 verification
 * attaches before serving PROMPT_PACK_UNIT_V0_1.
 *
 * It intentionally does not import a live x402 package because this repo does
 * not yet define an application runtime or package manager boundary.
 */

const { mayServePromptPack } = require("./gate_003");

function paymentRequiredResponse() {
  return {
    status: 402,
    body: {
      error: "payment_required",
      boundary: "PAYMENT_BOUNDARY_V0_1",
      builder_code: "bc_j1200j64",
      docket_id: "MN-STEARNS-003",
      receipt_id: "r_mn_stearns_003_v1",
      nutrition_score: 78,
      replay_url: "https://goblin.court/replay/mn-stearns-003",
      output: "PROMPT_PACK_UNIT_V0_1",
      artifact_count: 7,
      authority: false,
      truth_claims: "prohibited"
    }
  };
}

function forbiddenResponse(result) {
  return {
    status: 403,
    body: {
      error: "paid_artifact_gate_failed",
      payment_errors: result.payment_errors,
      prompt_pack_errors: result.prompt_pack_errors
    }
  };
}

function okResponse(promptPack) {
  return {
    status: 200,
    body: promptPack
  };
}

/*
 * Production adapter contract:
 *
 * async function verifyLivePayment(request) {
 *   // Attach official x402/facilitator verification here.
 *   // Must return:
 *   // {
 *   //   payment_valid: true,
 *   //   builder_code: "bc_j1200j64",
 *   //   docket_id: "MN-STEARNS-003",
 *   //   receipt_id: "r_mn_stearns_003_v1",
 *   //   nutrition_score: 78,
 *   //   replay_url: "https://goblin.court/replay/mn-stearns-003"
 *   // }
 * }
 */

async function handlePromptPackRequest({ paymentContext, promptPack }) {
  if (!paymentContext || paymentContext.payment_valid !== true) {
    return paymentRequiredResponse();
  }

  const result = mayServePromptPack(paymentContext, promptPack);
  if (!result.ok) {
    return forbiddenResponse(result);
  }

  return okResponse(promptPack);
}

module.exports = {
  paymentRequiredResponse,
  forbiddenResponse,
  okResponse,
  handlePromptPackRequest
};
