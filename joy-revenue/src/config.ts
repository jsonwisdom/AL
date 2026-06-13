import type { Address } from "viem";

export const JOY_CONTRACT_ADDRESS = (
  process.env.JOY_CONTRACT_ADDRESS ?? "0x0000000000000000000000000000000000000000"
) as Address;

export const RPC_URL = process.env.RPC_URL ?? "wss://your-node.example/ws";

export const ALLOWED_METHODS = new Set([
  "eth_getLogs",
  "eth_call",
  "eth_getBlockByNumber"
]);

export const START_BLOCK = BigInt(process.env.START_BLOCK ?? "0");

export const ZERO_KEY_RULING = Object.freeze({
  chain_write: false,
  wallet_control: false,
  signing: false,
  broadcast: false,
  authority: false,
  no_fake_green: true
});
