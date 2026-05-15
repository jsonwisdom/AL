import { DivergenceClass, Hash } from "./types.js";
import { Observer, isActiveObserver } from "./observer.js";

export interface ObserverReport {
  observer: Observer;
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
  uniqueActiveObservers: number;
  conflictingRoots: Hash[];
  isLineageBound: boolean;
  activeObserverCount: number;
} {
  const isLineageBound = typeof receipt.lineage_tip === "string" && receipt.lineage_tip.length === 64;

  if (!isLineageBound) {
    return {
      isContradiction: false,
      divergence: "D0",
      uniqueActiveObservers: 0,
      conflictingRoots: [],
      isLineageBound: false,
      activeObserverCount: 0
    };
  }

  const activeReports = receipt.reports.filter((report) =>
    isActiveObserver(report.observer, receipt.lineage_tip)
  );
  const activeObserverCount = activeReports.length;

  if (activeObserverCount < 2) {
    return {
      isContradiction: false,
      divergence: "D0",
      uniqueActiveObservers: 0,
      conflictingRoots: [],
      isLineageBound: true,
      activeObserverCount
    };
  }

  const byObserver = new Map<Hash, ObserverReport>();
  for (const report of activeReports) {
    byObserver.set(report.observer.observer_id, report);
  }

  const uniqueReports = Array.from(byObserver.values());
  const uniqueActiveObservers = uniqueReports.length;

  if (uniqueActiveObservers < 2) {
    return {
      isContradiction: false,
      divergence: "D0",
      uniqueActiveObservers,
      conflictingRoots: [],
      isLineageBound: true,
      activeObserverCount
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
    uniqueActiveObservers,
    conflictingRoots: hasConflict ? Array.from(rootSet) : [],
    isLineageBound: true,
    activeObserverCount
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
