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

export const CONTRACT_VERIFICATION_STATUS = process.env.CONTRACT_VERIFICATION_STATUS ?? "unverified";

export const ZORA_PRODUCT_TYPE = process.env.ZORA_PRODUCT_TYPE ?? "unknown";

export const ACCEPTED_PRODUCT_TYPES = new Set([
  "zora_creator_coin",
  "zora_content_coin",
  "zora_1155_collection",
  "verified_erc20",
  "verified_erc1155"
]);

export const ZERO_KEY_RULING = Object.freeze({
  chain_write: false,
  wallet_control: false,
  signing: false,
  broadcast: false,
  authority: false,
  no_fake_green: true
});

export function assertVerifiedTarget() {
  const zero = "0x0000000000000000000000000000000000000000";

  if (JOY_CONTRACT_ADDRESS === zero) {
    throw new Error("JOY_CONTRACT_ADDRESS is not set. Refusing fake revenue indexing.");
  }

  if (CONTRACT_VERIFICATION_STATUS !== "verified") {
    throw new Error("CONTRACT_VERIFICATION_STATUS must be verified before indexing.");
  }

  if (!ACCEPTED_PRODUCT_TYPES.has(ZORA_PRODUCT_TYPE)) {
    throw new Error(`ZORA_PRODUCT_TYPE is not accepted: ${ZORA_PRODUCT_TYPE}`);
  }
}

export function targetReceipt() {
  return {
    contract: JOY_CONTRACT_ADDRESS,
    contract_verification_status: CONTRACT_VERIFICATION_STATUS,
    zora_product_type: ZORA_PRODUCT_TYPE,
    accepted_product_types: [...ACCEPTED_PRODUCT_TYPES],
    ...ZERO_KEY_RULING
  };
}
