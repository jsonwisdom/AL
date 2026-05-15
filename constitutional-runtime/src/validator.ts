import { Lineage, Receipt, Verdict } from "./types.js";
import { replayReceipt, pathExists } from "./replay.js";
import { divergenceClass, mutationSurface } from "./divergence.js";
import Ajv from "ajv/dist/ajv.js";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { verifySignature } from "./signature.js";
import { canonicalizeForSignature } from "./canonical.js";
import { evaluateObserverThreshold } from "./threshold.js";
import { resolveObserverAtLineage } from "./observer.js";
import {
  ContradictionReceipt,
  detectContradiction,
  isValidContradictionReceipt
} from "./contradiction.js";
import {
  isMeaningfulObserverTransition,
  isObserverRevocation,
  isValidObserverTransition,
  ObserverTransition
} from "./observer-transition.js";

const SCHEMA_DIR = join(process.cwd(), "schema");
const PLACEHOLDER_PUBLIC_KEY = "0000000000000000000000000000000000000000000000000000000000000000";

let lineageValidator: any = null;
let receiptValidator: any = null;
let contradictionValidator: any = null;
let observerTransitionValidator: any = null;

function initValidators() {
  if (lineageValidator) return;

  const ajv = new Ajv({ allErrors: true, strict: true, verbose: true });

  const eventSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "event.schema.json"), "utf8"));
  const lineageSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "lineage.schema.json"), "utf8"));
  const receiptSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "receipt.schema.json"), "utf8"));
  const observerReportSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "observer-report.schema.json"), "utf8"));
  const contradictionSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "contradiction.schema.json"), "utf8"));
  const observerTransitionSchema = JSON.parse(readFileSync(join(SCHEMA_DIR, "observer-transition.schema.json"), "utf8"));

  ajv.addSchema(eventSchema, "event.schema.json");
  ajv.addSchema(lineageSchema, "lineage.schema.json");
  ajv.addSchema(receiptSchema, "receipt.schema.json");
  ajv.addSchema(observerReportSchema, "observer-report.schema.json");
  ajv.addSchema(contradictionSchema, "contradiction.schema.json");
  ajv.addSchema(observerTransitionSchema, "observer-transition.schema.json");

  lineageValidator = ajv.compile(lineageSchema);
  receiptValidator = ajv.compile(receiptSchema);
  contradictionValidator = ajv.compile(contradictionSchema);
  observerTransitionValidator = ajv.compile(observerTransitionSchema);
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

export function validateObserverTransitionSchema(data: unknown): { valid: boolean; errors?: any[] } {
  initValidators();
  const valid = observerTransitionValidator(data);
  return { valid, errors: valid ? undefined : observerTransitionValidator.errors };
}

export function validateReceipt(
  receipt: Receipt | ContradictionReceipt | ObserverTransition,
  lineage: Lineage
): {
  verdict: Verdict | "OBSERVER_TRANSITION";
  computed_root?: string;
  divergence?: string;
  mutation_surface?: "Mutable" | "Frozen";
  details?: {
    uniqueActiveObservers?: number;
    activeObserverCount?: number;
    totalReportsSubmitted?: number;
    conflictingRoots?: string[];
    lineage_tip?: string;
    observer_id?: string;
    from_status?: "ACTIVE" | "REVOKED";
    to_status?: "ACTIVE" | "REVOKED";
    replay_path?: string[];
    replayPathLength?: number;
    hasValidLineageBinding?: boolean;
    resolvedObserver?: {
      observer_id: string;
      status: "ACTIVE" | "REVOKED";
      lineage_tip: string;
      public_key_source: "placeholder";
    } | null;
    context?: {
      replayPath: string[];
      replayPathLength: number;
      lineageTip: string;
      hasValidLineageBinding: boolean;
      resolvedObserverAvailable: boolean;
      lineageConsistency: {
        observerLineageTip: string | null;
        transitionLineageTip: string;
        isConsistent: boolean | null;
        reason: string;
      };
    };
    isMeaningful?: boolean;
    isRevocation?: boolean;
    lineageConsistency?: {
      observerLineageTip: string | null;
      transitionLineageTip: string;
      isConsistent: boolean | null;
      reason: string;
    };
    reason?: string | null;
  };
} {
  if ("verdict" in receipt && receipt.verdict === "OBSERVER_TRANSITION") {
    const schemaResult = validateObserverTransitionSchema(receipt);
    if (!schemaResult.valid || !isValidObserverTransition(receipt)) {
      return {
        verdict: "INSUFFICIENT_EVIDENCE",
        mutation_surface: "Frozen",
        details: {
          reason: "schema_or_structural_validation_failed"
        }
      };
    }

    const replayPath = receipt.replay_path ?? [];
    const hasValidLineageBinding = typeof receipt.lineage_tip === "string" && receipt.lineage_tip.length === 64;
    const resolvedObserver = resolveObserverAtLineage(
      receipt.observer_id,
      PLACEHOLDER_PUBLIC_KEY,
      receipt.lineage_tip,
      []
    );
    const resolvedObserverDetails = resolvedObserver
      ? {
          observer_id: resolvedObserver.observer_id,
          status: resolvedObserver.status,
          lineage_tip: resolvedObserver.lineage_tip,
          public_key_source: "placeholder" as const
        }
      : null;
    const lineageConsistency = {
      observerLineageTip: resolvedObserver?.lineage_tip ?? null,
      transitionLineageTip: receipt.lineage_tip,
      isConsistent: resolvedObserver ? resolvedObserver.lineage_tip === receipt.lineage_tip : null,
      reason: resolvedObserver ? "observer_resolved_with_placeholder_key" : "observer_context_not_available"
    };

    return {
      verdict: hasValidLineageBinding ? "OBSERVER_TRANSITION" : "INSUFFICIENT_EVIDENCE",
      mutation_surface: "Frozen",
      details: {
        observer_id: receipt.observer_id,
        from_status: receipt.from_status,
        to_status: receipt.to_status,
        replay_path: replayPath,
        replayPathLength: replayPath.length,
        hasValidLineageBinding,
        resolvedObserver: resolvedObserverDetails,
        lineage_tip: receipt.lineage_tip,
        context: {
          replayPath,
          replayPathLength: replayPath.length,
          lineageTip: receipt.lineage_tip,
          hasValidLineageBinding,
          resolvedObserverAvailable: Boolean(resolvedObserver),
          lineageConsistency
        },
        isMeaningful: isMeaningfulObserverTransition(receipt),
        isRevocation: isObserverRevocation(receipt),
        lineageConsistency,
        reason: receipt.reason ?? null
      }
    };
  }

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
