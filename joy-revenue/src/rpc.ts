import { createPublicClient, webSocket } from "viem";

import { ALLOWED_METHODS, RPC_URL, ZERO_KEY_RULING } from "./config.js";

export const client = createPublicClient({
  transport: webSocket(RPC_URL)
});

export function assertAllowed(method: string) {
  if (!ALLOWED_METHODS.has(method)) {
    throw new Error(`Method not allowed by zero-key read-only policy: ${method}`);
  }
}

export function getRuntimeRuling() {
  return {
    mode: "read_only_public_client",
    ...ZERO_KEY_RULING
  };
}
