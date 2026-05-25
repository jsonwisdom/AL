export type CanonicalJson =
  | string
  | number
  | boolean
  | null
  | { readonly [key: string]: CanonicalJson }
  | readonly CanonicalJson[];

function isPlainObject(value: unknown): value is Record<string, CanonicalJson> {
  if (value === null || typeof value !== "object") return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

export function canonicalize(value: CanonicalJson): string {
  if (value === undefined) throw new Error("UNDEFINED_FORBIDDEN");

  if (typeof value === "number") {
    if (!Number.isInteger(value) || !Number.isSafeInteger(value)) {
      throw new Error("UNSAFE_OR_NON_INTEGER_NUMBER_FORBIDDEN");
    }
    return value.toString();
  }

  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }

  if (Array.isArray(value)) {
    for (let i = 0; i < value.length; i += 1) {
      if (!(i in value)) throw new Error("SPARSE_ARRAY_FORBIDDEN");
    }
    return `[${value.map(canonicalize).join(",")}]`;
  }

  if (!isPlainObject(value)) throw new Error("NON_PLAIN_OBJECT_FORBIDDEN");

  const keys = Object.keys(value).sort();
  return `{${keys
    .map((key) => {
      const child = value[key];
      if (child === undefined) throw new Error("UNDEFINED_FORBIDDEN");
      return `${JSON.stringify(key)}:${canonicalize(child)}`;
    })
    .join(",")}}`;
}
