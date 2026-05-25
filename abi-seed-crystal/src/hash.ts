import { createHash } from "node:crypto";
import { canonicalize, type CanonicalJson } from "./canonicalize.js";

export function sha256HexCanonical(value: CanonicalJson): string {
  return createHash("sha256")
    .update(canonicalize(value), "utf8")
    .digest("hex");
}
