import {
  GENESIS_MANIFEST,
  MinimalVerifiableKernel,
  type RawEvent
} from "../../../src/kernel";

import vector001 from "../vectors/001_positive_parity_genesis.json" assert { type: "json" };
import vector002 from "../vectors/002_structural_rejection_float.json" assert { type: "json" };

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

function runPositiveParity(vector: any): Verdict {
  const kernel = new MinimalVerifiableKernel(GENESIS_MANIFEST);

  for (const event of vector.events as RawEvent[]) {
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
      final_root: replay.root,
      event_count: replay.eventCount,
      degraded: replay.degraded,
      degradation_notes: replay.degradationNotes
    }
  };
}

function runStructuralRejection(vector: any): Verdict {
  try {
    const kernel = new MinimalVerifiableKernel(GENESIS_MANIFEST);

    for (const event of vector.events as RawEvent[]) {
      kernel.appendEvent(event);
    }

    return {
      vector_id: vector.vector_id,
      runtime: runtimeName(),
      implementation: "minimal-verifiable-kernel-ts-v1",
      verdict: "FAIL",
      mismatches: ["Expected rejection but append succeeded"]
    };
  } catch (error) {
    return {
      vector_id: vector.vector_id,
      runtime: runtimeName(),
      implementation: "minimal-verifiable-kernel-ts-v1",
      verdict: "PASS",
      mismatches: [],
      computed: {
        rejection: String(error)
      }
    };
  }
}

const verdicts = [
  runPositiveParity(vector001),
  runStructuralRejection(vector002)
];

console.log(JSON.stringify(verdicts, null, 2));
