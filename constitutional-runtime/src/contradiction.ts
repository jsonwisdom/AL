import { DivergenceClass, Hash } from "./types.js";

export interface ObserverReport {
  observer_id: Hash;
  event_id: Hash;
  observed_state_root: Hash;
  signature: string;
}

export interface ContradictionReceipt {
  event_id: Hash;
  replay_path?: Hash[];
  lineage_tip: Hash;
  reports: ObserverReport[];
  verdict: "CONSTITUTIONAL_CONTRADICTION";
  divergence: "D3";
  mutation_surface: "Frozen";
}

export function detectContradiction(
  receipt: ContradictionReceipt
): {
  isContradiction: boolean;
  divergence: DivergenceClass;
  uniqueObserverCount: number;
  conflictingRoots: Hash[];
  isLineageBound: boolean;
} {
  const isLineageBound = typeof receipt.lineage_tip === "string" && receipt.lineage_tip.length === 64;

  if (!isLineageBound) {
    return {
      isContradiction: false,
      divergence: "D0",
      uniqueObserverCount: 0,
      conflictingRoots: [],
      isLineageBound: false
    };
  }

  if (receipt.reports.length < 2) {
    return {
      isContradiction: false,
      divergence: "D0",
      uniqueObserverCount: 0,
      conflictingRoots: [],
      isLineageBound: true
    };
  }

  const byObserver = new Map<Hash, ObserverReport>();
  for (const report of receipt.reports) {
    byObserver.set(report.observer_id, report);
  }

  const uniqueReports = Array.from(byObserver.values());
  const uniqueObserverCount = uniqueReports.length;

  if (uniqueObserverCount < 2) {
    return {
      isContradiction: false,
      divergence: "D0",
      uniqueObserverCount,
      conflictingRoots: [],
      isLineageBound: true
    };
  }

  const rootSet = new Set<Hash>();
  for (const report of uniqueReports) {
    rootSet.add(report.observed_state_root);
  }

  const hasConflict = rootSet.size > 1;

  return {
    isContradiction: hasConflict,
    divergence: hasConflict ? "D3" : "D0",
    uniqueObserverCount,
    conflictingRoots: hasConflict ? Array.from(rootSet) : [],
    isLineageBound: true
  };
}

export function isValidContradictionReceipt(
  receipt: Partial<ContradictionReceipt>
): boolean {
  return (
    receipt.verdict === "CONSTITUTIONAL_CONTRADICTION" &&
    receipt.divergence === "D3" &&
    receipt.mutation_surface === "Frozen" &&
    typeof receipt.event_id === "string" &&
    typeof receipt.lineage_tip === "string" &&
    Array.isArray(receipt.reports) &&
    receipt.reports.length >= 2
  );
}
