import { createHash } from "node:crypto";
import { canonicalize } from "./canonical.js";

export function sha256Hex(value: unknown): string {
  return createHash("sha256")
    .update(canonicalize(value))
    .digest("hex");
}
