import { bytesHex } from "./jcs.ts";

/**
 * Runtime-agnostic cryptographic digest.
 * Uses Web Crypto API through globalThis.crypto.subtle.
 *
 * No runtime-specific imports.
 */
export async function sha256Hex(data: Uint8Array): Promise<string> {
  const subtle = globalThis.crypto.subtle;

  if (!subtle) {
    throw new Error(
      "Web Crypto API not available. Expected globalThis.crypto.subtle.digest to exist."
    );
  }

  const digest = await subtle.digest("SHA-256", data);
  return bytesHex(new Uint8Array(digest));
}

export { bytesHex as toHex } from "./jcs.ts";
