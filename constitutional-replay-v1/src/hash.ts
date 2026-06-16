import { createHash } from "node:crypto";
import { canonicalize } from "./canonicalize.js";

export class HashMismatchError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "HashMismatchError";
  }
}

export function sha256Hex(bytes: Uint8Array): string {
  return createHash("sha256").update(bytes).digest("hex");
}

export function canonicalHash(value: unknown): string {
  const canonicalBytes = canonicalize(value);
  return `sha256:${sha256Hex(canonicalBytes)}`;
}

export function assertCanonicalHash(value: unknown, expected: string): void {
  const actual = canonicalHash(value);

  if (actual !== expected) {
    throw new HashMismatchError(
      `HASH_MISMATCH expected=${expected} actual=${actual}`
    );
  }
}
