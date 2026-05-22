#!/usr/bin/env node

const verdict = {
  verdict: "NEEDS_SOURCE",
  script: "replay-verification.js",
  checked: [
    "replay_procedure",
    "reproducible_environment_capture"
  ],
  missing_sources: [
    "replay_input_specification",
    "deterministic_execution_contract",
    "baseline_commit_anchor"
  ],
  promotion_status: "STUB_LOCKED",
  ghost_anchor_risk: false
};

console.log(JSON.stringify(verdict, null, 2));
