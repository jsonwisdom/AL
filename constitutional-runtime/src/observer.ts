import { Hash } from "./types.js";

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
