import { createHash } from "node:crypto";
import { loadBaseline, BaselineReceipt } from "./load_baseline.js";

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

export interface DriftResult {
  drift: boolean;
  baselineHash: string;
  candidateHash: string;
  diff?: {
    baseline: string;
    candidate: string;
  };
}

export function compareBaseline(
  baselinePath: string,
  candidatePath: string
): DriftResult {
  const baseline: BaselineReceipt = loadBaseline(baselinePath);
  const candidate: BaselineReceipt = loadBaseline(candidatePath);

  const baselineCanon = canonicalize(baseline);
  const candidateCanon = canonicalize(candidate);

  const baselineHash = sha256(baselineCanon);
  const candidateHash = sha256(candidateCanon);

  const drift = baselineHash !== candidateHash;

  if (drift) {
    return {
      drift: true,
      baselineHash,
      candidateHash,
      diff: {
        baseline: baselineCanon,
        candidate: candidateCanon
      }
    };
  }

  return {
    drift: false,
    baselineHash,
    candidateHash
  };
}
