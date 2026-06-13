// DISABLED WORKFLOW DISPATCH SCAFFOLD
// AUTHORITY=false NO_FAKE_GREEN=true
// This module documents the intended workflow_dispatch boundary but does not dispatch.

export const DISPATCH_BOUNDARY = Object.freeze({
  status: "DISABLED_PENDING_EXPLICIT_AUTHORIZATION",
  repo: "jsonwisdom/AL",
  workflow: "al-jay-agent-zora-sleep-console.yml",
  ref: "master",
  event: "workflow_dispatch",
  allowed_input: "replay",
  workflow_dispatch: false,
  workflow_write: false,
  chain_write: false,
  wallet_control: false,
  signing: false,
  broadcast: false,
  authority: false,
  no_fake_green: true,
  required_authorization_phrase: "dispatch authorized — workflow only, no chain write, no wallet"
});

export function disabledDispatchResponse() {
  return {
    ok: false,
    error: "workflow dispatch disabled pending explicit operator authorization receipt",
    boundary: DISPATCH_BOUNDARY,
    next_best_action: "Operator must explicitly receipt: dispatch authorized — workflow only, no chain write, no wallet"
  };
}
