import { readFileSync } from "node:fs";
import { validateReceipt } from "./validator.js";
import { Lineage } from "./types.js";
import { ObserverRegistry } from "./observer-registry.js";
import { ObserverTransition } from "./observer-transition.js";

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(message);
  }
}

function runRegistryBackedResolutionTest(): void {
  console.log("Running registry-backed validator resolution test...");

  const transition = readJson<ObserverTransition>("fixtures/observer.revoked.json");
  const lineage = readJson<Lineage>("fixtures/lineage.valid.json");
  const registry = readJson<ObserverRegistry>("fixtures/observer-registry.valid.json");

  const result = validateReceipt(transition, lineage, registry);

  assert(
    result.verdict === "OBSERVER_TRANSITION",
    `expected OBSERVER_TRANSITION, got ${result.verdict}`
  );

  assert(
    result.details?.resolvedObserver?.resolvedObserverSource === "registry",
    "resolvedObserverSource must be registry when registry context is injected"
  );

  assert(
    result.details?.context?.resolvedObserverSource === "registry",
    "context.resolvedObserverSource must be registry"
  );

  assert(
    result.details?.resolvedObserver?.registryLineageTip === registry.lineage_tip,
    "registryLineageTip must match registry lineage_tip"
  );

  console.log("OK resolvedObserverSource=registry with injected registry context");
  console.log("Registry-backed validator resolution test passed");
}

try {
  runRegistryBackedResolutionTest();
} catch (error) {
  console.error("Registry-backed validator resolution test failed:", error);
  process.exit(1);
}
