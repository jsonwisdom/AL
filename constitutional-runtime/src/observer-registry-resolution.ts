import { Hash } from "./types.js";
import { Observer } from "./observer.js";
import {
  ObserverRegistry,
  hasConsistentObserverTotals,
  isValidObserverRegistry,
  resolveObserverFromRegistry
} from "./observer-registry.js";
import {
  ObserverTransition,
  applyObserverTransition,
  isValidObserverTransitionForObserver
} from "./observer-transition.js";

export interface RegistryBackedResolution {
  observer: Observer | null;
  source: "registry" | "missing";
  appliedTransitionCount: number;
  registryLineageTip: Hash;
}

export function resolveObserverWithRegistry(
  registry: ObserverRegistry,
  observerId: Hash,
  knownTransitions: ObserverTransition[] = []
): RegistryBackedResolution {
  if (!isValidObserverRegistry(registry) || !hasConsistentObserverTotals(registry)) {
    return {
      observer: null,
      source: "missing",
      appliedTransitionCount: 0,
      registryLineageTip: registry.lineage_tip
    };
  }

  const registryObserver = resolveObserverFromRegistry(registry, observerId);
  if (!registryObserver) {
    return {
      observer: null,
      source: "missing",
      appliedTransitionCount: 0,
      registryLineageTip: registry.lineage_tip
    };
  }

  let current = registryObserver;
  let appliedTransitionCount = 0;

  for (const transition of knownTransitions) {
    if (!isValidObserverTransitionForObserver(current, transition)) continue;
    current = applyObserverTransition(current, transition);
    appliedTransitionCount += 1;
  }

  return {
    observer: current,
    source: "registry",
    appliedTransitionCount,
    registryLineageTip: registry.lineage_tip
  };
}

export function resolveObserversWithRegistry(
  registry: ObserverRegistry,
  observerIds: Hash[],
  knownTransitions: ObserverTransition[] = []
): Map<Hash, RegistryBackedResolution> {
  const results = new Map<Hash, RegistryBackedResolution>();

  for (const observerId of observerIds) {
    results.set(
      observerId,
      resolveObserverWithRegistry(registry, observerId, knownTransitions)
    );
  }

  return results;
}

export function resolveRegistryWithTransitions(
  registry: ObserverRegistry,
  knownTransitions: ObserverTransition[] = []
): ObserverRegistry {
  if (!isValidObserverRegistry(registry)) return registry;

  const observers = registry.observers.map((observer) => {
    const result = resolveObserverWithRegistry(
      registry,
      observer.observer_id,
      knownTransitions
    );
    return result.observer ?? observer;
  });

  return {
    ...registry,
    observers,
    totalActive: observers.filter((observer) => observer.status === "ACTIVE").length,
    totalRevoked: observers.filter((observer) => observer.status === "REVOKED").length
  };
}
