export type ReceiptSignature = {
  signerId: string;
  signature: string;
  algorithm: "dummy" | "ed25519";
  signedObjectHash: string;
  timestamp: number;
};
