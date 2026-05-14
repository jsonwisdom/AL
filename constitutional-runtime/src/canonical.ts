export function canonicalize(value: unknown): string {
  return JSON.stringify(sortCanonical(value));
}

function sortCanonical(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortCanonical);

  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, v]) => [k, sortCanonical(v)])
    );
  }

  return value;
}

export function canonicalizeForSignature(event: { signatures?: unknown[]; [key: string]: unknown }): string {
  const { signatures, ...unsignedEvent } = event;
  return canonicalize(unsignedEvent);
}
