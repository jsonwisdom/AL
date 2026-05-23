import { describe, it, expect, beforeEach } from "vitest";
import { canonicalizeIncident } from "./canonicalizeIncident";
import { emitIncidentReceipt } from "./emitIncidentReceipt";
import { appendSignature, writeReceipt } from "./filesystemAnchor";
import { verifySignedIncidentReceipt } from "./signatureVerificationService";
import type { ReceiptSignature } from "../types/ReceiptSignature";
import { existsSync, rmSync } from "node:fs";

function resetFS() {
  if (existsSync("runtime-data")) rmSync("runtime-data", { recursive: true, force: true });
}

describe("SIGNATURE_VERIFICATION_V1 — spine-native", () => {
  beforeEach(() => resetFS());

  it("NO_SIGNATURES for real written receipt", async () => {
    const now = 1700000000000;
    const canonical = await canonicalizeIncident({ type: "test", payload: { x: 1 } }, now);
    const receipt = await emitIncidentReceipt(canonical, now);
    await writeReceipt(receipt);

    const res = await verifySignedIncidentReceipt(receipt.receiptId);
    expect(res.status).toBe("NO_SIGNATURES");
    expect(res.validSignatures).toHaveLength(0);
  });

  it("VALID for dummy signature appended through appendSignature", async () => {
    const now = 1700000000001;
    const canonical = await canonicalizeIncident({ type: "test", payload: { x: 2 } }, now);
    const receipt = await emitIncidentReceipt(canonical, now);
    await writeReceipt(receipt);

    const sig: ReceiptSignature = {
      signerId: "tester",
      signature: "dummy-signature",
      algorithm: "dummy",
      signedObjectHash: receipt.receiptId,
      timestamp: now,
    };

    const result = await appendSignature(receipt.receiptId, sig);
    expect(result.ok).toBe(true);

    const res = await verifySignedIncidentReceipt(receipt.receiptId);
    expect(res.status).toBe("VALID");
    expect(res.validSignatures).toHaveLength(1);
  });

  it("appendSignature rejects wrong signedObjectHash", async () => {
    const now = 1700000000002;
    const canonical = await canonicalizeIncident({ type: "test", payload: { x: 3 } }, now);
    const receipt = await emitIncidentReceipt(canonical, now);
    await writeReceipt(receipt);

    const badSig: ReceiptSignature = {
      signerId: "attacker",
      signature: "dummy-signature",
      algorithm: "dummy",
      signedObjectHash: "wrong-id",
      timestamp: now,
    };

    const result = await appendSignature(receipt.receiptId, badSig);
    expect(result.ok).toBe(false);
    expect(result.status).toBe("WRITE_FAILED");

    const res = await verifySignedIncidentReceipt(receipt.receiptId);
    expect(res.status).toBe("NO_SIGNATURES");
  });

  it("NO_RECEIPT for missing receipt", async () => {
    const res = await verifySignedIncidentReceipt("nonexistent");
    expect(res.status).toBe("NO_RECEIPT");
  });
});
