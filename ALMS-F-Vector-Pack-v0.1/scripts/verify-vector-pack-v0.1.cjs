const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "..");
const MANIFEST = path.join(ROOT, "manifest.json");
const FILE_HASHES = path.join(ROOT, "expected", "file_hashes.json");

function canonicalize(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
  return "{" + Object.keys(value).sort().map(k => JSON.stringify(k) + ":" + canonicalize(value[k])).join(",") + "}";
}

function sha256(s) {
  return crypto.createHash("sha256").update(s, "utf8").digest("hex");
}

const manifest = JSON.parse(fs.readFileSync(MANIFEST, "utf8"));

if (manifest.files.includes("expected/file_hashes.json")) {
  throw new Error("manifest must not include expected/file_hashes.json");
}

const files = {};
for (const rel of manifest.files) {
  const p = path.join(ROOT, rel);
  if (!fs.existsSync(p)) throw new Error("missing file: " + rel);
  const obj = JSON.parse(fs.readFileSync(p, "utf8"));
  files[rel] = sha256(canonicalize(obj));
}

const registry = { files, hash_algorithm: "SHA-256" };
fs.writeFileSync(FILE_HASHES, canonicalize(registry) + "\n");

const rootHash = sha256(canonicalize(registry));
process.stdout.write(rootHash + "\n");
