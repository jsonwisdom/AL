import type { ReceiptSignature } from "../types/ReceiptSignature";

export type SignatureVerificationStatus =
  | "VALID"
  | "INVALID"
  | "UNSUPPORTED_ALGORITHM";

export function verifySignature(
  receiptId: string,
  sig: ReceiptSignature
): SignatureVerificationStatus {
  if (sig.signedObjectHash !== receiptId) return "INVALID";

  if (sig.algorithm === "dummy") {
    return sig.signature.length > 0 ? "VALID" : "INVALID";
  }

  return "UNSUPPORTED_ALGORITHM";
}
