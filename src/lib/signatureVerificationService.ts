import { readReceiptBundle } from "./filesystemAnchor";
import type { ReceiptSignature } from "../types/ReceiptSignature";
import { verifySignature } from "./verifySignature";

export type SignatureLayerStatus =
  | "VALID"
  | "NO_RECEIPT"
  | "NO_SIGNATURES"
  | "INVALID_SIGNATURE"
  | "UNSUPPORTED_ALGORITHM";

export async function verifySignedIncidentReceipt(receiptId: string) {
  const bundle = await readReceiptBundle(receiptId);

  if (!bundle) {
    return { status: "NO_RECEIPT", receiptId, validSignatures: [], invalidSignatures: [], unsupportedSignatures: [], errors: ["Receipt not found"] };
  }

  const signatures = (bundle.signatures ?? []) as ReceiptSignature[];

  if (signatures.length === 0) {
    return { status: "NO_SIGNATURES", receiptId, validSignatures: [], invalidSignatures: [], unsupportedSignatures: [], errors: [] };
  }

  const validSignatures: ReceiptSignature[] = [];
  const invalidSignatures: ReceiptSignature[] = [];
  const unsupportedSignatures: ReceiptSignature[] = [];
  const errors: string[] = [];

  for (const sig of signatures) {
    const res = verifySignature(receiptId, sig);
    if (res === "VALID") validSignatures.push(sig);
    else if (res === "INVALID") {
      invalidSignatures.push(sig);
      errors.push(`Invalid signature from ${sig.signerId}`);
    } else {
      unsupportedSignatures.push(sig);
    }
  }

  const status: SignatureLayerStatus =
    invalidSignatures.length > 0 ? "INVALID_SIGNATURE" :
    validSignatures.length > 0 ? "VALID" :
    unsupportedSignatures.length > 0 ? "UNSUPPORTED_ALGORITHM" :
    "NO_SIGNATURES";

  return { status, receiptId, validSignatures, invalidSignatures, unsupportedSignatures, errors };
}
