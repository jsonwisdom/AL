// JCS (JSON Canonicalization Scheme) - RFC 8785 compliant subset
// Pilot 001: integers only, no floats to avoid rounding artifacts
export function jcsStringify(obj: any): string {
  if (obj === null) return "null";
  if (typeof obj === "boolean") return obj ? "true" : "false";
  if (typeof obj === "number") {
    if (!Number.isFinite(obj)) throw new Error("Invalid number");
    if (!Number.isInteger(obj)) throw new Error("Floats forbidden in Pilot 001");
    return obj.toString();
  }
  if (typeof obj === "string") return JSON.stringify(obj);
  
  if (Array.isArray(obj)) {
    return "[" + obj.map(item => jcsStringify(item)).join(",") + "]";
  }
  
  // Object: sort keys alphabetically
  const keys = Object.keys(obj).sort();
  const pairs = keys.map(k => jcsStringify(k) + ":" + jcsStringify(obj[k]));
  return "{" + pairs.join(",") + "}";
}
