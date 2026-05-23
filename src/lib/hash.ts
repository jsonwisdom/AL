import crypto from "node:crypto";
import { stableJson } from "./stableJson";

export function sha256StableJson(value: unknown): string {
  return crypto.createHash("sha256").update(stableJson(value), "utf8").digest("hex");
}
