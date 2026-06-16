import { describe, it, expect, beforeEach } from "vitest";
import { canonicalizeIncident } from "./canonicalizeIncident";
import { emitIncidentReceipt } from "./emitIncidentReceipt";
import { appendSignature, readReceiptBundle, writeReceipt } from "./filesystemAnchor";
import { existsSync, rmSync } from "node:fs";

function resetRuntimeFS() {
  if (existsSync("runtime-data")) rmSync("runtime-data", { recursive: true, force: true });
}

describe("E06 End-to-End Replay — V1", () => {
  beforeEach(() => resetRuntimeFS());

  it("receiptId equals canonicalIncidentHash", async () => {
    const t = 1700000000000;
    const canonical = await canonicalizeIncident({ type: "ZORA_MINT_ANOMALY", chain: "base" }, t);
    const receipt = await emitIncidentReceipt(canonical, t + 100, { surface: "zora-explorer" });

    expect(receipt.receiptId).toBe(canonical.canonicalIncidentHash);
    expect(receipt.canonicalIncidentHash).toBe(canonical.canonicalIncidentHash);
  });

  it("handles nested objects deterministically", async () => {
    const raw = { level1: { level2: { z: 1, a: 2 }, b: "test" }, array: [3, { x: 1 }, 2] };
    const c1 = await canonicalizeIncident(raw, 4000);
    const c2 = await canonicalizeIncident(raw, 4000);
    const r1 = await emitIncidentReceipt(c1, 4100);
    const r2 = await emitIncidentReceipt(c2, 4100);

    expect(c1.canonicalIncidentHash).toBe(c2.canonicalIncidentHash);
    expect(r1).toEqual(r2);
  });

  it("write once receipt", async () => {
    const canonical = await canonicalizeIncident({ test: true }, 1000);
    const receipt = await emitIncidentReceipt(canonical, 1100);

    const first = await writeReceipt(receipt);
    const second = await writeReceipt(receipt);

    expect(first.ok).toBe(true);
    expect(first.status).toBe("WRITTEN");
    expect(second.ok).toBe(false);
    expect(second.status).toBe("ALREADY_EXISTS");
  });

  it("signature append external and read bundle roundtrip", async () => {
    const canonical = await canonicalizeIncident({ hello: "world" }, 2000);
    const receipt = await emitIncidentReceipt(canonical, 2100);

    await writeReceipt(receipt);
    const sig = { signedObjectHash: receipt.receiptId, signerId: "jay", signature: "0xmock", timestamp: 2200 };
    const appended = await appendSignature(receipt.receiptId, sig);
    const bundle = await readReceiptBundle(receipt.receiptId);

    expect(appended.ok).toBe(true);
    expect(bundle).not.toBeNull();
    expect(bundle!.receipt).toEqual(receipt);
    expect(bundle!.signatures).toEqual([sig]);
  });

  it("deterministic replay — same inputs, same outputs", async () => {
    const raw = { value: 42, nested: { b: 2, a: 1 } };
    const c1 = await canonicalizeIncident(raw, 3000);
    const c2 = await canonicalizeIncident(raw, 3000);
    const r1 = await emitIncidentReceipt(c1, 3100);
    const r2 = await emitIncidentReceipt(c2, 3100);

    expect(c1).toEqual(c2);
    expect(r1).toEqual(r2);
  });
});
