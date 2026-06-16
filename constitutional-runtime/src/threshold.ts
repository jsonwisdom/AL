import type { Signature } from "./types.js";

export function evaluateObserverThreshold(
  signatures: Signature[],
  observerSet: string[],
  threshold: number
): boolean {
  if (threshold <= 0) return true;

  const authorized = new Set(observerSet);
  const uniqueValidObservers = new Set(
    signatures
      .map((sig) => sig.observer_id)
      .filter((id) => authorized.has(id))
  );

  return uniqueValidObservers.size >= threshold;
}
