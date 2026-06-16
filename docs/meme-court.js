// Meme Court Charge Detector Engine
// Status: v0 design implementation for GitHub Pages
// Truth boundary: ALMS receipts + repo-visible manifests. This UI is not a proof boundary.

const ALMS_STAGES = [
  "CAPTURE",
  "HASH",
  "COMMIT",
  "FETCH",
  "REPLAY",
  "PUBLISH",
  "CHAIN_CONFIRM"
];

const STAGE_INDEX = Object.fromEntries(ALMS_STAGES.map((stage, index) => [stage, index]));

const IDENTITY_BINDING = {
  operator: "Jay Wisdom",
  display: "jaywisdom.base",
  canonical: "jaywisdom.eth",
  resolution: "jaywisdom.base -> jaywisdom.eth"
};

function hasReceiptForStage(state, stage) {
  return Boolean(state?.receipts?.[stage]);
}

function monotonicStageValid(state) {
  const current = state?.stage;
  if (!(current in STAGE_INDEX)) return false;
  const currentIndex = STAGE_INDEX[current];
  for (let i = 0; i <= currentIndex; i++) {
    if (!hasReceiptForStage(state, ALMS_STAGES[i])) return false;
  }
  return true;
}

function detectVerificationViolations(state) {
  const charges = [];

  if (!monotonicStageValid(state)) {
    charges.push({
      charge: "GHOST_PROMOTION",
      severity: "RED",
      fix: "Return to the last stage with a valid receipt."
    });
  }

  if ((state?.stage === "CHAIN_CONFIRM" || state?.claimed_status === "CHAIN_CONFIRMED") && !hasReceiptForStage(state, "REPLAY")) {
    charges.push({
      charge: "SKIPPED_REPLAY",
      severity: "RED",
      fix: "Run replay and record REPLAY receipt before chain confirmation."
    });
  }

  const text = state?.text || "";
  if (/[“”‘’]/.test(text) || text.includes("—")) {
    charges.push({
      charge: "NORMALIZATION_TREASON",
      severity: "RED",
      fix: "Replace smart quotes / em dash drift with canonical bytes."
    });
  }

  if (state?.operator_base_name === "jaywisdom.base" && state?.canonical_ens_root !== "jaywisdom.eth") {
    charges.push({
      charge: "IDENTITY_DRIFT",
      severity: "YELLOW",
      fix: "Bind jaywisdom.base to canonical ENS root jaywisdom.eth."
    });
  }

  if (state?.hash && !/^[a-f0-9]{64}$/.test(state.hash)) {
    charges.push({
      charge: "HASH_THEATER",
      severity: "RED",
      fix: "Recompute SHA-256 from the stated bytes."
    });
  }

  if (state?.base_tx_hash && state?.base_tx_hash === state?.zora_contract_address) {
    charges.push({
      charge: "FAKE_CHAIN_CONFIRM",
      severity: "RED",
      fix: "Do not treat tx hash as contract address. Fetch chain evidence."
    });
  }

  return charges;
}

function renderMachineState(state) {
  const currentIndex = STAGE_INDEX[state?.stage] ?? -1;
  return ALMS_STAGES.map((stage, index) => ({
    stage,
    complete: index <= currentIndex && hasReceiptForStage(state, stage),
    receipt: state?.receipts?.[stage] || null
  }));
}

function buildMemeCourtCase(state) {
  const charges = detectVerificationViolations(state);
  return {
    artifact: "MEME_COURT_CASE_RESULT",
    operator: IDENTITY_BINDING.operator,
    identity: IDENTITY_BINDING.resolution,
    machine_state: renderMachineState(state),
    charges,
    verdict: charges.length ? "GOBLIN_DETECTED" : "CLEAN_PASS",
    root_status: charges.length ? "RED_OR_YELLOW" : "GREEN"
  };
}

function zoraCaptionFromCase(caseResult, context = {}) {
  return [
    `Meme Court Case: ${context.case_id || "MC-DRAFT"}`,
    "",
    `Verdict: ${caseResult.verdict}`,
    `Operator: ${IDENTITY_BINDING.operator}`,
    `Identity: ${IDENTITY_BINDING.resolution}`,
    `Root: ${context.root || "PENDING"}`,
    `Receipt: ${context.receipt_path || "PENDING"}`,
    `Verify: ${context.verify_url || "https://jsonwisdom.github.io/AL/"}`,
    "",
    "No Receipt. No Mercy. 🧌⚖️🧾"
  ].join("\n");
}

if (typeof window !== "undefined") {
  window.ALMS_STAGES = ALMS_STAGES;
  window.IDENTITY_BINDING = IDENTITY_BINDING;
  window.detectVerificationViolations = detectVerificationViolations;
  window.renderMachineState = renderMachineState;
  window.buildMemeCourtCase = buildMemeCourtCase;
  window.zoraCaptionFromCase = zoraCaptionFromCase;
}
