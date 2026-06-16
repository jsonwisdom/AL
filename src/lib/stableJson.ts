export function normalize(value: unknown): unknown {
  if (value === null) return null;
  if (typeof value === "bigint") return value.toString();
  if (value instanceof Date) return value.toISOString();
  if (Array.isArray(value)) return value.map(normalize);

  if (typeof value === "object") {
    const obj = value as Record<string, unknown>;
    return Object.keys(obj)
      .sort()
      .reduce<Record<string, unknown>>((acc, key) => {
        const v = obj[key];
        if (v !== undefined) acc[key] = normalize(v);
        return acc;
      }, {});
  }

  return value;
}

export function stableJson(value: unknown): string {
  return JSON.stringify(normalize(value));
}
