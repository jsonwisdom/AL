import { readFileSync } from "node:fs";
import {
  DegradedObserverMode,
  assessObserverHealth,
  calculateActiveRatio,
  determineConfidenceLevel,
  isFakeEscalationSignal,
  isValidDegradedObserverMode
} from "./degraded-mode.js";

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(message);
  }
}

function runDegradedModeTests(): void {
  console.log("Running DegradedMode pure evaluator tests...");

  const validDegraded = readJson<DegradedObserverMode>("fixtures/degraded-observer-mode.valid.json");
  const fakeEscalation = readJson<DegradedObserverMode>("fixtures/degraded-observer-mode.fake-escalation.json");

  assert(
    isValidDegradedObserverMode(validDegraded) &&
      isValidDegradedObserverMode(fakeEscalation),
    "isValidDegradedObserverMode() must accept valid fixtures"
  );
  console.log("OK isValidDegradedObserverMode accepts valid fixtures");

  assert(
    calculateActiveRatio(7, 10) === 0.7 &&
      calculateActiveRatio(9, 10) === 0.9 &&
      calculateActiveRatio(0, 10) === 0,
    "calculateActiveRatio() must compute expected ratios"
  );
  console.log("OK calculateActiveRatio computes expected ratios");

  assert(
    determineConfidenceLevel(0.95) === "HEALTHY" &&
      determineConfidenceLevel(0.7) === "DEGRADED" &&
      determineConfidenceLevel(0.4) === "INSUFFICIENT",
    "determineConfidenceLevel() must apply expected thresholds"
  );
  console.log("OK determineConfidenceLevel applies expected thresholds");

  const health = assessObserverHealth(10, 7);
  assert(
    health.activeRatio === 0.7 &&
      health.confidenceLevel === "DEGRADED" &&
      health.missingObserverCount === 3 &&
      health.isDegraded === true,
    "assessObserverHealth() must return expected degraded assessment"
  );
  console.log("OK assessObserverHealth returns expected degraded assessment");

  assert(
    !isFakeEscalationSignal(validDegraded) &&
      isFakeEscalationSignal(fakeEscalation),
    "isFakeEscalationSignal() must flag healthy-surface degraded claims"
  );
  console.log("OK isFakeEscalationSignal flags fake escalation signal");

  const zeroActive = assessObserverHealth(5, 0);
  assert(
    zeroActive.activeRatio === 0 &&
      zeroActive.confidenceLevel === "INSUFFICIENT" &&
      zeroActive.missingObserverCount === 5,
    "zero active observers must be insufficient"
  );
  console.log("OK zero active observers handled as INSUFFICIENT");

  const zeroExpected = assessObserverHealth(0, 0);
  assert(
    zeroExpected.activeRatio === 0 &&
      zeroExpected.confidenceLevel === "INSUFFICIENT" &&
      zeroExpected.missingObserverCount === 0,
    "zero expected observers must not create authority"
  );
  console.log("OK zero expected observers handled without authority expansion");

  console.log("DegradedMode tests: 7/7 passed");
}

try {
  runDegradedModeTests();
} catch (error) {
  console.error("DegradedMode tests failed:", error);
  process.exit(1);
}
