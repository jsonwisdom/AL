import { mkdir, readFile, writeFile, appendFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import type { IncidentReceipt } from "./emitIncidentReceipt";

export type AnchorWriteResult =
  | { ok: true; path: string; status: "WRITTEN" | "APPENDED" }
  | { ok: false; path: string; status: "ALREADY_EXISTS" | "WRITE_FAILED"; error: string };

const ROOT = "runtime-data";

export const paths = {
  receipt: (receiptId: string) => join(ROOT, "receipts", `${receiptId}.json`),
  signatures: (receiptId: string) => join(ROOT, "signatures", `${receiptId}.ndjson`),
  raid: (raidId: string) => join(ROOT, "raids", `${raidId}.json`),
};

async function ensureParent(path: string): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
}

export async function writeReceipt(receipt: IncidentReceipt): Promise<AnchorWriteResult> {
  const path = paths.receipt(receipt.receiptId);
  try {
    await ensureParent(path);
    await writeFile(path, JSON.stringify(receipt, null, 2), { flag: "wx" });
    return { ok: true, path, status: "WRITTEN" };
  } catch (err: any) {
    if (err?.code === "EEXIST") return { ok: false, path, status: "ALREADY_EXISTS", error: err.message };
    return { ok: false, path, status: "WRITE_FAILED", error: err?.message ?? String(err) };
  }
}

export async function appendSignature(
  receiptId: string,
  sig: { signedObjectHash: string; signerId: string; signature: string; timestamp: number }
): Promise<AnchorWriteResult> {
  const path = paths.signatures(receiptId);
  try {
    if (sig.signedObjectHash !== receiptId) {
      return { ok: false, path, status: "WRITE_FAILED", error: "signature signedObjectHash does not match receiptId" };
    }
    await ensureParent(path);
    await appendFile(path, `${JSON.stringify(sig)}\n`, { flag: "a" });
    return { ok: true, path, status: "APPENDED" };
  } catch (err: any) {
    return { ok: false, path, status: "WRITE_FAILED", error: err?.message ?? String(err) };
  }
}

export async function readReceiptBundle(
  receiptId: string
): Promise<{ receipt: IncidentReceipt; signatures: unknown[] } | null> {
  try {
    const receipt = JSON.parse(await readFile(paths.receipt(receiptId), "utf8")) as IncidentReceipt;
    let signatures: unknown[] = [];

    try {
      const raw = await readFile(paths.signatures(receiptId), "utf8");
      signatures = raw.split("\n").filter((line) => line.trim()).map((line) => JSON.parse(line));
    } catch (err: any) {
      if (err?.code !== "ENOENT") throw err;
    }

    return { receipt, signatures };
  } catch {
    return null;
  }
}
