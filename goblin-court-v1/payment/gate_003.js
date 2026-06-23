/*
 * Goblin Court v1 — MN-STEARNS-003 lineage gate
 *
 * Framework-neutral CommonJS module.
 * This file does not perform network settlement.
 * It validates that the paid artifact matches the signed payment boundary
 * before a route serves PROMPT_PACK_UNIT_V0_1.
 */

const REQUIRED = Object.freeze({
  docket_id: "MN-STEARNS-003",
  receipt_id: "r_mn_stearns_003_v1",
  replay_url: "https://goblin.court/replay/mn-stearns-003",
  nutrition_score: 78,
  builder_code: "bc_j1200j64",
  artifact_count: 7,
  schema: "PROMPT_PACK_UNIT_V0_1",
  authority: false,
  truth_claims: "prohibited"
});

const REQUIRED_ARTIFACT_KEYS = Object.freeze([
  "poster_prompt",
  "meme_prompt",
  "storyboard_prompt",
  "trading_card_prompt",
  "court_sketch_prompt",
  "tweet_thread",
  "headline_pack"
]);

function countArtifactUnits(artifacts) {
  if (!artifacts || typeof artifacts !== "object") return 0;
  return REQUIRED_ARTIFACT_KEYS.filter((key) => Object.prototype.hasOwnProperty.call(artifacts, key)).length;
}

function validatePromptPackUnit(promptPack) {
  const errors = [];

  if (!promptPack || typeof promptPack !== "object") {
    return { ok: false, errors: ["prompt_pack_missing"] };
  }

  for (const [key, expected] of Object.entries(REQUIRED)) {
    if (key === "artifact_count") continue;
    if (promptPack[key] !== expected) {
      errors.push(`mismatch:${key}`);
    }
  }

  const artifactCount = countArtifactUnits(promptPack.artifacts);
  if (artifactCount !== REQUIRED.artifact_count) {
    errors.push(`artifact_count:${artifactCount}`);
  }

  const footer = String(promptPack.lineage_footer || "");
  for (const token of [REQUIRED.docket_id, REQUIRED.receipt_id, String(REQUIRED.nutrition_score), REQUIRED.replay_url]) {
    if (!footer.includes(token)) {
      errors.push(`lineage_footer_missing:${token}`);
    }
  }

  const headlineMetadata = promptPack.artifacts && promptPack.artifacts.headline_metadata;
  if (!headlineMetadata) {
    errors.push("headline_metadata_missing");
  } else {
    for (const key of ["docket_id", "receipt_id", "nutrition_score", "replay_url"]) {
      if (headlineMetadata[key] !== REQUIRED[key]) {
        errors.push(`headline_metadata_mismatch:${key}`);
      }
    }
  }

  return {
    ok: errors.length === 0,
    errors
  };
}

function validatePaymentContext(paymentContext) {
  const errors = [];

  if (!paymentContext || typeof paymentContext !== "object") {
    return { ok: false, errors: ["payment_context_missing"] };
  }

  if (paymentContext.builder_code !== REQUIRED.builder_code) {
    errors.push("builder_code_mismatch");
  }

  if (paymentContext.docket_id !== REQUIRED.docket_id) {
    errors.push("docket_id_mismatch");
  }

  if (paymentContext.receipt_id !== REQUIRED.receipt_id) {
    errors.push("receipt_id_mismatch");
  }

  if (paymentContext.replay_url !== REQUIRED.replay_url) {
    errors.push("replay_url_mismatch");
  }

  if (paymentContext.nutrition_score !== REQUIRED.nutrition_score) {
    errors.push("nutrition_score_mismatch");
  }

  if (paymentContext.payment_valid !== true) {
    errors.push("payment_not_valid");
  }

  return {
    ok: errors.length === 0,
    errors
  };
}

function mayServePromptPack(paymentContext, promptPack) {
  const payment = validatePaymentContext(paymentContext);
  const pack = validatePromptPackUnit(promptPack);

  return {
    ok: payment.ok && pack.ok,
    payment_errors: payment.errors,
    prompt_pack_errors: pack.errors
  };
}

module.exports = {
  REQUIRED,
  REQUIRED_ARTIFACT_KEYS,
  validatePromptPackUnit,
  validatePaymentContext,
  mayServePromptPack
};
