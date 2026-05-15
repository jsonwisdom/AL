import { readFileSync } from "node:fs";
import {
  ObserverRegistry,
  buildObserverRegistry,
  countActiveObservers,
  countRevokedObservers,
  hasConsistentObserverTotals,
  isValidObserverRegistry,
  resolveObserverFromRegistry
} from "./observer-registry.js";

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(message);
  }
}

function runObserverRegistryTests(): void {
  console.log("Running ObserverRegistry pure evaluator tests...");

  const registry = readJson<ObserverRegistry>("fixtures/observer-registry.valid.json");

  assert(
    isValidObserverRegistry(registry),
    "isValidObserverRegistry() must accept valid registry fixture"
  );
  console.log("OK isValidObserverRegistry accepts valid registry fixture");

  assert(
    hasConsistentObserverTotals(registry),
    "hasConsistentObserverTotals() must pass on registry fixture"
  );
  console.log("OK hasConsistentObserverTotals passes on registry fixture");

  const activeCount = countActiveObservers(registry.observers, registry.lineage_tip);
  const revokedCount = countRevokedObservers(registry.observers);
  assert(
    activeCount === 2 && revokedCount === 1,
    `count mismatch: active=${activeCount}, revoked=${revokedCount}`
  );
  console.log("OK countActiveObservers / countRevokedObservers correct (2/1)");

  const resolved = resolveObserverFromRegistry(
    registry,
    "1111111111111111111111111111111111111111111111111111111111111111"
  );
  assert(
    resolved !== null && resolved.status === "ACTIVE",
    "resolveObserverFromRegistry() must return expected active observer"
  );
  console.log("OK resolveObserverFromRegistry returns expected observer");

  const built = buildObserverRegistry(
    registry.observers,
    registry.lineage_tip,
    [],
    registry.replay_path
  );
  assert(
    built.verdict === "OBSERVER_REGISTRY" &&
      built.totalActive === 2 &&
      built.totalRevoked === 1 &&
      built.replay_path.length === registry.replay_path.length,
    "buildObserverRegistry() must construct consistent registry"
  );
  console.log("OK buildObserverRegistry constructs consistent registry");

  const empty = buildObserverRegistry(
    [],
    "0000000000000000000000000000000000000000000000000000000000000000",
    [],
    []
  );
  assert(
    empty.totalActive === 0 && empty.totalRevoked === 0,
    "empty registry must have zero active and revoked observers"
  );
  console.log("OK empty registry edge case handled correctly");

  console.log("ObserverRegistry tests: 6/6 passed");
}

try {
  runObserverRegistryTests();
} catch (error) {
  console.error("ObserverRegistry tests failed:", error);
  process.exit(1);
}
