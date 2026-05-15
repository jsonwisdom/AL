import { Hash } from "./types.js";
import { Observer, isValidObserver } from "./observer.js";

export interface ObserverTransition {
  observer_id: Hash;
  from_status: "ACTIVE" | "REVOKED";
  to_status: "ACTIVE" | "REVOKED";
  lineage_tip: Hash;
  reason?: string;
  verdict: "OBSERVER_TRANSITION";
  mutation_surface: "Frozen";
}

export function isValidObserverTransition(
  transition: Partial<ObserverTransition>
): boolean {
  return (
    typeof transition.observer_id === "string" &&
    transition.observer_id.length === 64 &&
    (transition.from_status === "ACTIVE" || transition.from_status === "REVOKED") &&
    (transition.to_status === "ACTIVE" || transition.to_status === "REVOKED") &&
    typeof transition.lineage_tip === "string" &&
    transition.lineage_tip.length === 64 &&
    transition.verdict === "OBSERVER_TRANSITION" &&
    transition.mutation_surface === "Frozen"
  );
}

export function isMeaningfulObserverTransition(
  transition: ObserverTransition
): boolean {
  return transition.from_status !== transition.to_status;
}

export function hasConsistentObserverTransitionLineage(
  observer: Observer,
  transition: ObserverTransition
): boolean {
  return (
    isValidObserver(observer) &&
    isValidObserverTransition(transition) &&
    observer.observer_id === transition.observer_id &&
    observer.lineage_tip === transition.lineage_tip
  );
}

export function isValidObserverTransitionForObserver(
  observer: Observer,
  transition: ObserverTransition
): boolean {
  return (
    hasConsistentObserverTransitionLineage(observer, transition) &&
    observer.status === transition.from_status
  );
}

export function applyObserverTransition(
  observer: Observer,
  transition: ObserverTransition
): Observer {
  if (!isValidObserverTransitionForObserver(observer, transition)) return observer;

  return {
    ...observer,
    status: transition.to_status,
    lineage_tip: transition.lineage_tip
  };
}

export function isObserverRevocation(
  transition: ObserverTransition
): boolean {
  return (
    isValidObserverTransition(transition) &&
    transition.from_status === "ACTIVE" &&
    transition.to_status === "REVOKED"
  );
}
