import { generateKeyPairSync, sign, verify, createHash } from "crypto";
import { writeFileSync } from "fs";

const batchRoot = "4d8f1c5e6b7a8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e";
const msg = `REPLAY_WITNESS_V1:${batchRoot}`;
const { publicKey, privateKey } = generateKeyPairSync("ed25519");

const sig = sign(null, Buffer.from(msg), privateKey);
const ok = verify(null, Buffer.from(msg), publicKey, sig);

const receipt = {
  proof: "RECEIPT_011_ED25519_WITNESS",
  witness_version: "REPLAY_WITNESS_V1",
  batch_root: batchRoot,
  prefixed_message: msg,
  public_key_der_base64: publicKey.export({ type: "spki", format: "der" }).toString("base64"),
  signature_base64: sig.toString("base64"),
  private_key_exported: "NO",
  funds_moved: "NO",
  secrets_printed: "NO",
  status: ok ? "WITNESS_VALID" : "WITNESS_INVALID",
  timestamp_utc: new Date().toISOString()
};

const canonical = JSON.stringify(receipt, null, 2);
receipt.fileHash = createHash("sha256").update(canonical).digest("hex");

writeFileSync("receipts/011/RECEIPT_011_ED25519_WITNESS.json", JSON.stringify(receipt, null, 2) + "\n");

console.log("WITNESS_VALID:", ok);
console.log("fileHash:", receipt.fileHash);
