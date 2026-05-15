import { readFileSync } from "node:fs";
import { ObserverRegistry } from "./observer-registry.js";
import { ObserverTransition } from "./observer-transition.js";
import {
  resolveObserverWithRegistry,
  resolveObserversWithRegistry,
  resolveRegistryWithTransitions
} from "./observer-registry-resolution.js";

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(message);
  }
}

function runObserverRegistryResolutionTests(): void {
  console.log("Running ObserverRegistry resolution tests...");

  const registry = readJson<ObserverRegistry>("fixtures/observer-registry.valid.json");
  const revokedTransition = readJson<ObserverTransition>("fixtures/observer.revoked.json");

  const firstObserverId = "1111111111111111111111111111111111111111111111111111111111111111";
  const secondObserverId = "2222222222222222222222222222222222222222222222222222222222222222";
  const thirdObserverId = "3333333333333333333333333333333333333333333333333333333333333333";
  const unknownObserverId = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff";

  const resolvedFirst = resolveObserverWithRegistry(registry, firstObserverId, []);
  assert(
    resolvedFirst.source === "registry" &&
      resolvedFirst.observer !== null &&
      resolvedFirst.observer.status === "ACTIVE" &&
      resolvedFirst.appliedTransitionCount === 0,
    "resolveObserverWithRegistry() must return active observer from registry"
  );
  console.log("OK resolveObserverWithRegistry returns observer from registry snapshot");

  const resolvedSecondWithTransition = resolveObserverWithRegistry(registry, secondObserverId, [
    revokedTransition
  ]);
  assert(
    resolvedSecondWithTransition.source === "registry" &&
      resolvedSecondWithTransition.observer !== null &&
      resolvedSecondWithTransition.observer.status === "REVOKED" &&
      resolvedSecondWithTransition.appliedTransitionCount === 1,
    "resolveObserverWithRegistry() must apply valid matching transition"
  );
  console.log("OK resolveObserverWithRegistry applies valid matching transition");

  const resolvedMany = resolveObserversWithRegistry(registry, [firstObserverId, thirdObserverId], []);
  assert(
    resolvedMany.size === 2 &&
      resolvedMany.get(thirdObserverId)?.observer?.status === "REVOKED",
    "resolveObserversWithRegistry() must resolve multiple observers"
  );
  console.log("OK resolveObserversWithRegistry resolves multiple observers");

  const updatedRegistry = resolveRegistryWithTransitions(registry, [revokedTransition]);
  assert(
    updatedRegistry.totalActive === 1 && updatedRegistry.totalRevoked === 2,
    `resolveRegistryWithTransitions() must update totals after transition, got active=${updatedRegistry.totalActive}, revoked=${updatedRegistry.totalRevoked}`
  );
  console.log("OK resolveRegistryWithTransitions updates snapshot totals");

  const unknown = resolveObserverWithRegistry(registry, unknownObserverId, []);
  assert(
    unknown.source === "missing" && unknown.observer === null,
    "resolveObserverWithRegistry() must return missing/null for unknown observer"
  );
  console.log("OK resolveObserverWithRegistry handles unknown observer");

  console.log("ObserverRegistry resolution tests: 5/5 passed");
}

try {
  runObserverRegistryResolutionTests();
} catch (error) {
  console.error("ObserverRegistry resolution tests failed:", error);
  process.exit(1);
}
