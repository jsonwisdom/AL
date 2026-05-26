const fs = require("fs");
const crypto = require("crypto");
const cp = require("child_process");

const attestationUid = process.argv[2];
const txHash = process.argv[3];

function fail(msg) {
  console.error("FAIL:", msg);
  process.exit(1);
}

function sha256File(path) {
  return crypto.createHash("sha256").update(fs.readFileSync(path)).digest("hex");
}

if (!/^0x[a-fA-F0-9]{64}$/.test(attestationUid || "")) fail("missing/invalid attestation_uid");
if (!/^0x[a-fA-F0-9]{64}$/.test(txHash || "")) fail("missing/invalid tx_hash");

cp.execSync("npm run secure-boot:budget-forecast-001", { stdio: "inherit" });
cp.execSync("npm run validate:leaf-002:draft", { stdio: "inherit" });

const DRAFT_PATH = "drafts/leaf-002/draft-manifest.json";
const CHAIN_PATH = "receipts/receipt_chain.json";

if (!fs.existsSync(CHAIN_PATH)) fail("receipt_chain.json missing — initialize genesis chain before sealing");

const draft = JSON.parse(fs.readFileSync(DRAFT_PATH, "utf8"));
if (draft.witness_status !== "DRAFT") fail("draft witness_status must be DRAFT");
if (draft.review_status !== "APPROVED") fail("draft review_status must be APPROVED");

const previousLeafHash = sha256File("receipts/budget-forecast-001/receipt_manifest.json");
const canonicalHash = sha256File(DRAFT_PATH);
const gitCommit = cp.execSync("git rev-parse HEAD").toString().trim();
const gitCommitShort = cp.execSync("git rev-parse --short HEAD").toString().trim();
const sealedAt = Math.floor(Date.now() / 1000);

const manifest = {
  leaf_id: "leaf-002",
  sequence_number: 2,
  audit_id: draft.audit_id,
  source_url: draft.source_url,
  subject: draft.subject,
  scope: draft.scope,
  claims: draft.claims,
  previous_leaf_hash: previousLeafHash,
  canonical_json_sha256: canonicalHash,
  schema_uid: "0x640f314744e9cf8ad9f72cfbeab54fb71e20b5489540d9e302c69bccceb60177",
  attestation_uid: attestationUid,
  attestation_tx_hash: txHash,
  git_commit: gitCommit,
  git_commit_short: gitCommitShort,
  schema_version: "receipt_manifest.v1",
  witness_status: "SEALED",
  review_status: "APPROVED",
  private_key_terminal: false,
  sealed_at_unix: sealedAt,
  receipt_sha256: null
};

manifest.receipt_sha256 = crypto
  .createHash("sha256")
  .update(JSON.stringify(manifest, Object.keys(manifest).sort()))
  .digest("hex");

fs.mkdirSync("receipts/budget-forecast-002", { recursive: true });
fs.writeFileSync("receipts/budget-forecast-002/receipt_manifest.json", JSON.stringify(manifest, null, 2) + "\n");

const chain = JSON.parse(fs.readFileSync(CHAIN_PATH, "utf8"));
chain.leaves.push({
  leaf_id: "leaf-002",
  sequence_number: 2,
  receipt_sha256: manifest.receipt_sha256,
  parent_receipt_sha256: previousLeafHash,
  parent_sequence_number: 1,
  private_key_terminal: false,
  sealed_at: sealedAt
});
fs.writeFileSync(CHAIN_PATH, JSON.stringify(chain, null, 2) + "\n");

console.log("PASS: Leaf 002 sealed");
console.log(JSON.stringify({ receipt: "receipts/budget-forecast-002/receipt_manifest.json", receipt_sha256: manifest.receipt_sha256 }, null, 2));
