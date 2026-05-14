import * as ed from "@noble/ed25519";
import { sha512 } from "@noble/hashes/sha2.js";
import { hexToBytes } from "@noble/hashes/utils";

ed.hashes.sha512 = sha512;

export function verifySignature(
  canonicalEventBytes: Uint8Array,
  signature: string,
  observerPublicKey: string
): boolean {
  try {
    const sigBytes = hexToBytes(signature);
    const pubBytes = hexToBytes(observerPublicKey);

    if (sigBytes.length !== 64 || pubBytes.length !== 32) {
      return false;
    }

    return ed.verify(sigBytes, canonicalEventBytes, pubBytes, { zip215: false });
  } catch {
    return false;
  }
}
