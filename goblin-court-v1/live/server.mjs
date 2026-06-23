import express from "express";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const require = createRequire(import.meta.url);
const { mayServePromptPack } = require("../payment/gate_003.js");
const promptPack = require("../fixtures/mn-stearns-003/prompt_pack_unit.json");

export const ROUTE = "/api/mn-stearns-003/prompt-pack";

export function getLiveConfig(env = process.env) {
  return Object.freeze({
    docket_id: env.GC_DOCKET_ID || "MN-STEARNS-003",
    receipt_id: env.GC_RECEIPT_ID || "r_mn_stearns_003_v1",
    nutrition_score: Number(env.GC_NUTRITION_SCORE || 78),
    replay_url: env.GC_REPLAY_URL || "https://goblin.court/replay/mn-stearns-003",
    builder_code: env.GC_BUILDER_CODE || "bc_j1200j64",
    port: Number(env.PORT || 4021),
    network: env.GC_X402_NETWORK || "eip155:84532",
    facilitator_url: env.GC_X402_FACILITATOR_URL || "https://x402.org/facilitator",
    price: env.GC_X402_PRICE || "$2.00",
    pay_to: env.GC_X402_PAY_TO
  });
}

export function assertLiveConfig(config) {
  if (!config.pay_to || config.pay_to === "0xYourReceivingWalletAddress") {
    throw new Error("GC_X402_PAY_TO must be set to a receiving wallet address before starting the live server.");
  }
}

export function createApp(env = process.env) {
  const config = getLiveConfig(env);
  assertLiveConfig(config);

  const app = express();

  const facilitatorClient = new HTTPFacilitatorClient({
    url: config.facilitator_url
  });

  const resourceServer = new x402ResourceServer(facilitatorClient)
    .register(config.network, new ExactEvmScheme());

  app.get("/health", (_req, res) => {
    res.json({
      ok: true,
      service: "goblin-court-v1-live-003",
      docket_id: config.docket_id,
      receipt_id: config.receipt_id,
      builder_code: config.builder_code,
      network: config.network,
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
              price: config.price,
              network: config.network,
              payTo: config.pay_to
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
      builder_code: config.builder_code,
      docket_id: config.docket_id,
      receipt_id: config.receipt_id,
      nutrition_score: config.nutrition_score,
      replay_url: config.replay_url
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

  return { app, config };
}

export function startServer(env = process.env) {
  const { app, config } = createApp(env);

  return app.listen(config.port, () => {
    console.log(`Goblin Court live 003 server listening on port ${config.port}`);
    console.log(`Protected route: GET ${ROUTE}`);
    console.log(`Network: ${config.network}`);
    console.log(`Price: ${config.price}`);
  });
}

const thisFile = fileURLToPath(import.meta.url);
const invokedFile = process.argv[1] ? resolve(process.argv[1]) : "";

if (thisFile === invokedFile) {
  startServer();
}
