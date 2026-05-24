export class CanonicalizationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CanonicalizationError";
  }
}

type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return Object.prototype.toString.call(value) === "[object Object]";
}

function normalize(value: unknown): JsonValue {
  if (value === null) {
    return null;
  }

  if (typeof value === "string") {
    return value.normalize("NFC");
  }

  if (typeof value === "boolean") {
    return value;
  }

  if (typeof value === "number") {
    if (!Number.isInteger(value)) {
      throw new CanonicalizationError("floats forbidden; use integers or decimal strings");
    }
    if (!Number.isSafeInteger(value)) {
      throw new CanonicalizationError("unsafe integers forbidden; use decimal strings");
    }
    return value;
  }

  if (Array.isArray(value)) {
    return value.map((item) => normalize(item));
  }

  if (isPlainObject(value)) {
    const sorted: Record<string, JsonValue> = {};
    const keys = Object.keys(value).map((key) => key.normalize("NFC")).sort();

    for (const key of keys) {
      const originalKey = Object.keys(value).find((candidate) => candidate.normalize("NFC") === key);
      if (originalKey === undefined) {
        throw new CanonicalizationError(`normalized key missing: ${key}`);
      }
      sorted[key] = normalize(value[originalKey]);
    }

    return sorted;
  }

  throw new CanonicalizationError(`unsupported value type: ${typeof value}`);
}

export function canonicalize(value: unknown): Uint8Array {
  const normalized = normalize(value);
  const json = JSON.stringify(normalized);
  return new TextEncoder().encode(json);
}

export function canonicalizeToString(value: unknown): string {
  return new TextDecoder().decode(canonicalize(value));
}
