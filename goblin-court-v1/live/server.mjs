import express from "express";
import { createRequire } from "node:module";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const require = createRequire(import.meta.url);
const { mayServePromptPack } = require("../payment/gate_003.js");
const promptPack = require("../fixtures/mn-stearns-003/prompt_pack_unit.json");

const REQUIRED = Object.freeze({
  docket_id: process.env.GC_DOCKET_ID || "MN-STEARNS-003",
  receipt_id: process.env.GC_RECEIPT_ID || "r_mn_stearns_003_v1",
  nutrition_score: Number(process.env.GC_NUTRITION_SCORE || 78),
  replay_url: process.env.GC_REPLAY_URL || "https://goblin.court/replay/mn-stearns-003",
  builder_code: process.env.GC_BUILDER_CODE || "bc_j1200j64"
});

const PORT = Number(process.env.PORT || 4021);
const NETWORK = process.env.GC_X402_NETWORK || "eip155:84532";
const FACILITATOR_URL = process.env.GC_X402_FACILITATOR_URL || "https://x402.org/facilitator";
const PRICE = process.env.GC_X402_PRICE || "$2.00";
const PAY_TO = process.env.GC_X402_PAY_TO;
const ROUTE = "/api/mn-stearns-003/prompt-pack";

if (!PAY_TO || PAY_TO === "0xYourReceivingWalletAddress") {
  throw new Error("GC_X402_PAY_TO must be set to a receiving wallet address before starting the live server.");
}

const app = express();

const facilitatorClient = new HTTPFacilitatorClient({
  url: FACILITATOR_URL
});

const resourceServer = new x402ResourceServer(facilitatorClient)
  .register(NETWORK, new ExactEvmScheme());

app.get("/health", (_req, res) => {
  res.json({
    ok: true,
    service: "goblin-court-v1-live-003",
    docket_id: REQUIRED.docket_id,
    receipt_id: REQUIRED.receipt_id,
    builder_code: REQUIRED.builder_code,
    network: NETWORK,
    authority: false,
    truth_claims: "prohibited"
  });
});

app.use(
  paymentMiddleware(
    {
      [`GET ${ROUTE}`]: {
        accepts: [
          {
            scheme: "exact",
            price: PRICE,
            network: NETWORK,
            payTo: PAY_TO
          }
        ],
        description: "Goblin Court MN-STEARNS-003 paid Prompt Pack Unit",
        mimeType: "application/json"
      }
    },
    resourceServer
  )
);

app.get(ROUTE, (_req, res) => {
  // If this route is reached, the x402 middleware accepted the payment for this resource.
  // The local lineage gate still decides whether the paid artifact is safe to serve.
  const paymentContext = {
    payment_valid: true,
    builder_code: REQUIRED.builder_code,
    docket_id: REQUIRED.docket_id,
    receipt_id: REQUIRED.receipt_id,
    nutrition_score: REQUIRED.nutrition_score,
    replay_url: REQUIRED.replay_url
  };

  const result = mayServePromptPack(paymentContext, promptPack);

  if (!result.ok) {
    return res.status(403).json({
      error: "paid_artifact_gate_failed",
      payment_errors: result.payment_errors,
      prompt_pack_errors: result.prompt_pack_errors
    });
  }

  return res.json(promptPack);
});

app.listen(PORT, () => {
  console.log(`Goblin Court live 003 server listening on port ${PORT}`);
  console.log(`Protected route: GET ${ROUTE}`);
  console.log(`Network: ${NETWORK}`);
  console.log(`Price: ${PRICE}`);
});
