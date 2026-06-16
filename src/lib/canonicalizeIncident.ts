import { sha256StableJson } from "./hash";

export interface CanonicalizedResult {
  version: "E06.V1";
  canonicalIncident: Record<string, unknown>;
  canonicalIncidentHash: string;
}

export async function canonicalizeIncident(
  rawIncident: unknown,
  timestamp: number
): Promise<CanonicalizedResult> {
  const raw =
    rawIncident && typeof rawIncident === "object"
      ? (rawIncident as Record<string, unknown>)
      : { value: rawIncident };

  const canonicalIncident: Record<string, unknown> = {
    ...raw,
    _canonicalVersion: "E06.V1",
    _normalizedAt: timestamp,
  };

  return {
    version: "E06.V1",
    canonicalIncident,
    canonicalIncidentHash: sha256StableJson(canonicalIncident),
  };
}
