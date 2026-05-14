import { mkdirSync, writeFileSync } from "node:fs";
import { resolve, basename } from "node:path";
import { loadBaseline } from "./load_baseline.js";
import { createHash } from "node:crypto";

function canonicalize(value: unknown): string {
  return JSON.stringify(sortCanonical(value));
}

function sortCanonical(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(sortCanonical);
  }

  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, v]) => [k, sortCanonical(v)])
    );
  }

  return value;
}

function sha256(data: string): string {
  return createHash("sha256").update(data, "utf8").digest("hex");
}

export function writeDriftReceipt(
  baselinePath: string,
  candidatePath: string
): string {
  const baseline = loadBaseline(baselinePath);
  const candidate = loadBaseline(candidatePath);

  const canonicalBaseline = canonicalize(baseline);
  const canonicalCandidate = canonicalize(candidate);

  const baselineHash = sha256(canonicalBaseline);
  const candidateHash = sha256(canonicalCandidate);

  const detectedAt = new Date().toISOString();

  const receiptBody = {
    schemaVersion: "baseline_drift_receipt_v1",
    baselinePath,
    candidatePath,
    baselineHash,
    candidateHash,
    detectedAt,
    canonicalBaseline,
    canonicalCandidate
  };

  const receiptHash = sha256(canonicalize(receiptBody));

  const receipt = {
    ...receiptBody,
    receiptHash
  };

  const driftDir = resolve(process.cwd(), "reports/baselines/drift");

  mkdirSync(driftDir, { recursive: true });

  const filename = `drift_${receiptHash}.json`;
  const outPath = resolve(driftDir, filename);

  writeFileSync(outPath, JSON.stringify(receipt, null, 2), "utf8");

  return outPath;
}
