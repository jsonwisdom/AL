import { Hash } from "./types.js";

export type ConfidenceLevel = "HEALTHY" | "DEGRADED" | "INSUFFICIENT";

export interface DegradedObserverMode {
  verdict: "DEGRADED_OBSERVER_MODE";
  lineage_tip: Hash;
  replay_path?: Hash[];
  expectedObserverCount: number;
  activeObserverCount: number;
  missingObserverCount: number;
  activeRatio: number;
  confidenceLevel: ConfidenceLevel;
  mutation_surface: "Frozen";
}

export interface ObserverHealthAssessment {
  activeRatio: number;
  confidenceLevel: ConfidenceLevel;
  missingObserverCount: number;
  isDegraded: boolean;
}

export function calculateActiveRatio(
  activeObserverCount: number,
  expectedObserverCount: number
): number {
  if (expectedObserverCount <= 0) return 0;
  return Math.min(1, Math.max(0, activeObserverCount / expectedObserverCount));
}

export function determineConfidenceLevel(activeRatio: number): ConfidenceLevel {
  if (activeRatio >= 0.9) return "HEALTHY";
  if (activeRatio >= 0.5) return "DEGRADED";
  return "INSUFFICIENT";
}

export function assessObserverHealth(
  expectedObserverCount: number,
  activeObserverCount: number
): ObserverHealthAssessment {
  const activeRatio = calculateActiveRatio(activeObserverCount, expectedObserverCount);
  const confidenceLevel = determineConfidenceLevel(activeRatio);

  return {
    activeRatio,
    confidenceLevel,
    missingObserverCount: Math.max(0, expectedObserverCount - activeObserverCount),
    isDegraded: confidenceLevel !== "HEALTHY"
  };
}

export function isValidDegradedObserverMode(
  mode: Partial<DegradedObserverMode>
): boolean {
  if (
    mode.verdict !== "DEGRADED_OBSERVER_MODE" ||
    typeof mode.lineage_tip !== "string" ||
    mode.lineage_tip.length !== 64 ||
    (mode.replay_path !== undefined &&
      (!Array.isArray(mode.replay_path) ||
        !mode.replay_path.every((id) => typeof id === "string" && id.length === 64))) ||
    typeof mode.expectedObserverCount !== "number" ||
    typeof mode.activeObserverCount !== "number" ||
    typeof mode.missingObserverCount !== "number" ||
    typeof mode.activeRatio !== "number" ||
    (mode.confidenceLevel !== "HEALTHY" &&
      mode.confidenceLevel !== "DEGRADED" &&
      mode.confidenceLevel !== "INSUFFICIENT") ||
    mode.mutation_surface !== "Frozen"
  ) {
    return false;
  }

  const assessed = assessObserverHealth(
    mode.expectedObserverCount,
    mode.activeObserverCount
  );

  return (
    mode.missingObserverCount === assessed.missingObserverCount &&
    Math.abs(mode.activeRatio - assessed.activeRatio) < Number.EPSILON &&
    mode.confidenceLevel === assessed.confidenceLevel
  );
}

export function isFakeEscalationSignal(mode: DegradedObserverMode): boolean {
  if (!isValidDegradedObserverMode(mode)) return false;
  return mode.confidenceLevel === "DEGRADED" && mode.activeRatio >= 0.85;
}
