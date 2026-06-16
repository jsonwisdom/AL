import { DivergenceClass } from "./types.js";

export function divergenceClass(a: string, b: string): DivergenceClass {
  if (a === b) return "D0";
  // v0.1 conservative rule: any root mismatch is deterministic replay failure
  return "D3";
}

export function mutationSurface(d: DivergenceClass): "Mutable" | "Frozen" {
  return d === "D3" || d === "D4" ? "Frozen" : "Mutable";
}
