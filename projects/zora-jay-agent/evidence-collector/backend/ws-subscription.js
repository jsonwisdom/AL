// READ-ONLY SEPOLIA WEBSOCKET SUBSCRIPTION SUBSYSTEM
// AUTHORITY=false NO_FAKE_GREEN=true
// Requires: npm install ws
// Run: SEPOLIA_WS_URL=<wss endpoint> node ws-subscription.js

import WebSocket from "ws";

const SEPOLIA_WS_URL = process.env.SEPOLIA_WS_URL || "";
const WATCH_WALLET = (process.env.SEPOLIA_WATCH_WALLET || "0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5").toLowerCase();
const MAX_EVENTS = Number(process.env.MAX_EVENTS || 50);
const events = [];

if (!SEPOLIA_WS_URL.startsWith("wss://")) {
  console.error(JSON.stringify({
    ok: false,
    error: "SEPOLIA_WS_URL must be a wss:// endpoint",
    authority: false,
    no_fake_green: true,
    chain_write: false,
    wallet_control: false,
    signing: false,
    broadcast: false
  }, null, 2));
  process.exit(1);
}

function remember(event) {
  events.unshift({ observed_at: new Date().toISOString(), ...event });
  events.splice(MAX_EVENTS);
}

function send(ws, method, params = []) {
  const id = Date.now();
  ws.send(JSON.stringify({ jsonrpc: "2.0", id, method, params }));
  return id;
}

function boot() {
  const ws = new WebSocket(SEPOLIA_WS_URL);

  ws.on("open", () => {
    remember({ type: "socket_open", endpoint_label: "SEPOLIA_WS_URL" });
    send(ws, "eth_subscribe", ["newHeads"]);
    // Optional next layer: subscribe logs only when contract address/topic filter is known.
    // send(ws, "eth_subscribe", ["logs", { address: "0x..." }]);
    console.log(JSON.stringify({
      status: "SUBSCRIBED_READ_ONLY",
      subscription: "newHeads",
      watch_wallet: WATCH_WALLET,
      authority: false,
      no_fake_green: true,
      chain_write: false,
      wallet_control: false,
      signing: false,
      broadcast: false
    }, null, 2));
  });

  ws.on("message", (raw) => {
    let msg;
    try { msg = JSON.parse(raw.toString()); } catch { return; }

    if (msg.method === "eth_subscription" && msg.params?.result) {
      const result = msg.params.result;
      remember({
        type: "new_head",
        subscription: msg.params.subscription,
        block_hash: result.hash,
        block_number_hex: result.number,
        parent_hash: result.parentHash,
        timestamp_hex: result.timestamp
      });
      console.log(JSON.stringify(events[0]));
      return;
    }

    if (msg.result && typeof msg.result === "string") {
      remember({ type: "subscription_ack", subscription_id: msg.result });
      console.log(JSON.stringify(events[0]));
      return;
    }

    if (msg.error) {
      remember({ type: "subscription_error", error: msg.error });
      console.error(JSON.stringify(events[0]));
    }
  });

  ws.on("close", (code, reason) => {
    remember({ type: "socket_close", code, reason: reason.toString() });
    console.error(JSON.stringify(events[0]));
  });

  ws.on("error", (error) => {
    remember({ type: "socket_error", error: error.message });
    console.error(JSON.stringify(events[0]));
  });
}

boot();
