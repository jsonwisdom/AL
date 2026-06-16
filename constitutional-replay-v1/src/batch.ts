import { sha256Hex } from "./hash.js";
import { ReceiptV1, receiptHash } from "./receipt.js";

export class BatchError extends Error {
  readonly code: BatchFailureCode;

  constructor(code: BatchFailureCode, message?: string) {
    super(message ?? code);
    this.name = "BatchError";
    this.code = code;
  }
}

export type BatchFailureCode =
  | "EMPTY_BATCH"
  | "RECEIPT_HASH_MISSING"
  | "BATCH_ROOT_MISMATCH";

export interface ReceiptSummaryV1 {
  receipt_hash: string;
  policy_hash: string;
  interpreter_hash: string;
  result: "SUCCESS" | "REFUSAL";
  risk_tier: "LOW" | "MEDIUM" | "HIGH";
  reason_code: string | null;
  batch_id: string;
}

export interface ReceiptBatchV1 {
  batch_version: "batch.v1";
  batch_id: string;
  hash_algorithm: "sha256";
  leaves: string[];
  merkle_root: string;
}

function normalizeLeaf(hash: string): string {
  if (!hash.startsWith("sha256:") || hash.length !== "sha256:".length + 64) {
    throw new BatchError("RECEIPT_HASH_MISSING", hash);
  }

  return hash;
}

function hashPair(left: string, right: string): string {
  const leftHex = normalizeLeaf(left).slice("sha256:".length);
  const rightHex = normalizeLeaf(right).slice("sha256:".length);
  const combined = Buffer.from(`${leftHex}${rightHex}`, "utf8");

  return `sha256:${sha256Hex(combined)}`;
}

export function merkleRoot(leaves: string[]): string {
  if (leaves.length === 0) {
    throw new BatchError("EMPTY_BATCH");
  }

  let level = leaves.map(normalizeLeaf);

  while (level.length > 1) {
    const next: string[] = [];

    for (let index = 0; index < level.length; index += 2) {
      const left = level[index];

      if (left === undefined) {
        throw new BatchError("RECEIPT_HASH_MISSING", `index=${index}`);
      }

      const right = level[index + 1] ?? left;
      next.push(hashPair(left, right));
    }

    level = next;
  }

  const root = level[0];

  if (root === undefined) {
    throw new BatchError("EMPTY_BATCH");
  }

  return root;
}

export function summarizeReceipt(receipt: ReceiptV1, batch_id: string): ReceiptSummaryV1 {
  return {
    receipt_hash: receiptHash(receipt),
    policy_hash: receipt.policy_hash,
    interpreter_hash: receipt.interpreter_hash,
    result: receipt.result,
    risk_tier: receipt.result === "REFUSAL" ? "HIGH" : "LOW",
    reason_code: receipt.refusal_code,
    batch_id
  };
}

export function emitBatch(batch_id: string, receipts: ReceiptV1[]): ReceiptBatchV1 {
  const leaves = receipts.map((receipt) => receiptHash(receipt));

  return {
    batch_version: "batch.v1",
    batch_id,
    hash_algorithm: "sha256",
    leaves,
    merkle_root: merkleRoot(leaves)
  };
}

export function verifyBatch(batch: ReceiptBatchV1): void {
  const computed = merkleRoot(batch.leaves);

  if (computed !== batch.merkle_root) {
    throw new BatchError("BATCH_ROOT_MISMATCH", `expected=${batch.merkle_root} actual=${computed}`);
  }
}
