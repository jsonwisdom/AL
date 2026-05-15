import { readFileSync } from "node:fs";
import {
  applyObserverTransition,
  isMeaningfulObserverTransition,
  isObserverRevocation,
  isValidObserverTransition,
  ObserverTransition
} from "./observer-transition.js";
import { Observer } from "./observer.js";

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(message);
  }
}

function runObserverTransitionTests(): void {
  console.log("Running ObserverTransition pure evaluator tests...");

  const active = readJson<ObserverTransition>("fixtures/observer.active.json");
  const revoked = readJson<ObserverTransition>("fixtures/observer.revoked.json");
  const invalidState = readJson<ObserverTransition>("fixtures/observer-transition.invalid-state.json");

  assert(
    isValidObserverTransition(active) &&
      isValidObserverTransition(revoked) &&
      isValidObserverTransition(invalidState),
    "isValidObserverTransition() must accept schema-valid transition fixtures"
  );
  console.log("OK isValidObserverTransition accepts all schema-valid transitions");

  assert(
    isMeaningfulObserverTransition(revoked) && !isMeaningfulObserverTransition(invalidState),
    "isMeaningfulObserverTransition() must distinguish state changes from self-transitions"
  );
  console.log("OK isMeaningfulObserverTransition distinguishes meaningful state changes");

  assert(
    isObserverRevocation(revoked) &&
      !isObserverRevocation(active) &&
      !isObserverRevocation(invalidState),
    "isObserverRevocation() must detect ACTIVE to REVOKED only"
  );
  console.log("OK isObserverRevocation detects ACTIVE to REVOKED only");

  const observerBefore: Observer = {
    observer_id: revoked.observer_id,
    public_key: "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
    status: "ACTIVE",
    lineage_tip: active.lineage_tip
  };

  const observerAfter = applyObserverTransition(observerBefore, revoked);
  assert(
    observerAfter.status === "REVOKED" && observerAfter.lineage_tip === revoked.lineage_tip,
    "applyObserverTransition() must apply valid ACTIVE to REVOKED transition"
  );
  console.log("OK applyObserverTransition applies valid revocation transition");

  const noOpSelfTransition = applyObserverTransition(observerBefore, invalidState);
  assert(
    noOpSelfTransition.status === observerBefore.status &&
      noOpSelfTransition.lineage_tip === observerBefore.lineage_tip,
    "applyObserverTransition() must no-op on mismatched observer_id/self-transition fixture"
  );
  console.log("OK applyObserverTransition no-ops on invalid-state fixture");

  const mismatchedPriorObserver: Observer = {
    ...observerBefore,
    status: "REVOKED"
  };
  const noOpPriorMismatch = applyObserverTransition(mismatchedPriorObserver, revoked);
  assert(
    noOpPriorMismatch.status === "REVOKED" &&
      noOpPriorMismatch.lineage_tip === mismatchedPriorObserver.lineage_tip,
    "applyObserverTransition() must no-op when observer status does not match from_status"
  );
  console.log("OK applyObserverTransition no-ops on prior-state mismatch");

  console.log("ObserverTransition tests: 6/6 passed");
}

try {
  runObserverTransitionTests();
} catch (error) {
  console.error("ObserverTransition tests failed:", error);
  process.exit(1);
}
