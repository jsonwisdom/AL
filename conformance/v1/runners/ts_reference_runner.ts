import {
  GENESIS_MANIFEST,
  MinimalVerifiableKernel,
  type RawEvent,
  sha256Sync,
  toCanonicalBytes
} from "../../../src/kernel.ts";

import vector001 from "../vectors/001_positive_parity_genesis.json" with { type: "json" };
import vector002 from "../vectors/002_structural_rejection_float.json" with { type: "json" };

interface Verdict {
  vector_id: string;
  runtime: string;
  implementation: string;
  verdict: "PASS" | "FAIL" | "DEGRADED";
  mismatches: string[];
  computed?: unknown;
}

function runtimeName(): string {
  if (typeof Bun !== "undefined") return "bun";
  if (typeof Deno !== "undefined") return "deno";
  if (typeof window !== "undefined") return "browser";
  return "node";
}

function rejectionClass(error: unknown): string {
  const msg = String(error instanceof Error ? error.message : error);
  if (msg.includes("Number forbidden") || msg.includes("Float")) return "FAIL_NUMBER_FORBIDDEN";
  if (msg.includes("Manifest hash mismatch")) return "FAIL_MANIFEST_HASH_MISMATCH";
  if (msg.includes("Index must be gap-free")) return "FAIL_INDEX_GAP";
  return "FAIL_UNKNOWN";
}

function buildEventTelemetry(events: RawEvent[]) {
  const event_ids: string[] = [];
  const canonical_payload_sha256: string[] = [];

  for (const event of events) {
    const bytes = toCanonicalBytes(event.payload, GENESIS_MANIFEST);
    const id = sha256Sync(bytes);
    event_ids.push(id);
    canonical_payload_sha256.push(id);
  }

  return { event_ids, canonical_payload_sha256 };
}

function runPositiveParity(vector: any): Verdict {
  const kernel = new MinimalVerifiableKernel(GENESIS_MANIFEST);
  const events = vector.events as RawEvent[];
  const trace = buildEventTelemetry(events);

  for (const event of events) {
    kernel.appendEvent(event);
  }

  const replay = kernel.replay();

  return {
    vector_id: vector.vector_id,
    runtime: runtimeName(),
    implementation: "minimal-verifiable-kernel-ts-v1",
    verdict: replay.degraded ? "DEGRADED" : "PASS",
    mismatches: [],
    computed: {
      event_ids: trace.event_ids,
      canonical_payload_sha256: trace.canonical_payload_sha256,
      checkpoint_roots: replay.checkpoints,
      final_root: replay.root,
      event_count: replay.eventCount,
      degraded: replay.degraded,
      degradation_notes: replay.degradationNotes,
      manifest_used: replay.manifestUsed
    }
  };
}

function runStructuralRejection(vector: any): Verdict {
  try {
    const kernel = new MinimalVerifiableKernel(GENESIS_MANIFEST);
    const events = vector.events as RawEvent[];
    const trace = buildEventTelemetry(events);

    for (const event of events) {
      kernel.appendEvent(event);
    }

    const replay = kernel.replay();

    return {
      vector_id: vector.vector_id,
      runtime: runtimeName(),
      implementation: "minimal-verifiable-kernel-ts-v1",
      verdict: "FAIL",
      mismatches: ["Expected rejection but append succeeded"],
      computed: {
        event_ids: trace.event_ids,
        canonical_payload_sha256: trace.canonical_payload_sha256,
        checkpoint_roots: replay.checkpoints,
        final_root: replay.root,
        event_count: replay.eventCount,
        degraded: replay.degraded,
        degradation_notes: replay.degradationNotes,
        manifest_used: replay.manifestUsed,
        rejection_class: null,
        rejection_message: null
      }
    };
  } catch (error) {
    return {
      vector_id: vector.vector_id,
      runtime: runtimeName(),
      implementation: "minimal-verifiable-kernel-ts-v1",
      verdict: "PASS",
      mismatches: [],
      computed: {
        rejection_class: rejectionClass(error),
        rejection_message: String(error instanceof Error ? error.message : error)
      }
    };
  }
}

const verdicts = [
  runPositiveParity(vector001),
  runStructuralRejection(vector002)
];

console.log(JSON.stringify(verdicts, null, 2));
