import { Hash } from "./types.js";
import {
  applyObserverTransition,
  ObserverTransition
} from "./observer-transition.js";

export interface Observer {
  observer_id: Hash;
  public_key: Hash;
  status: "ACTIVE" | "REVOKED";
  lineage_tip: Hash;
}

export interface ObserverReportWithEmbedded {
  observer: Observer;
  event_id: Hash;
  observed_state_root: Hash;
  signature: string;
}

export function isValidObserver(observer: Partial<Observer>): boolean {
  return (
    typeof observer.observer_id === "string" &&
    typeof observer.public_key === "string" &&
    (observer.status === "ACTIVE" || observer.status === "REVOKED") &&
    typeof observer.lineage_tip === "string" &&
    observer.observer_id.length === 64 &&
    observer.public_key.length === 64 &&
    observer.lineage_tip.length === 64
  );
}

export function isActiveObserver(
  observer: Observer,
  currentLineageTip?: Hash
): boolean {
  if (!isValidObserver(observer)) return false;
  if (observer.status !== "ACTIVE") return false;
  if (currentLineageTip && observer.lineage_tip !== currentLineageTip) {
    return false;
  }
  return true;
}

export function deduplicateObservers(observers: Observer[]): Observer[] {
  const byObserverId = new Map<Hash, Observer>();
  for (const observer of observers) {
    if (isValidObserver(observer)) {
      byObserverId.set(observer.observer_id, observer);
    }
  }
  return Array.from(byObserverId.values());
}

export function resolveObserverAtLineage(
  observerId: Hash,
  publicKey: Hash,
  lineageTip: Hash,
  knownTransitions: ObserverTransition[] = []
): Observer | null {
  const initialObserver: Observer = {
    observer_id: observerId,
    public_key: publicKey,
    status: "ACTIVE",
    lineage_tip: lineageTip
  };

  if (!isValidObserver(initialObserver)) return null;

  const matchingTransitions = knownTransitions.filter(
    (transition) =>
      transition.observer_id === observerId && transition.lineage_tip === lineageTip
  );

  let resolved = initialObserver;
  for (const transition of matchingTransitions) {
    resolved = applyObserverTransition(resolved, transition);
  }

  return resolved;
}

export function resolveObserversAtLineage(
  observerIds: Hash[],
  publicKeysByObserverId: Map<Hash, Hash>,
  lineageTip: Hash,
  knownTransitions: ObserverTransition[] = []
): Map<Hash, Observer> {
  const resolved = new Map<Hash, Observer>();

  for (const observerId of observerIds) {
    const publicKey = publicKeysByObserverId.get(observerId);
    if (!publicKey) continue;

    const observer = resolveObserverAtLineage(
      observerId,
      publicKey,
      lineageTip,
      knownTransitions
    );

    if (observer) {
      resolved.set(observerId, observer);
    }
  }

  return resolved;
}
