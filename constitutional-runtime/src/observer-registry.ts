import { Hash } from "./types.js";
import {
  Observer,
  isActiveObserver,
  isValidObserver,
  resolveObserverAtLineage
} from "./observer.js";
import { ObserverTransition } from "./observer-transition.js";

export interface ObserverRegistry {
  verdict: "OBSERVER_REGISTRY";
  lineage_tip: Hash;
  replay_path: Hash[];
  observers: Observer[];
  totalActive: number;
  totalRevoked: number;
  mutation_surface: "Frozen";
}

export function isValidObserverRegistry(registry: Partial<ObserverRegistry>): boolean {
  return (
    registry.verdict === "OBSERVER_REGISTRY" &&
    typeof registry.lineage_tip === "string" &&
    registry.lineage_tip.length === 64 &&
    Array.isArray(registry.replay_path) &&
    registry.replay_path.every((id) => typeof id === "string" && id.length === 64) &&
    Array.isArray(registry.observers) &&
    registry.observers.every((observer) => isValidObserver(observer)) &&
    typeof registry.totalActive === "number" &&
    typeof registry.totalRevoked === "number" &&
    registry.totalActive >= 0 &&
    registry.totalRevoked >= 0 &&
    registry.mutation_surface === "Frozen"
  );
}

export function countActiveObservers(observers: Observer[], lineageTip?: Hash): number {
  return observers.filter((observer) => isActiveObserver(observer, lineageTip)).length;
}

export function countRevokedObservers(observers: Observer[]): number {
  return observers.filter((observer) => isValidObserver(observer) && observer.status === "REVOKED").length;
}

export function hasConsistentObserverTotals(registry: ObserverRegistry): boolean {
  return (
    registry.totalActive === countActiveObservers(registry.observers, registry.lineage_tip) &&
    registry.totalRevoked === countRevokedObservers(registry.observers)
  );
}

export function resolveObserverFromRegistry(
  registry: ObserverRegistry,
  observerId: Hash
): Observer | null {
  if (!isValidObserverRegistry(registry)) return null;
  return registry.observers.find((observer) => observer.observer_id === observerId) ?? null;
}

export function buildObserverRegistry(
  rawObservers: Observer[],
  lineageTip: Hash,
  knownTransitions: ObserverTransition[] = [],
  replayPath: Hash[] = []
): ObserverRegistry {
  const resolvedObservers = rawObservers.flatMap((observer) => {
    if (!isValidObserver(observer)) return [];

    const resolved = resolveObserverAtLineage(
      observer.observer_id,
      observer.public_key,
      lineageTip,
      knownTransitions
    );

    return resolved ? [resolved] : [observer];
  });

  return {
    verdict: "OBSERVER_REGISTRY",
    lineage_tip: lineageTip,
    replay_path: replayPath,
    observers: resolvedObservers,
    totalActive: countActiveObservers(resolvedObservers, lineageTip),
    totalRevoked: countRevokedObservers(resolvedObservers),
    mutation_surface: "Frozen"
  };
}
