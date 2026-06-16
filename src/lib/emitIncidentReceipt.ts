import { sha256StableJson } from "./hash";
import type { CanonicalizedResult } from "./canonicalizeIncident";

export interface IncidentReceipt {
  receiptId: string;
  version: "E06.V1";
  epoch: "E06";
  canonicalIncidentHash: string;
  canonicalIncident: Record<string, unknown>;
  emittedAt: number;
  lineage: { previousReceiptId?: string; sequenceNumber: number };
  surface: string;
  replay: { replayedFromBlock?: number; originalEmittedAt?: number };
  metadata: Record<string, unknown>;
  attachedEvidence: Array<{ type: string; hash: string; url?: string }>;
}

export async function emitIncidentReceipt(
  canonicalized: CanonicalizedResult,
  emittedAt: number,
  options: {
    surface?: string;
    previousReceiptId?: string;
    sequenceNumber?: number;
    metadata?: Record<string, unknown>;
    attachedEvidence?: Array<{ type: string; hash: string; url?: string }>;
  } = {}
): Promise<IncidentReceipt> {
  const receiptId = sha256StableJson(canonicalized.canonicalIncident);

  return {
    receiptId,
    version: "E06.V1",
    epoch: "E06",
    canonicalIncidentHash: canonicalized.canonicalIncidentHash,
    canonicalIncident: canonicalized.canonicalIncident,
    emittedAt,
    lineage: {
      previousReceiptId: options.previousReceiptId,
      sequenceNumber: options.sequenceNumber ?? 1,
    },
    surface: options.surface ?? "unknown",
    replay: {
      replayedFromBlock: options.metadata?.replayedFromBlock as number | undefined,
      originalEmittedAt: options.metadata?.originalEmittedAt as number | undefined,
    },
    metadata: options.metadata ?? {},
    attachedEvidence: options.attachedEvidence ?? [],
  };
}
