import { Lineage, Receipt, Verdict } from "./types.js";
import { replayReceipt, pathExists } from "./replay.js";
import { divergenceClass, mutationSurface } from "./divergence.js";
import Ajv from "ajv/dist/ajv.js";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { verifySignature } from "./signature.js";
import { canonicalizeForSignature } from "./canonical.js";
import { evaluateObserverThreshold } from "./threshold.js";
import {
  ContradictionReceipt,
  detectContradiction,
  isValidContradictionReceipt
} from "./contradiction.js";

const SCHEMA_DIR = join(process.cwd(), "schema");

let lineageValidator: any = null;
let receiptValidator: any = null;
let contradictionValidator: any = null;

function initValidators() {
  if (lineageValidator) return;

  const ajv = new Ajv({ allErrors: true, strict: true, verbose: true });

  const eventSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "event.schema.json"), "utf8"));
  const lineageSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "lineage.schema.json"), "utf8"));
  const receiptSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "receipt.schema.json"), "utf8"));
  const observerReportSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "observer-report.schema.json"), "utf8"));
  const contradictionSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "contradiction.schema.json"), "utf8"));

  ajv.addSchema(eventSchema, "event.schema.json");
  ajv.addSchema(lineageSchema, "lineage.schema.json");
  ajv.addSchema(receiptSchema, "receipt.schema.json");
  ajv.addSchema(observerReportSchema, "observer-report.schema.json");
  ajv.addSchema(contradictionSchema, "contradiction.schema.json");

  lineageValidator = ajv.compile(lineageSchema);
  receiptValidator = ajv.compile(receiptSchema);
  contradictionValidator = ajv.compile(contradictionSchema);
}

export function validateLineageSchema(data: unknown): { valid: boolean; errors?: any[] } {
  initValidators();
  const valid = lineageValidator(data);
  return { valid, errors: valid ? undefined : lineageValidator.errors };
}

export function validateReceiptSchema(data: unknown): { valid: boolean; errors?: any[] } {
  initValidators();
  const valid = receiptValidator(data);
  return { valid, errors: valid ? undefined : receiptValidator.errors };
}

export function validateContradictionSchema(data: unknown): { valid: boolean; errors?: any[] } {
  initValidators();
  const valid = contradictionValidator(data);
  return { valid, errors: valid ? undefined : contradictionValidator.errors };
}

export function validateReceipt(
  receipt: Receipt | ContradictionReceipt,
  lineage: Lineage
): {
  verdict: Verdict;
  computed_root?: string;
  divergence?: string;
  mutation_surface?: "Mutable" | "Frozen";
  details?: {
    uniqueActiveObservers?: number;
    activeObserverCount?: number;
    totalReportsSubmitted?: number;
    conflictingRoots?: string[];
    lineage_tip?: string;
    reason?: string;
  };
} {
  if ("reports" in receipt) {
    const schemaResult = validateContradictionSchema(receipt);
    if (!schemaResult.valid || !isValidContradictionReceipt(receipt)) {
      return {
        verdict: "INSUFFICIENT_EVIDENCE",
        mutation_surface: "Frozen"
      };
    }

    const result = detectContradiction(receipt);

    if (!result.isLineageBound) {
      return {
        verdict: "INSUFFICIENT_EVIDENCE",
        mutation_surface: "Frozen",
        details: {
          reason: "missing_lineage_binding"
        }
      };
    }

    if (result.isContradiction) {
      return {
        verdict: "CONSTITUTIONAL_CONTRADICTION",
        divergence: "D3",
        mutation_surface: "Frozen",
        details: {
          uniqueActiveObservers: result.uniqueActiveObservers,
          activeObserverCount: result.activeObserverCount,
          totalReportsSubmitted: receipt.reports.length,
          conflictingRoots: result.conflictingRoots,
          lineage_tip: receipt.lineage_tip
        }
      };
    }

    return {
      verdict: "INSUFFICIENT_EVIDENCE",
      mutation_surface: "Frozen",
      details: {
        activeObserverCount: result.activeObserverCount,
        totalReportsSubmitted: receipt.reports.length,
        reason: "insufficient_active_observers"
      }
    };
  }

  const replayReceiptInput = receipt as Receipt;

  if (!pathExists(replayReceiptInput, lineage)) {
    return {
      verdict: "INSUFFICIENT_EVIDENCE",
      mutation_surface: "Frozen"
    };
  }

  for (const eventId of replayReceiptInput.replay_path) {
    const event = lineage.events[eventId];

    if (event.signatures.length === 0) {
      return {
        verdict: "CONSTITUTIONAL_UNKNOWN",
        mutation_surface: "Frozen"
      };
    }

    const canonicalStr = canonicalizeForSignature(event as unknown as Record<string, unknown>);
    const canonicalBytes = new TextEncoder().encode(canonicalStr);

    for (const sig of event.signatures) {
      if (!verifySignature(canonicalBytes, sig.signature, sig.observer_id)) {
        return {
          verdict: "CONSTITUTIONAL_UNKNOWN",
          mutation_surface: "Frozen"
        };
      }
    }

    const signedObservers = [...new Set(event.signatures.map((s) => s.observer_id))];
    if (!evaluateObserverThreshold(event.signatures, signedObservers, 1)) {
      return {
        verdict: "CONSTITUTIONAL_UNKNOWN",
        mutation_surface: "Frozen"
      };
    }
  }

  const computed = replayReceipt(replayReceiptInput, lineage);
  const d = divergenceClass(computed, replayReceiptInput.state_snapshot);
  const surface = mutationSurface(d);

  if (d === "D0") {
    return {
      verdict: "MATCH",
      computed_root: computed,
      divergence: d,
      mutation_surface: surface
    };
  }

  return {
    verdict: "DIVERGENCE",
    computed_root: computed,
    divergence: d,
    mutation_surface: surface
  };
}
