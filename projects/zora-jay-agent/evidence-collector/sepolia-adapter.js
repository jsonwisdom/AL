// SEPOLIA READ-ONLY ADAPTER
// AUTHORITY=false NO_FAKE_GREEN=true
// This file is intentionally separate from index.html so it can be reviewed before inclusion.

const SEPOLIA_DEFAULT_WALLET = "0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5";

async function fetchSepoliaEvidence(wallet = SEPOLIA_DEFAULT_WALLET, limit = 8) {
  const response = await fetch(`/api/sepolia-evidence?wallet=${encodeURIComponent(wallet)}&limit=${encodeURIComponent(limit)}`);
  const json = await response.json();
  if (!response.ok) {
    throw new Error(json.error || `Sepolia evidence fetch failed: HTTP ${response.status}`);
  }
  return json;
}

function summarizeSepoliaEvidence(json) {
  return {
    mode: json.mode,
    chain_id: json.chain_id,
    wallet: json.wallet,
    balance_eth: json.balance_eth,
    latest_block: json.latest_block,
    transactions_observed: json.transactions_observed,
    chain_write: false,
    wallet_control: false,
    signing: false,
    broadcast: false,
    authority: false,
    no_fake_green: true,
    next_best_action: json.next_best_action
  };
}

window.AL_SEPOLIA_READ_ONLY_ADAPTER = {
  fetchSepoliaEvidence,
  summarizeSepoliaEvidence
};
